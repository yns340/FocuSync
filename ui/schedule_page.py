from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QFileDialog, QHeaderView,
    QMessageBox, QComboBox, QTimeEdit, QAbstractItemView, QListView
)
from PyQt6.QtCore import Qt, QTime
from PyQt6.QtGui import QFont

from ocr_manager import OCRManager

class SchedulePage(QWidget):
    def __init__(self, user_id, db_manager, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.db_manager = db_manager
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(28, 24, 28, 24)
        root.setSpacing(20)

        # ── Başlık ──
        hdr = QHBoxLayout()
        title = QLabel("Sabit Ders Programı")
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        title.setStyleSheet("color:#e4e6ed;")
        hdr.addWidget(title)
        hdr.addStretch()
        root.addLayout(hdr)

        # ── Yükleme Alanı (Büyük Kare Buton) ──
        self.upload_btn = QPushButton("\n📄\n\nPDF veya Görsel Yükle\n(Sürükle bırak veya seçmek için tıkla)\n")
        self.upload_btn.setFont(QFont("Segoe UI", 12))
        self.upload_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.upload_btn.setStyleSheet("""
            QPushButton {
                background-color: #1a1d26;
                color: #6b7280;
                border: 2px dashed #2e3248;
                border-radius: 12px;
                padding: 40px;
            }
            QPushButton:hover {
                background-color: #1e2130;
                border: 2px dashed #00e5a0;
                color: #e4e6ed;
            }
        """)
        self.upload_btn.clicked.connect(self._import_file)
        root.addWidget(self.upload_btn)

        # ── Düzenleme Alanı ──
        self.editor_container = QWidget()
        editor_layout = QVBoxLayout(self.editor_container)
        editor_layout.setContentsMargins(0, 0, 0, 0)
        editor_layout.setSpacing(15)

        # Araç Çubuğu
        tools_row = QHBoxLayout()
        ocr_title = QLabel("🔍 OCR Önizlemesi (Hataları üzerlerine tıklayarak düzeltebilirsiniz)")
        ocr_title.setStyleSheet("color:#00e5a0; font-weight:bold; font-size:14px;")
        tools_row.addWidget(ocr_title)
        tools_row.addStretch()

        add_row_btn = QPushButton("+ Satır Ekle")
        add_row_btn.setStyleSheet("background:#2e3248; color:#e4e6ed; border-radius:6px; padding:8px 16px; font-size: 14px; font-weight: bold;")
        add_row_btn.clicked.connect(lambda: self._add_table_row()) 
        
        del_row_btn = QPushButton("- Seçili Satırı Sil")
        del_row_btn.setStyleSheet("background:#ff6b35; color:#e4e6ed; border-radius:6px; padding:8px 16px; font-size: 14px; font-weight: bold;")
        del_row_btn.clicked.connect(self._delete_selected_row)

        tools_row.addWidget(add_row_btn)
        tools_row.addWidget(del_row_btn)
        editor_layout.addLayout(tools_row)

        # ── TABLO TASARIMI VE AYARLARI ──
        self.table = QTableWidget(0, 5) 
        self.table.setHorizontalHeaderLabels(["Gün", "Başlangıç", "Bitiş", "Ders Adı", "Tip"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        self.table.verticalHeader().setDefaultSectionSize(60)
        self.table.verticalHeader().setVisible(False) 

        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #111318;
                color: #e4e6ed;
                gridline-color: #1e2130;
                border: 1px solid #1e2130;
                border-radius: 8px;
                font-size: 18px; 
            }
            QHeaderView::section {
                background-color: #1a1d26;
                color: #6b7280;
                padding: 10px; 
                border: 1px solid #1e2130;
                font-weight: bold;
                font-size: 14px;
            }
            QTableWidget::item:selected {
                background-color: rgba(0, 229, 160, 0.15);
                border-top: 1px solid #00e5a0;
                border-bottom: 1px solid #00e5a0;
                color: #e4e6ed;
            }
            QComboBox, QTimeEdit {
                background-color: #1a1d26;
                color: #e4e6ed;
                border: 1px solid #2e3248;
                border-radius: 6px;
                font-size: 16px; 
                padding: 4px 10px;
                margin: 4px; 
            }
            QComboBox::drop-down, QTimeEdit::up-button, QTimeEdit::down-button {
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: #1a1d26;
                color: #e4e6ed;
                border: 1px solid #00e5a0;
                border-radius: 6px;
                selection-background-color: #00e5a0;
                selection-color: #111318;
                outline: none;
            }
            QComboBox QAbstractItemView::item {
                min-height: 35px;
                padding-left: 10px;
            }
            QTableWidget QLineEdit {
                font-size: 18px;
                color: #e4e6ed;
                background-color: #1a1d26;
            }
        """)
        editor_layout.addWidget(self.table, 1)

        # Kaydet Butonu
        self.save_btn = QPushButton("Veritabanına Kaydet")
        self.save_btn.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold)) 
        self.save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #00e5a0;
                color: #111318;
                border-radius: 8px;
                padding: 16px;
            }
            QPushButton:hover {
                background-color: #00c88c;
            }
        """)
        self.save_btn.clicked.connect(self._save_to_db)
        editor_layout.addWidget(self.save_btn)

        root.addWidget(self.editor_container, 1)
        self.editor_container.setVisible(False)
        
        root.addStretch()

    def _add_table_row(self, day="Pazartesi", start="09:00", end="10:00", course="", ctype="Teorik"):
        row_idx = self.table.rowCount()
        self.table.insertRow(row_idx)

        # 1. GÜN
        day_cb = QComboBox()
        day_cb.setView(QListView())
        day_cb.addItems(["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"])
        day_cb.setCurrentText(day)
        self.table.setCellWidget(row_idx, 0, day_cb)

        # 2. BAŞLANGIÇ SAATİ
        start_te = QTimeEdit(QTime.fromString(start, "HH:mm"))
        start_te.setDisplayFormat("HH:mm")
        self.table.setCellWidget(row_idx, 1, start_te)

        # 3. BİTİŞ SAATİ
        end_te = QTimeEdit(QTime.fromString(end, "HH:mm"))
        end_te.setDisplayFormat("HH:mm")
        self.table.setCellWidget(row_idx, 2, end_te)

        # 4. DERS ADI
        course_item = QTableWidgetItem(course)
        course_item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        self.table.setItem(row_idx, 3, course_item)

        # 5. TİP
        type_cb = QComboBox()
        type_cb.setView(QListView())
        type_cb.addItems(["Teorik", "Uygulamalı"])
        type_cb.setCurrentText(ctype)
        self.table.setCellWidget(row_idx, 4, type_cb)

    def _import_file(self):
        """Kullanıcının seçtiği PDF'i gerçek OCR'a gönderir ve tabloyu doldurur."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Ders Programı Seç", "", "PDF Dosyaları (*.pdf)")
        
        if file_path:
            # İşlem başladığında butonu bekleme moduna alıyoruz
            self.upload_btn.setText("\n⏳\n\nPDF Okunuyor, Lütfen Bekleyin...\n")
            self.upload_btn.repaint()
            
            # Gerçek OCR İşlemi
            ocr = OCRManager()
            success, result_data = ocr.parse_pdf(file_path)

            if not success:
                QMessageBox.warning(self, "Hata", result_data)
                self.upload_btn.setText("\n📄\n\nPDF veya Görsel Yükle\n(Sürükle bırak veya seçmek için tıkla)\n")
                return

            # Tabloyu temizle ve yeni verileri yerleştir
            self.table.setRowCount(0)
            added_count = 0
            
            for day, courses in result_data.items():
                for item in courses:
                    self._add_table_row(
                        day=day, 
                        start=item["start"], 
                        end=item["end"], 
                        course=item["course"], 
                        ctype=item["ctype"]
                    )
                    added_count += 1

            if added_count == 0:
                QMessageBox.information(self, "Uyarı", "PDF başarıyla okundu ancak uygun formatta ders bulunamadı.")
                self.upload_btn.setText("\n📄\n\nPDF veya Görsel Yükle\n(Sürükle bırak veya seçmek için tıkla)\n")
            else:
                self.editor_container.setVisible(True)
                self.upload_btn.setText(f"\n✅\n\nBaşarıyla {added_count} Ders Okundu\n(Yeni yüklemek için tıkla)\n")
                self.upload_btn.setStyleSheet("""
                    QPushButton { background-color: rgba(0, 229, 160, 0.1); color: #00e5a0; border: 2px solid #00e5a0; border-radius: 12px; padding: 15px; }
                """)

    def _delete_selected_row(self):
        current_row = self.table.currentRow()
        if current_row >= 0:
            self.table.removeRow(current_row)

    def _save_to_db(self):
        schedule_dict = { "Pazartesi": [], "Salı": [], "Çarşamba": [], "Perşembe": [], "Cuma": [], "Cumartesi": [], "Pazar": [] }

        for row in range(self.table.rowCount()):
            day = self.table.cellWidget(row, 0).currentText()
            start = self.table.cellWidget(row, 1).time().toString("HH:mm")
            end = self.table.cellWidget(row, 2).time().toString("HH:mm")
            
            course_item = self.table.item(row, 3)
            course = course_item.text().strip() if course_item and course_item.text().strip() else None
            
            ctype = self.table.cellWidget(row, 4).currentText()

            if not course: continue 
            
            schedule_dict[day].append({
                "course_id": course, 
                "start_time": start,
                "end_time": end,
                "type": "School_Class",
                "class_type": ctype
            })
        
        QMessageBox.information(self, "Başarılı", "Ders programınız şimdilik sadece arayüzde onaylandı! (Henüz veritabanına yazılmadı)")