import os
import re
import time
from datetime import datetime, timezone

from PyQt6.QtCore import QThread, pyqtSignal

try:
    import winreg
except ImportError:
    winreg = None

try:
    import psutil
    import win32gui
    import win32process
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False


SYSTEM_EXES = {
    "explorer.exe",
    "shellexperiencehost.exe",
    "startmenuexperiencehost.exe",
    "searchhost.exe",
    "searchapp.exe",
    "applicationframehost.exe",
    "textinputhost.exe",
    "dwm.exe",
    "lockapp.exe",
    "taskhostw.exe",
    "ctfmon.exe",
    "widgets.exe",
    "photos.exe",
    "taskmgr.exe",
}

SELF_EXES = {
    "focusync.exe",
    "code.exe",
    "pycharm64.exe",
    "python.exe",  # mevcut davranışı korumak için bırakıldı
}

BAD_EXE_HINTS = (
    "unins", "uninstall", "updater", "update", "setup",
    "install", "repair", "helper", "crash", "service"
)


def format_seconds(seconds: float) -> str:
    total = int(round(seconds))
    saat = total // 3600
    dakika = (total % 3600) // 60
    saniye = total % 60
    return f"{saat:02d}:{dakika:02d}:{saniye:02d}"


def normalize_exe_name(text: str) -> str:
    text = (text or "").strip().strip('"').strip("'")
    text = os.path.basename(text)
    return text.lower().strip()


def get_active_window_info() -> tuple[str, str]:
    if not WIN32_AVAILABLE:
        return "", ""

    try:
        hwnd = win32gui.GetForegroundWindow()
        if not hwnd:
            return "", ""

        title = win32gui.GetWindowText(hwnd).strip()
        _, pid = win32process.GetWindowThreadProcessId(hwnd)

        if not pid:
            return "", title

        proc = psutil.Process(pid)
        exe_name = proc.name().lower().strip()

        return exe_name, title.strip()

    except Exception as e:
        print(f"[Whitelist] Aktif pencere bilgisi alınamadı: {e}")
        return "", ""


def _safe_reg_read(key, value_name, default=""):
    if winreg is None:
        return default

    try:
        value, _ = winreg.QueryValueEx(key, value_name)
        return value
    except OSError:
        return default


def _extract_exe_path(raw_value: str) -> str:
    if not raw_value:
        return ""

    text = os.path.expandvars(str(raw_value).strip())
    lower = text.lower()
    exe_index = lower.find(".exe")

    if exe_index == -1:
        return ""

    candidate = text[:exe_index + 4].strip().strip('"').strip("'")
    candidate = candidate.rstrip(" ,")
    candidate = os.path.normpath(candidate)

    if candidate.lower().endswith(".exe"):
        return candidate

    return ""


def _score_exe_candidate(path: str, display_name: str) -> int:
    name = os.path.basename(path).lower().strip()
    stem = os.path.splitext(name)[0]
    tokens = re.findall(r"[a-z0-9]+", display_name.lower())

    if name in SYSTEM_EXES:
        return -999

    score = 0

    if stem in display_name.lower():
        score += 8

    for token in tokens:
        if len(token) < 3:
            continue
        if token in stem:
            score += 3
        if stem == token:
            score += 5

    for bad in BAD_EXE_HINTS:
        if bad in stem:
            score -= 6

    if stem == "app":
        score -= 2

    score -= len(name) // 10
    return score


def _guess_exe_from_install_location(install_location: str, display_name: str) -> str:
    if not install_location:
        return ""

    folder = os.path.expandvars(str(install_location).strip().strip('"'))
    if not os.path.isdir(folder):
        return ""

    candidates = []
    try:
        for entry in os.scandir(folder):
            if entry.is_file() and entry.name.lower().endswith(".exe"):
                candidates.append(entry.path)
    except OSError:
        return ""

    if not candidates:
        return ""

    best_path = max(candidates, key=lambda p: _score_exe_candidate(p, display_name))
    best_score = _score_exe_candidate(best_path, display_name)

    if best_score < -2:
        return ""

    return os.path.normpath(best_path)


