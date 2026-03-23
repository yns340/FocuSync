# ui/whitelist_page.py
import sys
import time

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QListWidget, QMessageBox,
    QFrame, QCheckBox, QApplication
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont

try:
    import psutil
    import win32gui
    import win32process
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False
    print("[Whitelist] UYARI: Gerekli paketler eksik. Çalıştır: pip install pywin32 psutil")


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
}

SELF_EXES = {
    "focusync.exe",
    "code.exe",
    "pycharm64.exe",
    
}


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

        # Süre takibi
        self._monitoring_start_time: float | None = None
        self._violation_start_time: float | None = None
        self._total_monitoring_seconds: float = 0.0
        self._total_violation_seconds: float = 0.0

        self._build_ui()

        app = QApplication.instance()
        if app:
            app.aboutToQuit.connect(self._cleanup)

        print("[WhitelistPage] Yüklendi. DB read/write devre dışı.")
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
            "Örnek girişler: chrome.exe, code.exe, spotify.exe, pycharm64.exe"
        )
        desc.setStyleSheet("color:#6b7280; font-size:12px;")
        desc.setWordWrap(True)
        root.addWidget(desc)

        add_row = QHBoxLayout()
        self._input = QLineEdit()
        self._input.setPlaceholderText("İzin verilen exe adı (örn: chrome.exe)")
        self._input.setFixedHeight(36)
        self._input.returnPressed.connect(self._ekle)

        ekle_btn = QPushButton("Ekle")
        ekle_btn.setFixedSize(80, 36)
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
        self._list_widget.setFixedHeight(160)
        self._list_widget.setStyleSheet(
            "QListWidget { background:#111318; border:1px solid #1e2130; border-radius:8px; padding:6px; }"
            "QListWidget::item { padding:6px 8px; border-radius:4px; }"
            "QListWidget::item:selected { background:#1e2130; }"
        )
        root.addWidget(self._list_widget)

        sil_btn = QPushButton("Seçili Girişi Kaldır")
        sil_btn.setFixedWidth(180)
        sil_btn.clicked.connect(self._sil)
        root.addWidget(sil_btn, alignment=Qt.AlignmentFlag.AlignLeft)

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

    def _ekle(self):
        text = self._input.text().strip().lower()

        if not text:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir exe adı gir.")
            return

        if not text.endswith(".exe"):
            QMessageBox.warning(self, "Uyarı", "Lütfen .exe uzantısıyla gir. Örn: chrome.exe")
            return

        if text in self._whitelist:
            QMessageBox.information(self, "Bilgi", "Bu uygulama zaten listede.")
            return

        self._whitelist.add(text)
        self._listeyi_yenile()
        self._input.clear()
        print(f"[Whitelist] Eklendi: {text}")

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

            self._worker = MonitorWorker(self._get_whitelist, 10_000, self)
            self._worker.violation_found.connect(self._ihlal_isle)
            self._worker.no_violation.connect(self._ihlal_yok)
            self._worker.start()

            self._aktif_lbl.setText("İzleme: Açık")
            self._aktif_lbl.setStyleSheet("color:#00e5a0; font-size:11px;")
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

    def _ihlal_yok(self):
        if self.ihlal:
            if self._violation_start_time is not None:
                gecen = time.time() - self._violation_start_time
                self._total_violation_seconds += gecen
                self._violation_start_time = None

            print(f"[İHLAL BİTTİ] Son ihlal: {self._son_ihlal}")

        self.ihlal = False
        self._son_ihlal = ""

        self._ihlal_lbl.setText("İhlal: Yok ✓")
        self._ihlal_lbl.setStyleSheet("color:#00e5a0; font-size:13px; font-weight:700;")
        self._detay_lbl.setText("Tespit edilen uygulama: —")

    def _monitoring_bitisini_isle(self):
        if self._monitoring_start_time is not None:
            self._total_monitoring_seconds = time.time() - self._monitoring_start_time

        if self.ihlal and self._violation_start_time is not None:
            gecen = time.time() - self._violation_start_time
            self._total_violation_seconds += gecen
            self._violation_start_time = None

        if self._monitoring_start_time is not None:
            print(
                "[Whitelist ÖZET] "
                f"Toplam izleme süresi: {self._format_seconds(self._total_monitoring_seconds)} | "
                f"Toplam ihlal süresi: {self._format_seconds(self._total_violation_seconds)}"
            )

        self._monitoring_start_time = None

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
    page.resize(760, 560)
    page.show()
    sys.exit(app.exec())