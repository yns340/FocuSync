from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox,
    QFrame, QSpinBox, QMessageBox
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QColor, QPainter, QPen

class FocusCircle(QWidget):
    def __init__(self, size=120, parent=None):
        super().__init__(parent)
        self.value = 0
        self.color = "#00e5a0"
        self.setFixedSize(size, size)

    def set_value(self, v, color=None):
        self.value = max(0, min(100, v))
        if color: self.color = color
        self.update()

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        r = self.rect().adjusted(10,10,-10,-10)
        pen = QPen(QColor("#1e2130"), 8, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
        p.setPen(pen)
        p.drawArc(r, 0, 360*16)
        if self.value > 0:
            pen.setColor(QColor(self.color))
            p.setPen(pen)
            p.drawArc(r, 90*16, -int(self.value/100*360*16))
        p.setPen(QColor("#e4e6ed"))
        p.setFont(QFont("Segoe UI",16,QFont.Weight.Bold))
        p.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, f"{self.value}%")

class NotificationBanner(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(42)
        self.setVisible(False)
        l = QHBoxLayout(self)
        l.setContentsMargins(16,6,16,6)
        self.icon_lbl = QLabel()
        self.msg_lbl  = QLabel()
        self.msg_lbl.setStyleSheet("font-weight:600;background:transparent;border:none;")
        l.addWidget(self.icon_lbl)
        l.addWidget(self.msg_lbl)
        l.addStretch()
        self._timer = QTimer(); self._timer.setSingleShot(True)
        self._timer.timeout.connect(lambda: self.setVisible(False))

    def show_warning(self, icon, msg, color="#ff6b35", duration=5000):
        self.setStyleSheet(f"background:rgba(255,107,53,0.10);border:1px solid rgba(255,107,53,0.25);border-radius:8px;")
        if "yüz" in msg.lower() or "kamera" in msg.lower():
            self.setStyleSheet(f"background:rgba(245,158,11,0.10);border:1px solid rgba(245,158,11,0.25);border-radius:8px;")
            color = "#f59e0b"
        self.icon_lbl.setText(icon)
        self.icon_lbl.setStyleSheet(f"font-size:16px;background:transparent;border:none;")
        self.msg_lbl.setText(msg)
        self.msg_lbl.setStyleSheet(f"font-weight:600;color:{color};background:transparent;border:none;")
        self.setVisible(True)
        self._timer.start(duration)

class FocusPage(QWidget):
    violation_signal = pyqtSignal(str)

    def __init__(self, user_id: int, db_manager, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.db_manager = db_manager
        self._session_active = False
        self._elapsed = 0
        self._focused_elapsed = 0
        
        self._timer = QTimer()
        self._timer.timeout.connect(self._tick)
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(28,24,28,24)
        root.setSpacing(16)

        hdr = QHBoxLayout()
        title = QLabel("Odak Modu")
        title.setFont(QFont("Segoe UI",20,QFont.Weight.Bold))
        title.setStyleSheet("color:#e4e6ed;")
        hdr.addWidget(title); hdr.addStretch()
        root.addLayout(hdr)
        
        self.notif = NotificationBanner()
        root.addWidget(self.notif)

        main_row = QHBoxLayout(); main_row.setSpacing(16)
        left = QVBoxLayout(); left.setSpacing(14)

        # Kamera Arayüzü (Core silindi, sadece UI tepkisi var)
        cam_card = QFrame()
        cam_card.setStyleSheet("background:#111318;border:1px solid #1e2130;border-radius:14px;")
        cl = QVBoxLayout(cam_card); cl.setContentsMargins(16,14,16,14); cl.setSpacing(10)
        ch = QHBoxLayout()
        ch.addWidget(self._sec("Kamera (Arayüz Testi)"))
        self.cam_status_lbl = QLabel("⬤  Kapalı")
        self.cam_status_lbl.setStyleSheet("color:#6b7280;font-size:11px;background:transparent;border:none;")
        ch.addStretch(); ch.addWidget(self.cam_status_lbl)
        cl.addLayout(ch)

        cam_frame = QFrame()
        cam_frame.setStyleSheet("background:#0a0c10;border:1px dashed #1e2130;border-radius:10px;min-height:200px;")
        cfl = QVBoxLayout(cam_frame); cfl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cam_placeholder = QLabel("📷\nKamera Modülü (Core) Devre Dışı")
        self.cam_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cam_placeholder.setStyleSheet("color:#2e3248;font-size:14px;background:transparent;border:none;")
        cfl.addWidget(self.cam_placeholder)
        cl.addWidget(cam_frame)

        cam_ctrl = QHBoxLayout()
        self.cam_toggle_btn = QPushButton("Kamerayı Aç (UI Test)")
        self.cam_toggle_btn.setFixedHeight(32)
        self.cam_toggle_btn.clicked.connect(self._toggle_camera_ui)
        cam_ctrl.addWidget(self.cam_toggle_btn)
        cl.addLayout(cam_ctrl)
        left.addWidget(cam_card)

        # Zamanlayıcı
        timer_card = QFrame()
        timer_card.setStyleSheet("background:#111318;border:1px solid #1e2130;border-radius:14px;")
        tl = QHBoxLayout(timer_card); tl.setContentsMargins(20,14,20,14); tl.setSpacing(20)

        timer_info = QVBoxLayout()
        timer_info.addWidget(self._sec("Seans Süresi"))
        self.timer_lbl = QLabel("00:00:00")
        self.timer_lbl.setFont(QFont("Segoe UI",34,QFont.Weight.Bold))
        self.timer_lbl.setStyleSheet("color:#00e5a0;letter-spacing:2px;background:transparent;border:none;")
        timer_info.addWidget(self.timer_lbl)
        tl.addLayout(timer_info); tl.addStretch()

        btn_col = QVBoxLayout()
        self.start_btn = QPushButton("▶  Seansı Başlat")
        self.start_btn.setObjectName("primary_btn")
        self.start_btn.setFixedHeight(42)
        self.start_btn.clicked.connect(self._toggle_session)
        btn_col.addWidget(self.start_btn)
        tl.addLayout(btn_col)
        left.addWidget(timer_card)
        main_row.addLayout(left, 3)

        # Sağ Panel: Skor
        right = QVBoxLayout(); right.setSpacing(14)
        score_card = QFrame()
        score_card.setStyleSheet("background:#111318;border:1px solid #1e2130;border-radius:14px;")
        scl = QVBoxLayout(score_card); scl.setContentsMargins(18,14,18,14); scl.setSpacing(12)
        scl.addWidget(self._sec("Anlık Odak Skoru"))

        cring_row = QHBoxLayout(); cring_row.addStretch()
        self.focus_ring = FocusCircle(120); cring_row.addWidget(self.focus_ring); cring_row.addStretch()
        scl.addLayout(cring_row)
        right.addWidget(score_card)
        right.addStretch()
        main_row.addLayout(right, 2)
        root.addLayout(main_row, 1)

    def _sec(self, text):
        l = QLabel(text); l.setFont(QFont("Segoe UI",13,QFont.Weight.Bold))
        l.setStyleSheet("color:#e4e6ed;background:transparent;border:none;")
        return l

    def _toggle_session(self):
        if not self._session_active:
            self._start_session()
        else:
            self._end_session()

    def _start_session(self):
        self._session_active = True
        self._elapsed = 0; self._focused_elapsed = 0
        self.focus_ring.set_value(100, "#00e5a0")
        self._timer.start(1000)
        self.start_btn.setText("⏹  Seansı Bitir")
        self.start_btn.setObjectName("danger_btn")
        self.start_btn.style().unpolish(self.start_btn); self.start_btn.style().polish(self.start_btn)
        self.notif.show_warning("▶","Odak seansı başladı!","#00e5a0",3000)

    def _end_session(self):
        self._session_active = False
        self._timer.stop()
        
        # db_manager ile Firebase'e kayıt
        actual_focus_time = self._elapsed // 60
        score = int(self._focused_elapsed / self._elapsed * 100) if self._elapsed > 0 else 0
        success, msg = self.db_manager.add_focus_session(self.user_id, "manuel_plan", "Genel Çalışma", actual_focus_time, score, "Completed")
        
        self.notif.show_warning("✅",f"Seans tamamlandı! Firebase Kaydı: {msg}","#00e5a0",6000)
        
        self.start_btn.setText("▶  Seansı Başlat")
        self.start_btn.setObjectName("primary_btn")
        self.start_btn.style().unpolish(self.start_btn); self.start_btn.style().polish(self.start_btn)
        self._elapsed = 0
        self.timer_lbl.setText("00:00:00")

    def _tick(self):
        self._elapsed += 1
        self._focused_elapsed += 1 # Basit test için tam odak kabul ediyoruz
        h = self._elapsed // 3600; m = (self._elapsed % 3600) // 60; s = self._elapsed % 60
        self.timer_lbl.setText(f"{h:02d}:{m:02d}:{s:02d}")

    def _toggle_camera_ui(self):
        # Sadece UI durumu değişir, gerçek kamera açılmaz
        if "Aç" in self.cam_toggle_btn.text():
            self.cam_toggle_btn.setText("Kamerayı Kapat (UI Test)")
            self.cam_status_lbl.setText("⬤  Aktif (Sanal)")
            self.cam_status_lbl.setStyleSheet("color:#00e5a0;font-size:11px;background:transparent;border:none;")
            self.cam_placeholder.setText("📷\n(Kamera Arayüzü Aktif)")
        else:
            self.cam_toggle_btn.setText("Kamerayı Aç (UI Test)")
            self.cam_status_lbl.setText("⬤  Kapalı")
            self.cam_status_lbl.setStyleSheet("color:#6b7280;font-size:11px;background:transparent;border:none;")
            self.cam_placeholder.setText("📷\nKamera Modülü (Core) Devre Dışı")

    def cleanup(self):
        self._timer.stop()