def iter_installed_apps() -> list[dict]:
    if os.name != "nt" or winreg is None:
        return []

    uninstall_key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
    apps = []
    seen = set()

    registry_targets = [
        (winreg.HKEY_LOCAL_MACHINE, winreg.KEY_READ | getattr(winreg, "KEY_WOW64_64KEY", 0)),
        (winreg.HKEY_LOCAL_MACHINE, winreg.KEY_READ | getattr(winreg, "KEY_WOW64_32KEY", 0)),
        (winreg.HKEY_CURRENT_USER, winreg.KEY_READ),
    ]

    for root, access in registry_targets:
        try:
            with winreg.OpenKey(root, uninstall_key_path, 0, access) as parent_key:
                index = 0
                while True:
                    try:
                        subkey_name = winreg.EnumKey(parent_key, index)
                        index += 1
                    except OSError:
                        break

                    try:
                        with winreg.OpenKey(parent_key, subkey_name) as app_key:
                            display_name = str(_safe_reg_read(app_key, "DisplayName", "")).strip()
                            if not display_name:
                                continue

                            system_component = _safe_reg_read(app_key, "SystemComponent", 0)
                            try:
                                if int(system_component) == 1:
                                    continue
                            except Exception:
                                pass

                            release_type = str(_safe_reg_read(app_key, "ReleaseType", "")).strip().lower()
                            if release_type in {"hotfix", "security update", "update rollup"}:
                                continue

                            display_icon = str(_safe_reg_read(app_key, "DisplayIcon", "")).strip()
                            install_location = str(_safe_reg_read(app_key, "InstallLocation", "")).strip()
                            publisher = str(_safe_reg_read(app_key, "Publisher", "")).strip()

                            exe_path = _extract_exe_path(display_icon)
                            if not exe_path:
                                exe_path = _guess_exe_from_install_location(install_location, display_name)

                            if not exe_path:
                                continue

                            exe_name = os.path.basename(exe_path).lower().strip()
                            if not exe_name.endswith(".exe"):
                                continue

                            if any(bad in exe_name for bad in ("unins", "uninstall")):
                                continue

                            key = (display_name.lower(), exe_name, exe_path.lower())
                            if key in seen:
                                continue
                            seen.add(key)

                            apps.append({
                                "display_name": display_name,
                                "exe_name": exe_name,
                                "exe_path": exe_path,
                                "publisher": publisher,
                                "source": "registry",
                            })

                    except OSError:
                        continue

        except OSError:
            continue

    apps.sort(key=lambda x: (x["display_name"].lower(), x["exe_name"]))
    return apps


def build_violation_entry(active_exe: str, active_start: float | None):
    if not active_exe or active_start is None:
        return None

    end_time = time.time()
    sure = end_time - active_start

    if sure < 1.0:
        return None

    duration_seconds = int(round(sure))
    return {
        "app_name": active_exe,
        "duration_seconds": duration_seconds,
        "duration_hms": format_seconds(duration_seconds),
        "started_at": datetime.fromtimestamp(active_start, tz=timezone.utc),
        "ended_at": datetime.fromtimestamp(end_time, tz=timezone.utc),
    }


