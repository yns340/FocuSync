# ui/whitelist_page.py
import os
import re
import sys
import time

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QListWidget, QMessageBox,
    QFrame, QCheckBox, QApplication, QFileDialog,
    QDialog, QListWidgetItem
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QShortcut, QKeySequence

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
    print("[Whitelist] UYARI: Gerekli paketler eksik. Çalıştır: pip install pywin32 psutil")

from datetime import datetime, timezone

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
    "python.exe",  # focusync python ile çalıştığında aktif pencereyi tanımak için
}

BAD_EXE_HINTS = (
    "unins", "uninstall", "updater", "update", "setup",
    "install", "repair", "helper", "crash", "service"
)


def _get_active_window_info() -> tuple[str, str]:
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


def _iter_installed_apps() -> list[dict]:
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


class InstalledAppsDialog(QDialog):
    def __init__(self, apps: list[dict], parent=None):
        super().__init__(parent)
        self.setWindowTitle("Kurulu Uygulamalardan Ekle")
        self.resize(700, 520)

        self._all_apps = apps
        self._selected_app: dict | None = None

        root = QVBoxLayout(self)
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(12)

        info = QLabel(
            "Arama kutusuna uygulama adı veya exe adı yaz.\n"
            "Örnek: chrome, spotify, code, pycharm"
        )
        info.setStyleSheet("color:#6b7280; font-size:12px;")
        info.setWordWrap(True)
        root.addWidget(info)

        self._search = QLineEdit()
        self._search.setPlaceholderText("Ara: chrome, spotify, code...")
        self._search.setFixedHeight(36)
        self._search.textChanged.connect(self._refresh_list)
        root.addWidget(self._search)

        self._count_lbl = QLabel("")
        self._count_lbl.setStyleSheet("color:#6b7280; font-size:11px;")
        root.addWidget(self._count_lbl)

        self._list = QListWidget()
        self._list.setStyleSheet(
            "QListWidget { background:#111318; border:1px solid #1e2130; border-radius:8px; padding:6px; }"
            "QListWidget::item { padding:8px 10px; border-radius:4px; }"
            "QListWidget::item:selected { background:#1e2130; }"
        )
        self._list.itemDoubleClicked.connect(self._handle_double_click)
        root.addWidget(self._list)

        btn_row = QHBoxLayout()
        btn_row.addStretch()

        self._select_btn = QPushButton("Seçili Uygulamayı Ekle")
        self._select_btn.setFixedHeight(36)
        self._select_btn.clicked.connect(self._select_current)
        btn_row.addWidget(self._select_btn)

        cancel_btn = QPushButton("İptal")
        cancel_btn.setFixedHeight(36)
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(cancel_btn)

        root.addLayout(btn_row)
        self._refresh_list()

    def _refresh_list(self):
        query = self._search.text().strip().lower()
        parts = [p for p in query.split() if p]

        self._list.clear()
        shown = 0

        for app in self._all_apps:
            haystack = " ".join([
                app.get("display_name", ""),
                app.get("exe_name", ""),
                app.get("publisher", ""),
                app.get("exe_path", ""),
            ]).lower()

            if parts and not all(part in haystack for part in parts):
                continue

            item_text = f"{app['display_name']}  •  {app['exe_name']}"
            item = QListWidgetItem(item_text)

            tooltip = app["exe_path"]
            if app.get("publisher"):
                tooltip += f"\nYayıncı: {app['publisher']}"

            item.setToolTip(tooltip)
            item.setData(Qt.ItemDataRole.UserRole, app)
            self._list.addItem(item)
            shown += 1

        self._count_lbl.setText(f"Gösterilen uygulama sayısı: {shown}")

        if shown > 0:
            self._list.setCurrentRow(0)

    def _handle_double_click(self, item: QListWidgetItem):
        self._selected_app = item.data(Qt.ItemDataRole.UserRole)
        self.accept()

    def _select_current(self):
        item = self._list.currentItem()
        if not item:
            QMessageBox.warning(self, "Uyarı", "Lütfen listeden bir uygulama seç.")
            return

        self._selected_app = item.data(Qt.ItemDataRole.UserRole)
        self.accept()

    def selected_app(self) -> dict | None:
        return self._selected_app


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

            if not whitelist:
                self._emit_ok_if_changed()
            else:
                exe_name, window_title = _get_active_window_info()
                window_title_lower = window_title.lower().strip() if window_title else ""

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


