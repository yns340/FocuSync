from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QScrollArea
)
from PyQt6.QtCore import pyqtSignal
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

        hdr = QHBoxLayout()
        self.greeting_lbl = QLabel(f"Merhaba! (ID: {self.user_id})")
        self.greeting_lbl.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        self.greeting_lbl.setStyleSheet("color:#e4e6ed;")
        self.date_lbl = QLabel(datetime.now().strftime("%d %m %Y"))
        self.date_lbl.setStyleSheet("color:#6b7280;font-size:12px;")
        hdr.addWidget(self.greeting_lbl); hdr.addStretch(); hdr.addWidget(self.date_lbl)
        lay.addLayout(hdr)

        info = QLabel("Dashboard verileri şu an boştur. db_manager.py içerisine 'Firebase'den Veri Çekme (Read)' fonksiyonları eklendiğinde bu alandaki grafikler dolacaktır.")
        info.setStyleSheet("color:#ff6b35; font-size:12px; padding:10px; background:rgba(255,107,53,0.1); border-radius:8px;")
        info.setWordWrap(True)
        lay.addWidget(info)

        # Boş İstatistik Kartları (Tasarım bozulmasın diye tutuldu)
        stats_row = QHBoxLayout()
        self.card_score   = MiniStatCard("🎯","ODAK SKORU",   "—",  "", "#00e5a0")
        self.card_courses = MiniStatCard("📚","DERS SAYISI",   "—",  "", "#0099ff")
        self.card_viol    = MiniStatCard("⚠️","İHLAL",        "—",  "", "#ff6b35")
        self.card_time    = MiniStatCard("⏱️","ÇALIŞMA",      "—",  "", "#f59e0b")
        for c in [self.card_score, self.card_courses, self.card_viol, self.card_time]:
            stats_row.addWidget(c)
        lay.addLayout(stats_row)
        lay.addStretch()

    def set_user(self, user):
        pass # Artık user listesi değil direkt user_id kullanıyoruz

    def refresh(self):
        pass # Read fonksiyonları gelene kadar pasif