import os
import re
import time
import sys
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
    "snippingtool.exe",
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
if sys.platform == "darwin":
    try:
        from AppKit import NSWorkspace
    except ImportError:
        NSWorkspace = None
else:
    NSWorkspace = None

def get_default_id_type() -> str:
    platform_name = get_runtime_platform()
    if platform_name == "windows":
        return "exe"
    if platform_name == "macos":
        return "bundle_id"
    if platform_name == "linux":
        return "desktop_id"
    return "unknown"


def monitoring_supported() -> bool:
    platform_name = get_runtime_platform()

    if platform_name == "windows":
        return WIN32_AVAILABLE
    if platform_name == "macos":
        return NSWorkspace is not None
    if platform_name == "linux":
        return False   # şimdilik hazır değil
    return False

def format_seconds(seconds: float) -> str:
    total = int(round(seconds))
    saat = total // 3600
    dakika = (total % 3600) // 60
    saniye = total % 60
    return f"{saat:02d}:{dakika:02d}:{saniye:02d}"

def get_runtime_platform() -> str:
    if sys.platform == "win32":
        return "windows"
    if sys.platform == "darwin":
        return "macos"
    if sys.platform.startswith("linux"):
        return "linux"
    return "unknown"

def normalize_app_id(text: str) -> str:
    text = (text or "").strip().strip('"').strip("'").lower()

    # Windows'ta yol geldiyse basename al
    if text.endswith(".exe") or "\\" in text or "/" in text:
        text = os.path.basename(text)

    return text.strip()


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


def get_active_app_identity() -> dict:
    platform_name = get_runtime_platform()

    if platform_name == "windows":
        return _get_active_app_identity_windows()
    if platform_name == "macos":
        return _get_active_app_identity_macos()
    if platform_name == "linux":
        return _get_active_app_identity_linux()

    return {
        "platform": "unknown",
        "id_type": "unknown",
        "app_id": "",
        "app_display_name": "",
        "window_title": "",
    }


def _get_active_app_identity_windows() -> dict:
    if not WIN32_AVAILABLE:
        return {
            "platform": "windows",
            "id_type": "exe",
            "app_id": "",
            "app_display_name": "",
            "window_title": "",
        }

    try:
        hwnd = win32gui.GetForegroundWindow()
        if not hwnd:
            return {
                "platform": "windows",
                "id_type": "exe",
                "app_id": "",
                "app_display_name": "",
                "window_title": "",
            }

        title = win32gui.GetWindowText(hwnd).strip()
        _, pid = win32process.GetWindowThreadProcessId(hwnd)

        if not pid:
            return {
                "platform": "windows",
                "id_type": "exe",
                "app_id": "",
                "app_display_name": "",
                "window_title": title,
            }

        proc = psutil.Process(pid)
        exe_name = proc.name().lower().strip()

        return {
            "platform": "windows",
            "id_type": "exe",
            "app_id": exe_name,
            "app_display_name": exe_name,
            "window_title": title,
        }

    except Exception as e:
        print(f"[Whitelist] Aktif pencere bilgisi alınamadı: {e}")
        return {
            "platform": "windows",
            "id_type": "exe",
            "app_id": "",
            "app_display_name": "",
            "window_title": "",
        }


def _get_active_app_identity_macos() -> dict:
    if NSWorkspace is None:
        return {
            "platform": "macos",
            "id_type": "bundle_id",
            "app_id": "",
            "app_display_name": "",
            "window_title": "",
        }

    try:
        app = NSWorkspace.sharedWorkspace().frontmostApplication()
        bundle_id = str(app.bundleIdentifier() or "").strip() if app else ""
        app_name = str(app.localizedName() or "").strip() if app else ""

        return {
            "platform": "macos",
            "id_type": "bundle_id",
            "app_id": bundle_id.lower(),
            "app_display_name": app_name or bundle_id,
            "window_title": app_name,
        }
    except Exception as e:
        print(f"[Whitelist] macOS aktif uygulama alınamadı: {e}")
        return {
            "platform": "macos",
            "id_type": "bundle_id",
            "app_id": "",
            "app_display_name": "",
            "window_title": "",
        }


def _get_active_app_identity_linux() -> dict:
    return {
        "platform": "linux",
        "id_type": "desktop_id",
        "app_id": "",
        "app_display_name": "",
        "window_title": "",
    }

def format_identity_for_ui(item: dict) -> str:
    label = item.get("app_display_name") or item.get("app_id") or "unknown"
    platform_name = item.get("platform", "unknown")
    id_type = item.get("id_type", "unknown")
    app_id = item.get("app_id", "")
    return f"{label}  [{platform_name}:{id_type}]  {app_id}"


