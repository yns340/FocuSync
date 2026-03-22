from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QScrollArea
)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont
from datetime import datetime

class MiniStatCard(QFrame):
    def __init__(self, icon, label, value, sub="", accent="#00e5a0", parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"background:#111318;border:1px solid #1e2130;border-top:3px solid {accent};border-radius:12px;")
        lay = QVBoxLayout(self)
        lay.setContentsMargins(18, 14, 18, 14)
        
        top = QHBoxLayout()
        ic = QLabel(icon); ic.setStyleSheet("font-size:20px;background:transparent;border:none;")
        top.addWidget(ic); top.addStretch()
        tl = QLabel(label); tl.setStyleSheet(f"color:#6b7280;font-size:10px;font-weight:700;letter-spacing:0.8px;background:transparent;border:none;")
        top.addWidget(tl)
        lay.addLayout(top)

        self.val_lbl = QLabel(value)
        self.val_lbl.setStyleSheet("font-size:26px;font-weight:700;color:#e4e6ed;background:transparent;border:none;")
        lay.addWidget(self.val_lbl)

class DashboardPage(QWidget):
    navigate_to = pyqtSignal(str)

    def __init__(self, user_id: int, db_manager, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.db_manager = db_manager
        self._build_ui()
        self.refresh() # Sayfa açıldığında verileri otomatik çek

    def _build_ui(self):
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)

        container = QWidget()
        scroll.setWidget(container)
        lay = QVBoxLayout(container)
        lay.setContentsMargins(28, 24, 28, 24)
        lay.setSpacing(20)

        # Başlık ve Tarih
        hdr = QHBoxLayout()
        self.greeting_lbl = QLabel("MERHABA!")

        # DİKKAT: setFont kullanmadık, boyutu (font-size: 64px) buraya yazdık!
        self.greeting_lbl.setStyleSheet("""
            font-family: 'Segoe UI';
            font-size: 32px;
            font-weight: bold;
            color: #e4e6ed;
            padding-bottom: 15px;
            letter-spacing: 2px;
        """)

        self.date_lbl = QLabel(datetime.now().strftime("%d %m %Y"))
        self.date_lbl.setStyleSheet("color:#6b7280;font-size:16px; font-weight:600;")
        hdr.addWidget(self.greeting_lbl); hdr.addStretch(); hdr.addWidget(self.date_lbl)
        hdr.setAlignment(self.date_lbl, Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight)
        lay.addLayout(hdr)

        # İstatistik Kartları
        stats_row = QHBoxLayout()
        self.card_score   = MiniStatCard("🎯", "ODAK SKORU", "%0", "", "#00e5a0")
        self.card_courses = MiniStatCard("📚", "DERS SAYISI", "0", "", "#0099ff")
        self.card_time    = MiniStatCard("⏱️", "ÇALIŞMA (Dk)", "0", "", "#f59e0b")
        self.card_viol    = MiniStatCard("⚠️", "İHLAL", "0", "", "#ff6b35")
        
        for c in [self.card_score, self.card_courses, self.card_time, self.card_viol]:
            stats_row.addWidget(c)
        
        lay.addLayout(stats_row)
        lay.addStretch()

    def set_user(self, user):
        pass

    def refresh(self):
        """Firebase'den verileri çeker ve kartları günceller."""
        success, data = self.db_manager.get_dashboard_stats(self.user_id)
        
        if success:
            # 1. Kullanıcı adını güncelle
            name = data.get("user_name", "")
            if name:
                self.greeting_lbl.setText(f"MERHABA, {name.upper()}!")
            else:
                self.greeting_lbl.setText(f"MERHABA! (ID: {self.user_id[:5]}...)") # ID uzunsa ilk 5 karakter

            # 2. İstatistikleri Kartlara Yazdır
            self.card_score.val_lbl.setText(f"%{data.get('avg_focus_score', 0)}")
            self.card_courses.val_lbl.setText(str(data.get('course_count', 0)))
            self.card_time.val_lbl.setText(str(data.get('total_study_time', 0)))
            self.card_viol.val_lbl.setText(str(data.get('violation_count', 0)))