class WhitelistPage(QWidget):
    def __init__(self, user_id, db_manager, parent=None):
        super().__init__(parent)

        self.user_id = user_id
        self.db_manager = db_manager

        self._whitelist: set[str] = set()
        self.ihlal: bool = False
        self._son_ihlal = ""
        self._worker: MonitorWorker | None = None

        self._last_violation_exe: str | None = None
        self._last_violation_detay: str = ""

        # Seans içi episode logu
        self._violation_log: list[dict] = []
        self._active_violation_exe: str = ""
        self._active_violation_start: float | None = None

        # Süre takibi
        self._monitoring_start_time: float | None = None
        self._violation_start_time: float | None = None
        self._total_monitoring_seconds: float = 0.0
        self._total_violation_seconds: float = 0.0

        self._build_ui()
        self._update_allow_last_controls()

        app = QApplication.instance()
        if app:
            app.aboutToQuit.connect(self._cleanup)

        print("[WhitelistPage] Yüklendi.")
        if not WIN32_AVAILABLE:
            print("[WhitelistPage] pywin32 / psutil eksik, izleme çalışmayacak.")

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(28, 24, 28, 24)
        root.setSpacing(16)

        title = QLabel("Beyaz Liste & Denetim")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        root.addWidget(title)

        desc = QLabel(
            "Listeye eklediğin .exe adları dışındaki aktif kullanıcı uygulamaları ihlal sayılır.\n"
            "Sistem uygulamaları otomatik olarak izinli kabul edilir.\n"
            "Uygulama eklemek için kurulu uygulama listesi, dosya seçimi veya son ihlale hızlı izin verme kullanılabilir."
        )
        desc.setStyleSheet("color:#6b7280; font-size:12px;")
        desc.setWordWrap(True)
        root.addWidget(desc)

        action_row = QHBoxLayout()

        self._installed_apps_btn = QPushButton("Kurulu Uygulamalardan Ekle")
        self._installed_apps_btn.setFixedHeight(36)
        self._installed_apps_btn.clicked.connect(self._kurulu_uygulamalardan_ekle)
        action_row.addWidget(self._installed_apps_btn)

        self._browse_exe_btn = QPushButton("Dosyadan .exe Seç")
        self._browse_exe_btn.setFixedHeight(36)
        self._browse_exe_btn.clicked.connect(self._dosyadan_exe_sec)
        action_row.addWidget(self._browse_exe_btn)

        root.addLayout(action_row)

        add_row = QHBoxLayout()
        self._input = QLineEdit()
        self._input.setPlaceholderText("Manuel exe adı gir (örn: chrome.exe)")
        self._input.setFixedHeight(36)
        self._input.returnPressed.connect(self._ekle)

        ekle_btn = QPushButton("Elle Ekle")
        ekle_btn.setFixedHeight(36)
        ekle_btn.clicked.connect(self._ekle)

        add_row.addWidget(self._input)
        add_row.addWidget(ekle_btn)
        root.addLayout(add_row)

        liste_label = QLabel("İZİN VERİLEN UYGULAMALAR")
        liste_label.setStyleSheet(
            "color:#6b7280; font-size:10px; font-weight:700; letter-spacing:0.8px;"
        )
        root.addWidget(liste_label)

        self._list_widget = QListWidget()
        self._list_widget.setFixedHeight(180)
        self._list_widget.setStyleSheet(
            "QListWidget {"
            " background:#111318;"
            " color:#f3f4f6;"
            " border:1px solid #1e2130;"
            " border-radius:8px;"
            " padding:6px;"
            " outline:0;"
            "}"
            "QListWidget::item {"
            " padding:8px 10px;"
            " border-radius:6px;"
            " color:#f3f4f6;"
            "}"
            "QListWidget::item:hover {"
            " background:#1a1f2b;"
            "}"
            "QListWidget::item:selected {"
            " background:#757173;"
            " color:#a6ff00;"
            " font-weight:600;"
            "}"
        )
        root.addWidget(self._list_widget)

        list_btn_row = QHBoxLayout()

        sil_btn = QPushButton("Seçili Girişi Kaldır")
        sil_btn.setFixedWidth(180)
        sil_btn.clicked.connect(self._sil)
        list_btn_row.addWidget(sil_btn)

        self._allow_last_btn = QPushButton("Son İhlale İzin Ver (Ctrl+Shift+A)")
        self._allow_last_btn.setFixedHeight(36)
        self._allow_last_btn.clicked.connect(self._son_ihlale_izin_ver)
        list_btn_row.addWidget(self._allow_last_btn)

        list_btn_row.addStretch()
        root.addLayout(list_btn_row)

        self._allow_last_hint = QLabel(
            "Hızlı işlem: Son ihlali whitelist'e eklemek için Ctrl+Shift+A kullanılabilir."
        )
        self._allow_last_hint.setStyleSheet("color:#6b7280; font-size:11px;")
        self._allow_last_hint.setWordWrap(True)
        root.addWidget(self._allow_last_hint)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("color:#1e2130;")
        root.addWidget(sep)

        self._izleme_cb = QCheckBox("Aktif uygulama izlemesini başlat (10 sn aralıklı)")
        self._izleme_cb.setStyleSheet("font-size:13px;")
        self._izleme_cb.stateChanged.connect(self._izleme_toggle)
        root.addWidget(self._izleme_cb)

        durum_frame = QFrame()
        durum_frame.setStyleSheet(
            "background:#111318; border:1px solid #1e2130; border-radius:10px;"
        )
        durum_lay = QVBoxLayout(durum_frame)
        durum_lay.setContentsMargins(16, 12, 16, 12)
        durum_lay.setSpacing(6)

        self._ihlal_lbl = QLabel("İhlal: —")
        self._ihlal_lbl.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        durum_lay.addWidget(self._ihlal_lbl)

        self._detay_lbl = QLabel("Tespit edilen uygulama: —")
        self._detay_lbl.setStyleSheet("color:#6b7280; font-size:11px;")
        self._detay_lbl.setWordWrap(True)
        durum_lay.addWidget(self._detay_lbl)

        self._aktif_lbl = QLabel("İzleme: Kapalı")
        self._aktif_lbl.setStyleSheet("color:#6b7280; font-size:11px;")
        durum_lay.addWidget(self._aktif_lbl)

        root.addWidget(durum_frame)
        root.addStretch()

        self._allow_last_shortcut = QShortcut(QKeySequence("Ctrl+Shift+A"), self)
        self._allow_last_shortcut.setContext(Qt.ShortcutContext.WindowShortcut)
        self._allow_last_shortcut.activated.connect(self._son_ihlale_izin_ver)

    def _normalize_exe_name(self, text: str) -> str:
        text = (text or "").strip().strip('"').strip("'")
        text = os.path.basename(text)
        return text.lower().strip()

    def _current_violation_exe(self) -> str:
        if not self._son_ihlal:
            return ""
        return self._son_ihlal.split(" | ", 1)[0].strip().lower()

    def _update_allow_last_controls(self):
        aktif = bool(self._last_violation_exe)
        self._allow_last_btn.setEnabled(aktif)
        self._allow_last_shortcut.setEnabled(aktif)

        if aktif:
            self._allow_last_btn.setText(
                f"Son İhlale İzin Ver: {self._last_violation_exe} (Ctrl+Shift+A)"
            )
        else:
            self._allow_last_btn.setText("Son İhlale İzin Ver (Ctrl+Shift+A)")

    def _clear_last_violation(self):
        self._last_violation_exe = None
        self._last_violation_detay = ""
        self._update_allow_last_controls()

    def _add_exe_to_whitelist(self, exe_name: str, silent: bool = False) -> bool:
        exe_name = self._normalize_exe_name(exe_name)

        if not exe_name:
            if not silent:
                QMessageBox.warning(self, "Uyarı", "Geçerli bir exe adı bulunamadı.")
            return False

        if not exe_name.endswith(".exe"):
            if not silent:
                QMessageBox.warning(self, "Uyarı", "Lütfen .exe uzantılı bir uygulama seç.")
            return False

        if exe_name in self._whitelist:
            if not silent:
                QMessageBox.information(self, "Bilgi", f"{exe_name} zaten whitelist içinde.")
            return False

        self._whitelist.add(exe_name)
        self._listeyi_yenile()
        print(f"[Whitelist] Eklendi: {exe_name}")

        if self._last_violation_exe == exe_name:
            if self.ihlal and self._current_violation_exe() == exe_name:
                self._ihlal_yok()
            self._clear_last_violation()

        return True

    def _ekle(self):
        text = self._input.text().strip().lower()
        if self._add_exe_to_whitelist(text):
            self._input.clear()

    def _kurulu_uygulamalardan_ekle(self):
        if os.name != "nt":
            QMessageBox.warning(self, "Desteklenmiyor", "Bu özellik yalnızca Windows'ta kullanılabilir.")
            return

        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        try:
            apps = _iter_installed_apps()
        finally:
            QApplication.restoreOverrideCursor()

        if not apps:
            QMessageBox.information(
                self,
                "Bilgi",
                "Kurulu uygulama listesi alınamadı veya uygun exe bulunamadı.\n"
                "İstersen 'Dosyadan .exe Seç' seçeneğini kullanabilirsin."
            )
            return

        dialog = InstalledAppsDialog(apps, self)
        if dialog.exec():
            selected = dialog.selected_app()
            if not selected:
                return

            exe_name = selected.get("exe_name", "").strip().lower()
            self._add_exe_to_whitelist(exe_name)

    def _dosyadan_exe_sec(self):
        default_dir = os.environ.get("ProgramFiles", os.path.expanduser("~"))

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "İzin Verilecek Uygulamayı Seç",
            default_dir,
            "Executable Files (*.exe);;All Files (*)",
        )

        if not file_path:
            return

        exe_name = os.path.basename(file_path).lower().strip()
        self._add_exe_to_whitelist(exe_name)

    def _son_ihlale_izin_ver(self):
        exe_name = (self._last_violation_exe or "").strip().lower()

        if not exe_name:
            QMessageBox.information(self, "Bilgi", "İzin verilecek son ihlal bulunmuyor.")
            return

        if exe_name in SYSTEM_EXES:
            QMessageBox.information(self, "Bilgi", f"{exe_name} zaten sistem uygulaması olarak izinli.")
            self._clear_last_violation()
            return

        if exe_name in SELF_EXES:
            QMessageBox.information(self, "Bilgi", f"{exe_name} zaten uygulama tarafından izinli.")
            self._clear_last_violation()
            return

        if exe_name in self._whitelist:
            QMessageBox.information(self, "Bilgi", f"{exe_name} zaten whitelist içinde.")
            self._clear_last_violation()
            return

        basarili = self._add_exe_to_whitelist(exe_name, silent=True)
        if basarili:
            print(f"[Whitelist] Son ihlale hızlı izin verildi: {exe_name}")

    def _sil(self):
        item = self._list_widget.currentItem()
        if not item:
            QMessageBox.warning(self, "Uyarı", "Lütfen listeden bir giriş seç.")
            return

        text = item.text().strip().lower()
        self._whitelist.discard(text)
        self._listeyi_yenile()
        print(f"[Whitelist] Silindi: {text}")

    def _listeyi_yenile(self):
        self._list_widget.clear()
        for app in sorted(self._whitelist):
            self._list_widget.addItem(app)

    def _get_whitelist(self):
        return set(self._whitelist)

    def _izleme_toggle(self, state):
        if state == Qt.CheckState.Checked.value:
            if not WIN32_AVAILABLE:
                QMessageBox.warning(
                    self,
                    "Eksik Paket",
                    "Aktif pencere izlemesi için 'pywin32' ve 'psutil' gerekli."
                )
                self._izleme_cb.setChecked(False)
                return

            if self._worker and self._worker.isRunning():
                return

            self._monitoring_start_time = time.time()
            self._violation_start_time = None
            self._total_monitoring_seconds = 0.0
            self._total_violation_seconds = 0.0
            self.ihlal = False
            self._son_ihlal = ""

            self._violation_log = []
            self._active_violation_exe = ""
            self._active_violation_start = None

            self._clear_last_violation()

            self._worker = MonitorWorker(self._get_whitelist, 10_000, self)
            self._worker.violation_found.connect(self._ihlal_isle)
            self._worker.no_violation.connect(self._ihlal_yok)
            self._worker.start()

            self._aktif_lbl.setText("İzleme: Açık")
            self._aktif_lbl.setStyleSheet("color:#00e5a0; font-size:11px;")
            self._ihlal_lbl.setText("İhlal: —")
            self._ihlal_lbl.setStyleSheet("")
            self._detay_lbl.setText("Tespit edilen uygulama: —")

            print("[Whitelist] İzleme başlatıldı (10 sn aralıklı, exe modu).")

        else:
            self._monitoring_bitisini_isle()

            if self._worker:
                self._worker.stop()
                self._worker = None

            self._aktif_lbl.setText("İzleme: Kapalı")
            self._aktif_lbl.setStyleSheet("color:#6b7280; font-size:11px;")
            print("[Whitelist] İzleme durduruldu.")

    def _ihlal_isle(self, detay: str):
        exe_name = detay.split(" | ", 1)[0].strip().lower() if detay else ""

        if exe_name and exe_name.endswith(".exe"):
            self._last_violation_exe = exe_name
            self._last_violation_detay = detay
            self._update_allow_last_controls()

        # Farklı exe'ye geçildiyse önceki episode'u kapat
        if self._active_violation_exe and self._active_violation_exe != exe_name:
            self._episode_kapat()

        # Yeni episode başlat
        if exe_name and self._active_violation_exe != exe_name:
            self._active_violation_exe = exe_name
            self._active_violation_start = time.time()

        if not self.ihlal:
            self.ihlal = True
            self._son_ihlal = detay
            self._violation_start_time = time.time()

            self._ihlal_lbl.setText("İhlal: EVET ⚠")
            self._ihlal_lbl.setStyleSheet("color:#ff6b35; font-size:13px; font-weight:700;")
            self._detay_lbl.setText(f"Tespit edilen uygulama: {detay}")

            print(f"[İHLAL BAŞLADI] {detay}")

        else:
            self._son_ihlal = detay
            self._detay_lbl.setText(f"Tespit edilen uygulama: {detay}")

    def _episode_kapat(self):
        if not self._active_violation_exe or self._active_violation_start is None:
            return

        end_time = time.time()
        sure = end_time - self._active_violation_start

        if sure >= 1.0:
            duration_seconds = int(round(sure))
            self._violation_log.append({
                "app_name": self._active_violation_exe,
                "duration_seconds": duration_seconds,
                "duration_hms": self._format_seconds(duration_seconds),
                "started_at": datetime.fromtimestamp(self._active_violation_start, tz=timezone.utc),
                "ended_at": datetime.fromtimestamp(end_time, tz=timezone.utc),
            })

        self._active_violation_exe = ""
        self._active_violation_start = None

    def _ihlalleri_db_ye_kaydet(self):
        if not self.db_manager:
            print("[DB] db_manager yok, kayıt atlandı.")
            return

        total_seconds = int(round(self._total_monitoring_seconds))
        violation_seconds = int(round(self._total_violation_seconds))

        ok, msg = self.db_manager.save_whitelist_session(
            user_id=self.user_id,
            violations=self._violation_log.copy(),
            total_duration=total_seconds,
            violation_duration=violation_seconds,
            total_duration_hms=self._format_seconds(total_seconds),
            violation_duration_hms=self._format_seconds(violation_seconds),
            session_started_at=(
                datetime.fromtimestamp(self._monitoring_start_time, tz=timezone.utc)
                if self._monitoring_start_time is not None else None
            ),
            session_ended_at=datetime.now(timezone.utc)
        )
        print(f"[DB] {'✓' if ok else '✗'} {msg}")

    def _ihlal_yok(self):
        if self.ihlal:
            if self._violation_start_time is not None:
                gecen = time.time() - self._violation_start_time
                self._total_violation_seconds += gecen
                self._violation_start_time = None

            if self._active_violation_exe:
                self._episode_kapat()

            print(f"[İHLAL BİTTİ] Son ihlal: {self._son_ihlal}")

        self.ihlal = False
        self._son_ihlal = ""

        self._ihlal_lbl.setText("İhlal: Yok ✓")
        self._ihlal_lbl.setStyleSheet("color:#00e5a0; font-size:13px; font-weight:700;")
        self._detay_lbl.setText("Tespit edilen uygulama: —")

    def _monitoring_bitisini_isle(self):
        if self._monitoring_start_time is None:
            return  # ikinci kez kaydetmeyi önler

        self._total_monitoring_seconds = time.time() - self._monitoring_start_time

        if self.ihlal and self._violation_start_time is not None:
            gecen = time.time() - self._violation_start_time
            self._total_violation_seconds += gecen
            self._violation_start_time = None

        if self._active_violation_exe:
            self._episode_kapat()

        self._ihlalleri_db_ye_kaydet()

        print(
            "[Whitelist ÖZET] "
            f"Toplam izleme: {self._format_seconds(self._total_monitoring_seconds)} | "
            f"Toplam ihlal: {self._format_seconds(self._total_violation_seconds)} | "
            f"Kayıt sayısı: {len(self._violation_log)}"
        )

        self._monitoring_start_time = None
        self._violation_log.clear()
        self._active_violation_exe = ""
        self._active_violation_start = None

    @staticmethod
    def _format_seconds(seconds: float) -> str:
        total = int(round(seconds))
        saat = total // 3600
        dakika = (total % 3600) // 60
        saniye = total % 60
        return f"{saat:02d}:{dakika:02d}:{saniye:02d}"

    def _cleanup(self):
        self._monitoring_bitisini_isle()

        if self._worker:
            self._worker.stop()
            self._worker = None

    def closeEvent(self, event):
        self._cleanup()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    page = WhitelistPage("test_user", None)
    page.resize(860, 680)
    page.show()
    sys.exit(app.exec())