def is_allowed_app(active_app: dict, whitelist: list[dict]) -> bool:
    for item in whitelist:
        if (
            item.get("platform") == active_app.get("platform")
            and item.get("id_type") == active_app.get("id_type")
            and item.get("app_id") == active_app.get("app_id")
        ):
            return True
    return False
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


def build_violation_entry(active_app: dict, active_start: float | None):
    if not active_app or active_start is None:
        return None

    end_time = time.time()
    sure = end_time - active_start

    if sure < 1.0:
        return None

    duration_seconds = int(round(sure))
    return {
        "platform": active_app.get("platform", get_runtime_platform()),
        "id_type": active_app.get("id_type", get_default_id_type()),
        "app_id": active_app.get("app_id", ""),
        "app_display_name": active_app.get("app_display_name", active_app.get("app_id", "")),
        "window_title": active_app.get("window_title", ""),
        "duration_seconds": duration_seconds,
        "duration_hms": format_seconds(duration_seconds),
        "started_at": datetime.fromtimestamp(active_start, tz=timezone.utc),
        "ended_at": datetime.fromtimestamp(end_time, tz=timezone.utc),
    }


class MonitorWorker(QThread):
    violation_found = pyqtSignal(dict)
    no_violation = pyqtSignal()

    def __init__(self, get_whitelist_fn, interval_ms: int = 10_000, parent=None):
        super().__init__(parent)
        self._get_whitelist = get_whitelist_fn
        self.interval_ms = interval_ms
        self._running = False
        self._last_state = None  # "ok" veya ihlal detay string'i
        self._last_fg_debug = None

    def _emit_ok_if_changed(self):
        if self._last_state != "ok":
            self._last_state = "ok"
            self.no_violation.emit()

    def _emit_violation_if_changed(self, violation_payload: dict):
        detail_text = violation_payload.get("detail_text", "")
        if self._last_state != detail_text:
            self._last_state = detail_text
            self.violation_found.emit(violation_payload)

    def run(self):
        self._running = True

        while self._running:
            whitelist = self._get_whitelist()
            active_app = get_active_app_identity()

            app_id = active_app.get("app_id", "")
            window_title = active_app.get("window_title", "")
            window_title_lower = window_title.lower().strip() if window_title else ""

            current_fg = (
                active_app.get("platform"),
                active_app.get("id_type"),
                app_id,
                window_title,
            )

            if (app_id or window_title) and current_fg != self._last_fg_debug:
                print(
                    f"[FG DEBUG] platform={active_app.get('platform')!r} | "
                    f"id_type={active_app.get('id_type')!r} | "
                    f"app_id={app_id!r} | title={window_title!r}"
                )
                self._last_fg_debug = current_fg

            if not app_id:
                self._emit_ok_if_changed()

            elif active_app.get("platform") == "windows" and app_id in SYSTEM_EXES:
                self._emit_ok_if_changed()

            elif active_app.get("platform") == "windows" and app_id in SELF_EXES:
                self._emit_ok_if_changed()

            elif active_app.get("platform") == "windows" and app_id == "python.exe" and "focusync" in window_title_lower:
                self._emit_ok_if_changed()

            else:
                izinli = is_allowed_app(active_app, whitelist)

                if izinli:
                    self._emit_ok_if_changed()
                else:
                    detail_text = (
                        f"{active_app.get('app_display_name') or app_id} | {window_title}"
                        if window_title else
                        (active_app.get("app_display_name") or app_id)
                    )

                    payload = {
                        **active_app,
                        "detail_text": detail_text,
                    }
                    self._emit_violation_if_changed(payload)

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
        

        self._whitelist: list[dict] = []
        self.ihlal: bool = False
        self._son_ihlal = ""

        self._last_violation_exe: str | None = None
        self._last_violation_detay: str = ""

        self._violation_log: list[dict] = []
        self._active_violation_app: dict | None = None
        self._active_violation_start: float | None = None

        self._monitoring_start_time: float | None = None
        self._violation_start_time: float | None = None
        self._total_monitoring_seconds: float = 0.0
        self._total_violation_seconds: float = 0.0

    def get_whitelist(self):
        return list(self._whitelist)

    def whitelist_items(self):
        return [format_identity_for_ui(item) for item in self._whitelist]

    def has_last_violation(self) -> bool:
        return bool(self._last_violation_exe)

    def clear_last_violation(self):
        self._last_violation_exe = None
        self._last_violation_detay = ""

    def current_violation_app_id(self) -> str:
        if self._active_violation_app:
            return (self._active_violation_app.get("app_id") or "").strip().lower()
        return (self._last_violation_exe or "").strip().lower()

    def start_monitoring(self):
        self._monitoring_start_time = time.time()
        self._violation_start_time = None
        self._total_monitoring_seconds = 0.0
        self._total_violation_seconds = 0.0
        self.ihlal = False
        self._son_ihlal = ""

        self._violation_log = []
        self._active_violation_app = None
        self._active_violation_start = None

        self.clear_last_violation()

    def add_app_to_whitelist(
        self,
        app_id: str,
        platform_name: str | None = None,
        id_type: str | None = None,
        app_display_name: str | None = None
    ):
        app_id = normalize_app_id(app_id)
        platform_name = platform_name or get_runtime_platform()
        id_type = id_type or get_default_id_type()
        app_display_name = app_display_name or app_id

        if not app_id:
            return {
                "ok": False,
                "level": "warning",
                "msg": "Geçerli bir uygulama kimliği bulunamadı.",
                "app_id": "",
                "clear_info": None,
            }

        for item in self._whitelist:
            if (
                item.get("platform") == platform_name
                and item.get("id_type") == id_type
                and item.get("app_id") == app_id
            ):
                return {
                    "ok": False,
                    "level": "info",
                    "msg": f"{app_id} zaten whitelist içinde.",
                    "app_id": app_id,
                    "clear_info": None,
                }

        self._whitelist.append({
            "platform": platform_name,
            "id_type": id_type,
            "app_id": app_id,
            "app_display_name": app_display_name,
        })

        clear_info = None
        if self._last_violation_exe == app_id:
            if self.ihlal and self.current_violation_app_id() == app_id:
                clear_info = self.process_no_violation()
            self.clear_last_violation()

        return {
            "ok": True,
            "level": "success",
            "msg": f"{app_display_name} whitelist'e eklendi.",
            "app_id": app_id,
            "clear_info": clear_info,
        }
    
    def remove_app_from_whitelist(self, app_item: dict):
        if not app_item:
            return False

        before = len(self._whitelist)
        self._whitelist = [
            item for item in self._whitelist
            if not (
                item.get("platform") == app_item.get("platform")
                and item.get("id_type") == app_item.get("id_type")
                and item.get("app_id") == app_item.get("app_id")
            )
        ]
        return len(self._whitelist) < before

    

    def allow_last_violation(self):
        app_id = (self._last_violation_exe or "").strip().lower()

        if not app_id:
            return {
                "ok": False,
                "level": "info",
                "msg": "İzin verilecek son ihlal bulunmuyor.",
                "app_id": "",
                "clear_info": None,
            }

        platform_name = get_runtime_platform()
        id_type = get_default_id_type()

        if platform_name == "windows" and app_id in SYSTEM_EXES:
            self.clear_last_violation()
            return {
                "ok": False,
                "level": "info",
                "msg": f"{app_id} zaten sistem uygulaması olarak izinli.",
                "app_id": app_id,
                "clear_info": None,
            }

        if platform_name == "windows" and app_id in SELF_EXES:
            self.clear_last_violation()
            return {
                "ok": False,
                "level": "info",
                "msg": f"{app_id} zaten uygulama tarafından izinli.",
                "app_id": app_id,
                "clear_info": None,
            }

        for item in self._whitelist:
            if (
                item.get("platform") == platform_name
                and item.get("id_type") == id_type
                and item.get("app_id") == app_id
            ):
                self.clear_last_violation()
                return {
                    "ok": False,
                    "level": "info",
                    "msg": f"{app_id} zaten whitelist içinde.",
                    "app_id": app_id,
                    "clear_info": None,
                }

        return self.add_app_to_whitelist(
            app_id=app_id,
            platform_name=platform_name,
            id_type=id_type,
            app_display_name=app_id
        )

    def process_violation(self, violation_payload: dict):
        app_id = violation_payload.get("app_id", "").strip().lower()
        detay = violation_payload.get("detail_text", "")

        if app_id:
            self._last_violation_exe = app_id
            self._last_violation_detay = detay

        if self._active_violation_app and self._active_violation_app.get("app_id") != app_id:
            self.finish_current_episode()

        if app_id and (
            self._active_violation_app is None
            or self._active_violation_app.get("app_id") != app_id
        ):
            self._active_violation_app = violation_payload
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
            "app_id": app_id,
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

            if self._active_violation_app:
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
            self._active_violation_app,
            self._active_violation_start,
        )

        if entry:
            self._violation_log.append(entry)

        self._active_violation_app = None
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

        if self._active_violation_app:
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
                session_ended_at=datetime.now(timezone.utc),
                session_platform=get_runtime_platform(),
                session_id_type=get_default_id_type()
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
        self._active_violation_app = None
        self._active_violation_start = None

        return summary