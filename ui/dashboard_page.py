from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QScrollArea,
    QPushButton, QInputDialog, QMessageBox, QFileDialog, QDialog, QTableWidgetItem, QHeaderView
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
        lay.setSpacing(25)

        # Başlık ve Tarih Bölümü
        hdr = QHBoxLayout()
        self.greeting_lbl = QLabel("MERHABA!")
        self.greeting_lbl.setStyleSheet("""
            font-family: 'Segoe UI'; font-size: 32px; font-weight: bold;
            color: #e4e6ed; padding-bottom: 15px; letter-spacing: 2px;
        """)
        self.date_lbl = QLabel(datetime.now().strftime("%d %m %Y"))
        self.date_lbl.setStyleSheet("color:#6b7280; font-size:16px; font-weight:600;")
        hdr.addWidget(self.greeting_lbl); hdr.addStretch(); hdr.addWidget(self.date_lbl)
        lay.addLayout(hdr)

        # İstatistik Kartları
        stats_row = QHBoxLayout()
        self.card_score   = MiniStatCard("🎯", "ODAK SKORU", "%0", "", "#00e5a0")
        self.card_courses = MiniStatCard("📚", "DERS SAYISI", "0", "", "#0099ff")
        self.card_time    = MiniStatCard("⏱️", "ÇALIŞMA (Dk)", "0", "", "#f59e0b")
        self.card_viol    = MiniStatCard("⚠️", "İHLAL", "0", "", "#ff6b35")
        
        for c in [self.card_score, self.card_courses, self.card_time, self.card_viol]:
            c.setFixedHeight(120) # Kartların devasa olmasını engellemek için yükseklik sabitledik
            stats_row.addWidget(c)
        lay.addLayout(stats_row)

        # ACTIONS ROW REMOVED 

        self._add_weekly_summary_ui(lay)
        self._add_risk_analysis_ui(lay)
        lay.addStretch()
        
    def set_user(self, user):
        pass

    def refresh(self):
        """Firebase'den verileri çeker ve kartları günceller."""
        success, data = self.db_manager.get_dashboard_stats(self.user_id)
        
        if success:
            name = data.get("user_name", "")
            if name:
                self.greeting_lbl.setText(f"MERHABA, {name.upper()}!")
            else:
                self.greeting_lbl.setText(f"MERHABA! (ID: {self.user_id[:5]}...)")

            self.card_score.val_lbl.setText(f"%{data.get('avg_focus_score', 0)}")
            self.card_courses.val_lbl.setText(str(data.get('course_count', 0)))
            self.card_time.val_lbl.setText(str(data.get('total_study_time', 0)))
            self.card_viol.val_lbl.setText(str(data.get('violation_count', 0)))
            
            ok, weekly_data = self.db_manager.get_weekly_analysis(self.user_id)
            if ok:
                self.update_weekly_chart(weekly_data)
            else:
                self.update_weekly_chart({'Pzt':0,'Sal':0,'Çar':0,'Per':0,'Cum':0,'Cmt':0,'Paz':0})
            
            # IVR-REQ-02 — Risk analizini UI'a gerçekten yansıt
            success_r, risk_data = self.db_manager.get_course_risk_analysis(self.user_id)
            if success_r and risk_data:
                self._update_risk_panel(risk_data)

            # ADG-REQ-02 — Pazar günü haftalık otomatik zorluk güncelleme döngüsü
            from datetime import datetime as _dt
            if _dt.now().strftime('%A') == 'Sunday':
                try:
                    from decision_engine import DecisionEngine
                    engine = DecisionEngine(self.db_manager)
                    engine.run_weekly_update(self.user_id)
                except Exception as _e:
                    print(f"[Dashboard] Haftalık AI güncelleme hatası: {_e}")
                
    def update_weekly_chart(self, weekly_data):
        """
        weekly_data: {'Pzt': 75, 'Sal': 40, ...} gibi 100 üzerinden skorlar
        """
        max_height = 120 # track yüksekliği
        for day, score in weekly_data.items():
            if day in self.daily_bars:
                # Skora göre yüksekliği ayarla (Örn: %80 odak = 96px bar)
                new_height = int((score / 100) * max_height)
                self.daily_bars[day].setFixedHeight(max_height if new_height > max_height else new_height)
            
        
    def _add_weekly_summary_ui(self, layout):
        """Haftalık Verimlilik Grafiği"""
        summary_frame = QFrame()
        summary_frame.setStyleSheet("background: #111318; border: 1px solid #1e2130; border-radius: 15px;")
        s_lay = QVBoxLayout(summary_frame)
        s_lay.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("📊 HAFTALIK ODAKLANMA TRENDİ")
        title.setStyleSheet("color: #6b7280; font-weight: bold; font-size: 11px; letter-spacing: 1px; border: none;")
        s_lay.addWidget(title)
        s_lay.addSpacing(15)
        
        self.daily_bars = {} # Barları gün isimleriyle saklayalım
        days = ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"]
        chart_lay = QHBoxLayout()
        chart_lay.setSpacing(15)
        
        for day in days:
            day_box = QVBoxLayout()
            
            # Arka plan kanalı (gri ince çubuk)
            track = QFrame()
            track.setFixedWidth(12)
            track.setFixedHeight(120)
            track.setStyleSheet("background: #1e2130; border-radius: 6px;")
            track_lay = QVBoxLayout(track)
            track_lay.setContentsMargins(0, 0, 0, 0)
            track_lay.setAlignment(Qt.AlignmentFlag.AlignBottom)
            
            # Gerçek veri barı (mavi dolgu)
            bar = QFrame()
            bar.setFixedWidth(12)
            bar.setFixedHeight(20) # Başlangıçta kısa, veriyle uzayacak
            bar.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #00e5a0, stop:1 #0099ff); border-radius: 6px;")
            
            self.daily_bars[day] = bar # Referansı kaydet
            track_lay.addWidget(bar)
            
            lbl = QLabel(day)
            lbl.setStyleSheet("color: #6b7280; font-size: 10px; font-weight: bold; border: none; margin-top: 8px;")
            
            day_box.addWidget(track, alignment=Qt.AlignmentFlag.AlignCenter)
            day_box.addWidget(lbl, alignment=Qt.AlignmentFlag.AlignCenter)
            chart_lay.addLayout(day_box)
            
        s_lay.addLayout(chart_lay)
        layout.addWidget(summary_frame)
        
    def _add_risk_analysis_ui(self, parent_layout):
        """SRS 3.2.8.4: Akademik Başarı Tahminleme Panelini Dashboard'a ekler."""
        risk_card = QFrame()
        risk_card.setStyleSheet("""
            QFrame {
                background: #111318;
                border: 1px solid #1e2130;
                border-radius: 16px;
                margin-top: 10px;
            }
        """)
        self.risk_vbox = QVBoxLayout(risk_card)
        self.risk_vbox.setContentsMargins(20, 18, 20, 18)

        title_row = QHBoxLayout()
        title_lbl = QLabel("🎯 AKADEMİK RİSK VE HEDEF ANALİZİ (AI)")
        title_lbl.setStyleSheet("color: #6b7280; font-weight: bold; font-size: 11px; letter-spacing: 1px; border: none;")
        title_row.addWidget(title_lbl)
        title_row.addStretch()
        self.risk_vbox.addLayout(title_row)
        self.risk_vbox.addSpacing(10)

        # İlk yükleme — boş durumu göster
        self.risk_no_data_lbl = QLabel("Henüz analiz edilecek yeterli seans veya ders verisi bulunmuyor.")
        self.risk_no_data_lbl.setStyleSheet("color: #4b5563; font-style: italic; border: none;")
        self.risk_vbox.addWidget(self.risk_no_data_lbl)

        parent_layout.addWidget(risk_card)

    def _update_risk_panel(self, analysis_data: list):
        """IVR-REQ-02: Risk panelini güncel veriyle yeniden çizer."""
        # Eski satır widget'larını temizle (başlık ve spacing hariç, ilk 2 item korunur)
        while self.risk_vbox.count() > 2:
            item = self.risk_vbox.takeAt(2)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                # Layout içindeki widget'ları da sil
                while item.layout().count():
                    child = item.layout().takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()

        if not analysis_data:
            no_data = QLabel("Henüz analiz edilecek yeterli seans veya ders verisi bulunmuyor.")
            no_data.setStyleSheet("color: #4b5563; font-style: italic; border: none;")
            self.risk_vbox.addWidget(no_data)
            return

        for i, item in enumerate(analysis_data):
            course_row = QHBoxLayout()

            name_lbl = QLabel(item.get('course_name', item.get('name', 'Bilinmeyen Ders')))
            name_lbl.setStyleSheet("color: #e4e6ed; font-size: 13px; font-weight: 500; border: none;")

            target_lbl = QLabel(f"Hedef: {item.get('target', '-')}")
            target_lbl.setStyleSheet("color: #94a3b8; font-size: 11px; border: none;")

            status_lbl = QLabel(item.get('status', '').upper())
            status_lbl.setStyleSheet(
                f"color: {item.get('color', '#e4e6ed')}; font-weight: bold; font-size: 11px; border: none;"
            )

            course_row.addWidget(name_lbl)
            course_row.addStretch()
            course_row.addWidget(target_lbl)
            course_row.addSpacing(25)
            course_row.addWidget(status_lbl)
            self.risk_vbox.addLayout(course_row)

            if i < len(analysis_data) - 1:
                line = QFrame()
                line.setFrameShape(QFrame.Shape.HLine)
                line.setStyleSheet("background-color: #1e2130; max-height: 1px; border: none;")
                self.risk_vbox.addWidget(line)
            