class MonitorWorker(QThread):
    violation_found = pyqtSignal(str)
    no_violation = pyqtSignal()

    def __init__(self, get_whitelist_fn, interval_ms: int = 10_000, parent=None):
        super().__init__(parent)
        self._get_whitelist = get_whitelist_fn
        self.interval_ms = interval_ms
        self._running = False
        self._last_state = None  # "ok" veya ihlal detay string'i

    def _emit_ok_if_changed(self):
        if self._last_state != "ok":
            self._last_state = "ok"
            self.no_violation.emit()

    def _emit_violation_if_changed(self, detay: str):
        if self._last_state != detay:
            self._last_state = detay
            self.violation_found.emit(detay)

    def run(self):
        self._running = True

        while self._running:
            whitelist = self._get_whitelist()

            exe_name, window_title = get_active_window_info()
            window_title_lower = window_title.lower().strip() if window_title else ""

            # Geçici debug
            if exe_name or window_title:
                print(f"[FG DEBUG] exe={exe_name!r} | title={window_title!r}")

            if not exe_name:
                self._emit_ok_if_changed()

            elif exe_name in SYSTEM_EXES:
                self._emit_ok_if_changed()

            elif exe_name in SELF_EXES:
                self._emit_ok_if_changed()

            elif exe_name == "python.exe" and "focusync" in window_title_lower:
                self._emit_ok_if_changed()

            else:
                izinli = exe_name in whitelist

                if izinli:
                    self._emit_ok_if_changed()
                else:
                    detay = f"{exe_name} | {window_title}" if window_title else exe_name
                    self._emit_violation_if_changed(detay)

            elapsed = 0
            while self._running and elapsed < self.interval_ms:
                self.msleep(200)
                elapsed += 200
    def stop(self):
        self._running = False
        self.wait()


