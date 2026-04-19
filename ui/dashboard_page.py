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

        # HESAPLAYICI VE PDF KARTLARI (ACTIONS ROW)
        actions_row = QHBoxLayout()
        actions_row.setSpacing(20)
        
        # Kart: Hesaplayıcı
        self.calc_card = QFrame()
        self.calc_card.setCursor(Qt.CursorShape.PointingHandCursor)
        self.calc_card.setFixedSize(220, 120)
        self.calc_card.setStyleSheet("""
            QFrame {
                background: #1e2130;
                border: 1px solid #2a3042;
                border-top: 3px solid #00e5a0;
                border-radius: 12px;
            }
            QFrame:hover { background: #25293d; border: 1px solid #00e5a0; }
        """)
        
        calc_lay = QVBoxLayout(self.calc_card)
        calc_lay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_lbl = QLabel("🧮")
        icon_lbl.setStyleSheet("font-size: 28px; border: none; background: transparent;")
        title_lbl = QLabel("HEDEF NOT<br>HESAPLAYICI")
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_lbl.setStyleSheet("color: #e4e6ed; font-weight: 800; font-size: 11px; letter-spacing: 1px; border: none; background: transparent;")
        calc_lay.addWidget(icon_lbl); calc_lay.addSpacing(5); calc_lay.addWidget(title_lbl)
        self.calc_card.mousePressEvent = lambda event: self.open_grade_calculator()
        actions_row.addWidget(self.calc_card)

        # Kart: PDF Aktar
        self.pdf_card = QFrame()
        self.pdf_card.setCursor(Qt.CursorShape.PointingHandCursor)
        self.pdf_card.setFixedSize(220, 120)
        self.pdf_card.setStyleSheet("""
            QFrame {
                background: #1e2130;
                border: 1px solid #2a3042;
                border-top: 3px solid #0099ff;
                border-radius: 12px;
            }
            QFrame:hover { background: #25293d; border: 1px solid #0099ff; }
        """)
        
        pdf_lay = QVBoxLayout(self.pdf_card)
        pdf_lay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pdf_icon = QLabel("📄")
        pdf_icon.setStyleSheet("font-size: 28px; border: none; background: transparent;")
        pdf_title = QLabel("PROGRAMI<br>PDF'DEN AKTAR")
        pdf_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pdf_title.setStyleSheet("color: #e4e6ed; font-weight: 800; font-size: 11px; border: none; background: transparent;")
        pdf_lay.addWidget(pdf_icon); pdf_lay.addWidget(pdf_title)
        self.pdf_card.mousePressEvent = lambda event: self.start_pdf_import()
        actions_row.addWidget(self.pdf_card)

        actions_row.addStretch() 
        lay.addLayout(actions_row)

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
            
    def open_grade_calculator(self):
        """Kullanıcının girdiği özel not bileşenlerine göre hedef hesaplaması yapar."""
        try:
            # 1. Hedef Ortalamayı Al
            target, ok = QInputDialog.getDouble(self, "Hedef", "Dönem sonu hedef ortalamanız:", 60, 0, 100, 1)
            if not ok: return

            # 2. Bileşen Sayılarını Al
            vize_sayisi, ok1 = QInputDialog.getInt(self, "Vize", "Kaç vize var?", 2, 0, 5)
            if not ok1: return
            
            odev_sayisi, ok2 = QInputDialog.getInt(self, "Ödev", "Kaç ödev var?", 4, 0, 10)
            if not ok2: return

            # 3. Yüzdelik Etkileri Al (Sistem toplamın 100 olmasını bekler)
            vize_etki, ok3 = QInputDialog.getInt(self, "Vize Etkisi", "Tüm vizelerin toplam etkisi (%):", 30, 0, 100)
            odev_etki, ok4 = QInputDialog.getInt(self, "Ödev Etkisi", "Tüm ödevlerin toplam etkisi (%):", 30, 0, 100)
            final_etki = 100 - (vize_etki + odev_etki)
            
            if final_etki < 0:
                QMessageBox.warning(self, "Hata", "Vize ve ödev etkisi toplamı 100'ü geçemez!")
                return

            # 4. Notları Topla
            toplam_katki = 0
            
            # Vizeler
            for i in range(vize_sayisi):
                notu, ok = QInputDialog.getInt(self, "Vize Notu", f"{i+1}. Vize notunuz:", 50, 0, 100)
                if ok: toplam_katki += (notu / vize_sayisi) * (vize_etki / 100)
                
            # Ödevler
            for i in range(odev_sayisi):
                notu, ok = QInputDialog.getInt(self, "Ödev Notu", f"{i+1}. Ödev notunuz:", 80, 0, 100)
                if ok: toplam_katki += (notu / odev_sayisi) * (odev_etki / 100)

            # 5. Final Hesabı
            gereken_puan = target - toplam_katki
            gereken_final = gereken_puan / (final_etki / 100)

            # 6. Sonuç Gösterimi
            res_text = (f"<b>Hedef: {target}</b><br><br>"
                        f"Şu ana kadarki katkı: {round(toplam_katki, 2)} puan<br>"
                        f"Final Etkisi: %{final_etki}<br><br>")
            
            if gereken_final > 100:
                res_text += f"<font color='#ff6b35'>Finalden {round(gereken_final,1)} almanız gerekiyor. Hedef çok zor!</font>"
            else:
                res_text += f"<font color='#00e5a0'>Finalden en az <b>{max(0, round(gereken_final,1))}</b> almalısınız.</font>"

            QMessageBox.information(self, "Detaylı Not Analizi", res_text)

        except Exception as e:
            print(f"Hesaplayıcı hatası: {e}")
            
    def start_pdf_import(self):
        """Gelişmiş Regex ile PDF okuma ve Düzenleme Tablosu"""
        import pdfplumber
        import re
        from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView

        file_path, _ = QFileDialog.getOpenFileName(self, "PDF Seç", "", "PDF Dosyaları (*.pdf)")
        if not file_path: return

        try:
            with pdfplumber.open(file_path) as pdf:
                full_text = "\n".join([page.extract_text() for page in pdf.pages])

            # 1. Gelişmiş Regex 
            pattern = r"([A-Z]{2,4}[-\s]?\d{3})\s+([A-Za-zÇŞĞÜİÖçşğüiö\s\-\(\)]+)"
            matches = re.findall(pattern, full_text)
            
            if not matches:
                QMessageBox.warning(self, "Hata", "Ders formatı algılanamadı! Manuel girişe yönlendiriliyorsunuz.") [cite: 305]
                return

            # 2. Onay ve Düzenleme Diyaloğu 
            dialog = QDialog(self)
            dialog.setWindowTitle("Ders Programı Düzenleme ve Onay")
            dialog.setMinimumWidth(600)
            d_lay = QVBoxLayout(dialog)

            desc = QLabel("PDF'ten çekilen dersler aşağıdadır. Hatalı olanları üzerine tıklayıp düzeltebilirsiniz.")
            desc.setWordWrap(True)
            d_lay.addWidget(desc)

            table = QTableWidget(len(matches), 3)
            table.setHorizontalHeaderLabels(["Ders Kodu", "Ders Adı", "Başlangıç Zorluğu"])
            table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

            for i, (code, name) in enumerate(matches):
                table.setItem(i, 0, QTableWidgetItem(code.strip()))
                table.setItem(i, 1, QTableWidgetItem(name.strip()))
                table.setItem(i, 2, QTableWidgetItem("3.0")) 

            d_lay.addWidget(table)

            btn_box = QHBoxLayout()
            save_btn = QPushButton("Veritabanına Kaydet")
            save_btn.setStyleSheet("background: #00e5a0; color: #111318; font-weight: bold; padding: 10px;")
            cancel_btn = QPushButton("İptal")
            btn_box.addWidget(cancel_btn)
            btn_box.addWidget(save_btn)
            d_lay.addLayout(btn_box)

            save_btn.clicked.connect(dialog.accept)
            cancel_btn.clicked.connect(dialog.reject)

            # 3. Onay Verildiyse Kaydet
            if dialog.exec() == QDialog.DialogCode.Accepted:
                try:
                    success_count = 0
                    for row in range(table.rowCount()):
                        c_id = table.item(row, 0).text().strip()
                        c_name = table.item(row, 1).text().strip()
                    
                        try:
                            c_diff = float(table.item(row, 2).text().replace(',', '.'))
                        except:
                            c_diff = 3.0 

                        # Yunus'un metodunu çağırıyoruz
                        success, _ = self.db_manager.add_course(
                            user_id=self.user_id,
                            course_id=c_id,
                            course_name=c_name,
                            difficulty_level=c_diff,
                            weekly_hours=3
                        )
                        if success:
                            success_count += 1

                    if success_count > 0:
                        QMessageBox.information(self, "Başarılı", f"{success_count} ders Firebase'e işlendi.")
                        self.refresh() 
                
                except Exception as db_e:
                    QMessageBox.critical(self, "Hata", f"Veritabanı kaydı sırasında hata oluştu: {db_e}")

        except Exception as e:
            # Genel PDF işleme hatası
            QMessageBox.critical(self, "Hata", f"PDF işleme hatası: {e}")