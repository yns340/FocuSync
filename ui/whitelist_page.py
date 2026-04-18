import os
import sys

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QListWidget, QMessageBox,
    QFrame, QApplication, QFileDialog,
    QDialog, QListWidgetItem, QDialogButtonBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QShortcut, QKeySequence

# Sadece Windows'ta çalışan winsound kütüphanesini Mac'te çökmemesi için güvenli içe aktarma
try:
    import winsound
except ImportError:
    # Mac ve Linux için sahte (dummy) bir winsound oluşturuyoruz ki kodun aşağısında hata vermesin
    class DummySound:
        def Beep(self, freq, duration): pass
        def PlaySound(self, sound, flags): pass
        def MessageBeep(self, kind=0): pass

        SND_ALIAS = 0
        SND_ASYNC = 0
        SND_FILENAME = 0
        SND_NODEFAULT = 0
        MB_ICONEXCLAMATION = 0
    winsound = DummySound()

try:
    from whitelist_functionality import (
        WIN32_AVAILABLE,
        iter_installed_apps,
        MonitorWorker,
        WhitelistLogic,
        get_runtime_platform,
        get_default_id_type,
        format_identity_for_ui,
        monitoring_supported,
    )
except ImportError:
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
    if PROJECT_ROOT not in sys.path:
        sys.path.insert(0, PROJECT_ROOT)

    from whitelist_functionality import (
        WIN32_AVAILABLE,
        iter_installed_apps,
        MonitorWorker,
        WhitelistLogic,
        get_runtime_platform,
        get_default_id_type,
        format_identity_for_ui,
        monitoring_supported,
    )


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

class ViolationAlertDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Whitelist İhlali")
        self.setModal(False)
        self.setWindowFlags(
            Qt.WindowType.Dialog
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.WindowTitleHint
            | Qt.WindowType.CustomizeWindowHint
            | Qt.WindowType.Tool
        )
        self.resize(420, 180)

        self.setStyleSheet("""
            QDialog {
                background: #111318;
                border: 1px solid #1e2130;
                border-radius: 12px;
            }
            QLabel#titleLabel {
                color: #ff6b35;
                font-size: 16px;
                font-weight: 700;
            }
            QLabel#detailLabel {
                color: #f3f4f6;
                font-size: 12px;
            }
            QPushButton {
                background: #1e2130;
                color: #f3f4f6;
                border: 1px solid #2a3042;
                border-radius: 8px;
                padding: 8px 14px;
            }
            QPushButton:hover {
                background: #2a3042;
            }
        """)

        root = QVBoxLayout(self)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(10)

        self._title_lbl = QLabel("Whitelist ihlali algılandı!")
        self._title_lbl.setObjectName("titleLabel")
        root.addWidget(self._title_lbl)

        self._detail_lbl = QLabel("Tespit edilen uygulama: —")
        self._detail_lbl.setObjectName("detailLabel")
        self._detail_lbl.setWordWrap(True)
        root.addWidget(self._detail_lbl)

        self._info_lbl = QLabel("İhlal yapan uygulama kapanırsa bu pencere otomatik kapanır.")
        self._info_lbl.setObjectName("detailLabel")
        self._info_lbl.setWordWrap(True)
        root.addWidget(self._info_lbl)

        root.addStretch()

        buttons = QDialogButtonBox(self)
        close_btn = buttons.addButton("Tamam", QDialogButtonBox.ButtonRole.AcceptRole)
        close_btn.clicked.connect(self.close)
        root.addWidget(buttons)

    def set_violation_text(self, detay: str):
        self._detail_lbl.setText(f"Tespit edilen uygulama: {detay}")
        