class WhitelistLogic:
    def __init__(self, user_id, db_manager):
        self.user_id = user_id
        self.db_manager = db_manager

        self._whitelist: set[str] = set()
        self.ihlal: bool = False
        self._son_ihlal = ""

        self._last_violation_exe: str | None = None
        self._last_violation_detay: str = ""

        self._violation_log: list[dict] = []
        self._active_violation_exe: str = ""
        self._active_violation_start: float | None = None

        self._monitoring_start_time: float | None = None
        self._violation_start_time: float | None = None
        self._total_monitoring_seconds: float = 0.0
        self._total_violation_seconds: float = 0.0

    def get_whitelist(self):
        return set(self._whitelist)

    def whitelist_items(self):
        return sorted(self._whitelist)

    def has_last_violation(self) -> bool:
        return bool(self._last_violation_exe)

    def clear_last_violation(self):
        self._last_violation_exe = None
        self._last_violation_detay = ""

    def current_violation_exe(self) -> str:
        if not self._son_ihlal:
            return ""
        return self._son_ihlal.split(" | ", 1)[0].strip().lower()

    def start_monitoring(self):
        self._monitoring_start_time = time.time()
        self._violation_start_time = None
        self._total_monitoring_seconds = 0.0
        self._total_violation_seconds = 0.0
        self.ihlal = False
        self._son_ihlal = ""

        self._violation_log = []
        self._active_violation_exe = ""
        self._active_violation_start = None

        self.clear_last_violation()

    def add_exe_to_whitelist(self, exe_name: str):
        exe_name = normalize_exe_name(exe_name)

        if not exe_name:
            return {
                "ok": False,
                "level": "warning",
                "msg": "Geçerli bir exe adı bulunamadı.",
                "exe_name": "",
                "clear_info": None,
            }

        if not exe_name.endswith(".exe"):
            return {
                "ok": False,
                "level": "warning",
                "msg": "Lütfen .exe uzantılı bir uygulama seç.",
                "exe_name": exe_name,
                "clear_info": None,
            }

        if exe_name in self._whitelist:
            return {
                "ok": False,
                "level": "info",
                "msg": f"{exe_name} zaten whitelist içinde.",
                "exe_name": exe_name,
                "clear_info": None,
            }

        self._whitelist.add(exe_name)

        clear_info = None
        if self._last_violation_exe == exe_name:
            if self.ihlal and self.current_violation_exe() == exe_name:
                clear_info = self.process_no_violation()
            self.clear_last_violation()

        return {
            "ok": True,
            "level": "success",
            "msg": f"{exe_name} whitelist'e eklendi.",
            "exe_name": exe_name,
            "clear_info": clear_info,
        }

    def remove_exe_from_whitelist(self, exe_name: str):
        exe_name = normalize_exe_name(exe_name)

        if not exe_name:
            return False, ""

        self._whitelist.discard(exe_name)
        return True, exe_name

    def allow_last_violation(self):
        exe_name = (self._last_violation_exe or "").strip().lower()

        if not exe_name:
            return {
                "ok": False,
                "level": "info",
                "msg": "İzin verilecek son ihlal bulunmuyor.",
                "exe_name": "",
                "clear_info": None,
            }

        if exe_name in SYSTEM_EXES:
            self.clear_last_violation()
            return {
                "ok": False,
                "level": "info",
                "msg": f"{exe_name} zaten sistem uygulaması olarak izinli.",
                "exe_name": exe_name,
                "clear_info": None,
            }

        if exe_name in SELF_EXES:
            self.clear_last_violation()
            return {
                "ok": False,
                "level": "info",
                "msg": f"{exe_name} zaten uygulama tarafından izinli.",
                "exe_name": exe_name,
                "clear_info": None,
            }

        if exe_name in self._whitelist:
            self.clear_last_violation()
            return {
                "ok": False,
                "level": "info",
                "msg": f"{exe_name} zaten whitelist içinde.",
                "exe_name": exe_name,
                "clear_info": None,
            }

        return self.add_exe_to_whitelist(exe_name)

    def process_violation(self, detay: str):
        exe_name = detay.split(" | ", 1)[0].strip().lower() if detay else ""

        if exe_name and exe_name.endswith(".exe"):
            self._last_violation_exe = exe_name
            self._last_violation_detay = detay

        if self._active_violation_exe and self._active_violation_exe != exe_name:
            self.finish_current_episode()

        if exe_name and self._active_violation_exe != exe_name:
            self._active_violation_exe = exe_name
            self._active_violation_start = time.time()

        started_new = False
        if not self.ihlal:
            self.ihlal = True
            self._son_ihlal = detay
            self._violation_start_time = time.time()
            started_new = True
        else:
            self._son_ihlal = detay

        return {
            "detay": detay,
            "exe_name": exe_name,
            "started_new": started_new,
        }

    def process_no_violation(self):
        last_violation = self._son_ihlal
        ended = False

        if self.ihlal:
            if self._violation_start_time is not None:
                gecen = time.time() - self._violation_start_time
                self._total_violation_seconds += gecen
                self._violation_start_time = None

            if self._active_violation_exe:
                self.finish_current_episode()

            ended = True

        self.ihlal = False
        self._son_ihlal = ""

        return {
            "ended": ended,
            "last_violation": last_violation,
        }

    def finish_current_episode(self):
        entry = build_violation_entry(
            self._active_violation_exe,
            self._active_violation_start,
        )

        if entry:
            self._violation_log.append(entry)

        self._active_violation_exe = ""
        self._active_violation_start = None
        return entry

    def stop_monitoring_and_save(self):
        if self._monitoring_start_time is None:
            return None

        session_start = self._monitoring_start_time
        self._total_monitoring_seconds = time.time() - session_start

        if self.ihlal and self._violation_start_time is not None:
            gecen = time.time() - self._violation_start_time
            self._total_violation_seconds += gecen
            self._violation_start_time = None

        if self._active_violation_exe:
            self.finish_current_episode()

        total_seconds = int(round(self._total_monitoring_seconds))
        violation_seconds = int(round(self._total_violation_seconds))

        db_ok = None
        db_msg = "[DB] db_manager yok, kayıt atlandı."

        if self.db_manager:
            db_ok, db_msg = self.db_manager.save_whitelist_session(
                user_id=self.user_id,
                violations=self._violation_log.copy(),
                total_duration=total_seconds,
                violation_duration=violation_seconds,
                total_duration_hms=format_seconds(total_seconds),
                violation_duration_hms=format_seconds(violation_seconds),
                session_started_at=(
                    datetime.fromtimestamp(session_start, tz=timezone.utc)
                    if session_start is not None else None
                ),
                session_ended_at=datetime.now(timezone.utc)
            )

        summary = {
            "db_ok": db_ok,
            "db_msg": db_msg,
            "total_hms": format_seconds(total_seconds),
            "violation_hms": format_seconds(violation_seconds),
            "record_count": len(self._violation_log),
        }

        self._monitoring_start_time = None
        self._violation_log.clear()
        self._active_violation_exe = ""
        self._active_violation_start = None

        return summary