class WhitelistPage(QWidget):
    def __init__(self, user_id, db_manager, parent=None):
        super().__init__(parent)

        self.user_id = user_id
        self.db_manager = db_manager
        self.logic = WhitelistLogic(user_id, db_manager)

        self._worker: MonitorWorker | None = None

        self._build_ui()
        self._update_allow_last_controls()
        self._alert_dialog: ViolationAlertDialog | None = None
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self._alert_sound_path = os.path.join(
            project_root,
            "assets",
            "sounds",
            "whitelist_alert.wav"
        )

        app = QApplication.instance()
        if app:
            app.aboutToQuit.connect(self._cleanup)

        print("[WhitelistPage] Yüklendi.")

        platform_name = get_runtime_platform()
        if platform_name == "windows" and not WIN32_AVAILABLE:
            print("[WhitelistPage] Windows aktif pencere izlemesi için pywin32 / psutil eksik.")
        elif platform_name == "macos" and not monitoring_supported():
            print("[WhitelistPage] macOS aktif uygulama izlemesi için AppKit / NSWorkspace hazır değil.")
        elif platform_name == "linux":
            print("[WhitelistPage] Linux foreground app detection henüz uygulanmadı.")

    def _ensure_alert_dialog(self):
        if self._alert_dialog is None:
            self._alert_dialog = ViolationAlertDialog(self)

    def _play_alert_sound_once(self):
        try:
            if os.path.exists(self._alert_sound_path):
                winsound.PlaySound(
                    self._alert_sound_path,
                    winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_NODEFAULT
                )
            else:
                winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
        except Exception as e:
            print(f"[Whitelist] Uyarı sesi çalınamadı: {e}")

    def start_monitoring(self):
        if not monitoring_supported():
            QMessageBox.warning(
                self,
                "Desteklenmiyor",
                "Bu platform için aktif uygulama izleme henüz hazır değil."
            )
            return False

        if self._worker and self._worker.isRunning():
            return True

        self.logic.start_monitoring()

        self._worker = MonitorWorker(self.logic.get_whitelist, 1_000, self)
        self._worker.violation_found.connect(self._ihlal_isle)
        self._worker.no_violation.connect(self._ihlal_yok)
        self._worker.start()

        self._aktif_lbl.setText("İzleme: Açık")
        self._aktif_lbl.setStyleSheet("color:#00e5a0; font-size:11px;")
        self._render_neutral_state()
        self._update_allow_last_controls()

        print("[Whitelist] İzleme başlatıldı (1 sn aralıklı, uygulama modu).")
        return True


    def stop_monitoring(self):
        if self._worker:
            self._worker.stop()
            self._worker = None

        self._monitoring_bitisini_isle()

        self._aktif_lbl.setText("İzleme: Kapalı")
        self._aktif_lbl.setStyleSheet("color:#6b7280; font-size:11px;")
        print("[Whitelist] İzleme durduruldu.")

    def _show_alert_popup(self, detay: str, play_sound: bool = False):
        self._ensure_alert_dialog()
        self._alert_dialog.set_violation_text(detay)
        self._alert_dialog.show()
        self._alert_dialog.raise_()
        self._alert_dialog.activateWindow()

        if play_sound:
            self._play_alert_sound_once()

    def _close_alert_popup(self):
        if self._alert_dialog and self._alert_dialog.isVisible():
            self._alert_dialog.close()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(28, 24, 28, 24)
        root.setSpacing(16)

        title = QLabel("Beyaz Liste & Denetim")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        root.addWidget(title)

        desc = QLabel(
            "Listeye eklediğin uygulama adları dışındaki aktif kullanıcı uygulamaları ihlal sayılır.\n"
            "Sistem uygulamaları otomatik olarak izinli kabul edilir.\n"
            "Uygulama eklemek için kurulu uygulama listesi, dosya seçimi veya son ihlale hızlı izin verme kullanılabilir."
        )
        desc.setStyleSheet("color:#6b7280; font-size:12px;")
        desc.setWordWrap(True)
        root.addWidget(desc)

        action_row = QHBoxLayout()

        if get_runtime_platform() == "windows":
            self._installed_apps_btn = QPushButton("Kurulu Uygulamalardan Ekle")
            self._installed_apps_btn.setFixedHeight(36)
            self._installed_apps_btn.clicked.connect(self._kurulu_uygulamalardan_ekle)
            action_row.addWidget(self._installed_apps_btn)

            self._browse_exe_btn = QPushButton("Dosyadan Uygulama Seç")
            self._browse_exe_btn.setFixedHeight(36)
            self._browse_exe_btn.clicked.connect(self._dosyadan_exe_sec)
            action_row.addWidget(self._browse_exe_btn)

        root.addLayout(action_row)

        add_row = QHBoxLayout()
        self._input = QLineEdit()
        self._input.setPlaceholderText("Manuel uygulama adı gir (örn: chrome.exe, com.google.Chrome)")
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

    def _show_message(self, level: str, msg: str):
        if not msg:
            return

        if level == "warning":
            QMessageBox.warning(self, "Uyarı", msg)
        else:
            QMessageBox.information(self, "Bilgi", msg)

    def _listeyi_yenile(self):
        self._list_widget.clear()
        for item in self.logic._whitelist:
            ui_text = format_identity_for_ui(item)
            lw_item = QListWidgetItem(ui_text)
            lw_item.setData(Qt.ItemDataRole.UserRole, item)
            self._list_widget.addItem(lw_item)

    def _update_allow_last_controls(self):
        aktif = self.logic.has_last_violation()
        self._allow_last_btn.setEnabled(aktif)
        self._allow_last_shortcut.setEnabled(aktif)

        if aktif:
            self._allow_last_btn.setText(
                f"Son İhlale İzin Ver: {self.logic._last_violation_exe} (Ctrl+Shift+A)"
            )
        else:
            self._allow_last_btn.setText("Son İhlale İzin Ver (Ctrl+Shift+A)")

    def _render_neutral_state(self):
        self._ihlal_lbl.setText("İhlal: —")
        self._ihlal_lbl.setStyleSheet("")
        self._detay_lbl.setText("Tespit edilen uygulama: —")

    def _render_violation_state(self, detay: str, started_new: bool):
        self._ihlal_lbl.setText("İhlal: EVET ⚠")
        self._ihlal_lbl.setStyleSheet("color:#ff6b35; font-size:13px; font-weight:700;")
        self._detay_lbl.setText(f"Tespit edilen uygulama: {detay}")

        if started_new:
            print(f"[İHLAL BAŞLADI] {detay}")

    def _render_no_violation_state(self, last_violation: str | None = None, print_log: bool = True):
        if print_log and last_violation:
            print(f"[İHLAL BİTTİ] Son ihlal: {last_violation}")

        self._ihlal_lbl.setText("İhlal: Yok ✓")
        self._ihlal_lbl.setStyleSheet("color:#00e5a0; font-size:13px; font-weight:700;")
        self._detay_lbl.setText("Tespit edilen uygulama: —")

    def _ekle(self):
        raw = self._input.text().strip()

        result = self.logic.add_app_to_whitelist(
            app_id=raw,
            platform_name=get_runtime_platform(),
            id_type=get_default_id_type(),
            app_display_name=raw
        )

        if not result["ok"]:
            self._show_message(result["level"], result["msg"])
            return

        self._listeyi_yenile()
        self._input.clear()
        self._update_allow_last_controls()

        if result["clear_info"] and result["clear_info"]["ended"]:
            self._close_alert_popup()
            self._render_no_violation_state(result["clear_info"]["last_violation"])

        print(f"[Whitelist] Eklendi: {result['app_id']}")
    
    def _sil(self):
        item = self._list_widget.currentItem()
        if not item:
            QMessageBox.warning(self, "Uyarı", "Lütfen listeden bir giriş seç.")
            return

        app_item = item.data(Qt.ItemDataRole.UserRole)
        ok = self.logic.remove_app_from_whitelist(app_item)

        if ok:
            self._listeyi_yenile()
            print(f"[Whitelist] Silindi: {app_item.get('app_id')}")

    def _kurulu_uygulamalardan_ekle(self):
        if os.name != "nt":
            QMessageBox.warning(self, "Desteklenmiyor", "Bu özellik yalnızca Windows'ta kullanılabilir.")
            return

        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        try:
            apps = iter_installed_apps()
        finally:
            QApplication.restoreOverrideCursor()

        if not apps:
            QMessageBox.information(
                self,
                "Bilgi",
                "Kurulu uygulama listesi alınamadı veya uygun exe bulunamadı.\n"
                "İstersen 'Dosyadan Uygulama Seç' seçeneğini kullanabilirsin."
            )
            return

        dialog = InstalledAppsDialog(apps, self)
        if dialog.exec():
            selected = dialog.selected_app()
            if not selected:
                return

            result = self.logic.add_app_to_whitelist(
                app_id=selected.get("exe_name", "").strip().lower(),
                platform_name="windows",
                id_type="exe",
                app_display_name=selected.get("display_name", "").strip() or selected.get("exe_name", "").strip().lower()
            )
            if not result["ok"]:
                self._show_message(result["level"], result["msg"])
                return

            self._listeyi_yenile()
            self._update_allow_last_controls()

            if result["clear_info"] and result["clear_info"]["ended"]:
                self._close_alert_popup()
                self._render_no_violation_state(result["clear_info"]["last_violation"])

            print(f"[Whitelist] Eklendi: {result['app_id']}")

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

        result = self.logic.add_app_to_whitelist(
            app_id=os.path.basename(file_path).lower().strip(),
            platform_name="windows",
            id_type="exe",
            app_display_name=os.path.basename(file_path).lower().strip()
        )
        if not result["ok"]:
            self._show_message(result["level"], result["msg"])
            return

        self._listeyi_yenile()
        self._update_allow_last_controls()

        if result["clear_info"] and result["clear_info"]["ended"]:
            self._close_alert_popup()
            self._render_no_violation_state(result["clear_info"]["last_violation"])

        print(f"[Whitelist] Eklendi: {result['app_id']}")

    def _son_ihlale_izin_ver(self):
        result = self.logic.allow_last_violation()

        if not result["ok"]:
            self._update_allow_last_controls()
            self._show_message(result["level"], result["msg"])
            return

        self._listeyi_yenile()
        self._update_allow_last_controls()

        if result["clear_info"] and result["clear_info"]["ended"]:
            self._close_alert_popup()
            self._render_no_violation_state(result["clear_info"]["last_violation"])

        print(f"[Whitelist] Son ihlale hızlı izin verildi: {result['app_id']}")

    

    def _ihlal_isle(self, violation_payload: dict):
        result = self.logic.process_violation(violation_payload)
        detay = violation_payload.get("detail_text", "")

        self._update_allow_last_controls()
        self._render_violation_state(detay, result["started_new"])
        self._show_alert_popup(detay, play_sound=result["started_new"])

    def _ihlal_yok(self):
        result = self.logic.process_no_violation()
        self._close_alert_popup()
        self._render_no_violation_state(result["last_violation"], print_log=True)

    def _monitoring_bitisini_isle(self):
        summary = self.logic.stop_monitoring_and_save()
        if not summary:
            return

        if summary["db_ok"] is None:
            print(summary["db_msg"])
        else:
            print(f"[DB] {'✓' if summary['db_ok'] else '✗'} {summary['db_msg']}")

        print(
            "[Whitelist ÖZET] "
            f"Toplam izleme: {summary['total_hms']} | "
            f"Toplam ihlal: {summary['violation_hms']} | "
            f"Kayıt sayısı: {summary['record_count']}"
        )
        self._close_alert_popup()

    def _cleanup(self):
        if self._worker:
            self._worker.stop()
            self._worker = None

        self._monitoring_bitisini_isle()
        self._close_alert_popup()

    def closeEvent(self, event):
        self._cleanup()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    page = WhitelistPage("test_user", None)
    page.resize(860, 680)
    page.show()
    sys.exit(app.exec())