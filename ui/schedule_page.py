import socket
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QFileDialog, QHeaderView,
    QMessageBox, QComboBox, QTimeEdit, QAbstractItemView, QListView,
    QLineEdit, QStackedWidget
)
from PyQt6.QtCore import Qt, QTime, QThread, pyqtSignal
from PyQt6.QtGui import QFont

from ocr_manager import OCRManager

# --- ARKA PLAN OCR İŞÇİSİ ---
class OCRWorker(QThread):
    finished_signal = pyqtSignal(bool, str, object)

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def run(self):
        from ocr_manager import OCRManager
        ocr = OCRManager()
        success, doc_type, result_data = ocr.parse_pdf(self.file_path)
        self.finished_signal.emit(success, doc_type, result_data)

class CourseEditWidget(QWidget):
    def __init__(self, code="", name="", group_id="", parent=None):
        super().__init__(parent)
        self.group_id = group_id
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 0, 5, 0)
        layout.setSpacing(4)

        self.code_edit = QLineEdit(code)
        self.code_edit.setPlaceholderText("KOD ZORUNLU")
        self.code_edit.setMinimumWidth(110)
        self.code_edit.setMaximumWidth(140)
        
        self.sep_label = QLabel("-")
        self.sep_label.setStyleSheet("color: #6b7280; font-weight: bold; font-size: 16px;")

        self.name_edit = QLineEdit(name)
        self.name_edit.setPlaceholderText("İsim (İsteğe Bağlı)")
        self.name_edit.setStyleSheet("""
            QLineEdit { background: transparent; border: none; color: #ffffff; }
            QLineEdit:focus { background-color: #1a1d26; border-radius: 4px; }
        """)

        layout.addWidget(self.code_edit)
        layout.addWidget(self.sep_label)
        layout.addWidget(self.name_edit)
        
        layout.setStretch(0, 0) 
        layout.setStretch(1, 0)
        layout.setStretch(2, 1)

        self.code_edit.textChanged.connect(self._update_style)
        self._update_style(code) 

    def _update_style(self, text):
        if not text.strip():
            self.code_edit.setStyleSheet("""
                QLineEdit { background: rgba(255, 92, 92, 0.15); border: 1px solid #ff5c5c; border-radius: 4px; color: #ff5c5c; font-weight: bold; }
                QLineEdit:focus { background-color: #1a1d26; }
            """)
        else:
            self.code_edit.setStyleSheet("""
                QLineEdit { background: transparent; border: none; color: #ffffff; font-weight: bold; }
                QLineEdit:focus { background-color: #1a1d26; border-radius: 4px; }
            """)


class SchedulePage(QWidget):
    def __init__(self, user_id, db_manager, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.db_manager = db_manager
        self._build_ui()

    def showEvent(self, event):
        super().showEvent(event)
        self._load_current_schedule()

    def _check_internet(self):
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except OSError:
            pass
        return False

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(28, 24, 28, 24)
        root.setSpacing(20)

        # Başlık
        hdr = QHBoxLayout()
        title = QLabel("Sabit Ders Programı")
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        title.setStyleSheet("color:#e4e6ed;")
        hdr.addWidget(title)
        hdr.addStretch()
        root.addLayout(hdr)

        self.stacked_widget = QStackedWidget()
        root.addWidget(self.stacked_widget)

        # --- MOD 0: GÖRÜNTÜLEME MODU ---
        self.view_container = QWidget()
        view_layout = QVBoxLayout(self.view_container)
        view_layout.setContentsMargins(0,0,0,0)
        
        self.view_title = QLabel("📌 Mevcut Aktif Programınız")
        self.view_title.setStyleSheet("color: #00e5a0; font-size: 16px; font-weight: bold;")
        view_layout.addWidget(self.view_title)

        self.view_table = QTableWidget(0, 5)
        self.view_table.setHorizontalHeaderLabels(["Gün", "Başlangıç", "Bitiş", "Ders Bilgisi", "Tip"])
        self.view_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.view_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers) 
        self.view_table.setStyleSheet("""
            QTableWidget { background-color: #111318; color: #e4e6ed; border: 1px solid #1e2130; border-radius: 8px; font-size: 16px; }
            QHeaderView::section { background-color: #1a1d26; color: #6b7280; padding: 10px; border: 1px solid #1e2130; font-weight: bold; }
        """)
        view_layout.addWidget(self.view_table)

        # Düzenle Butonu
        self.btn_recreate = QPushButton("✏️ Programı Düzenle / Yeni PDF Yükle")
        self.btn_recreate.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_recreate.setStyleSheet("background-color: #3b82f6; color: #ffffff; border-radius: 8px; padding: 12px; font-weight: bold;")
        self.btn_recreate.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        view_layout.addWidget(self.btn_recreate)

        # YENİ: SİL BUTONU
        self.btn_delete_schedule = QPushButton("🗑️ Programı Tamamen Sil")
        self.btn_delete_schedule.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_delete_schedule.setStyleSheet("""
            QPushButton { background-color: transparent; color: #ff5c5c; border: 1px solid #ff5c5c; border-radius: 8px; padding: 10px; font-weight: bold; margin-top: 5px; }
            QPushButton:hover { background-color: rgba(255, 92, 92, 0.1); }
        """)
        self.btn_delete_schedule.clicked.connect(self._delete_schedule_action)
        view_layout.addWidget(self.btn_delete_schedule)

        self.stacked_widget.addWidget(self.view_container)

        # --- MOD 1: YÜKLEME VE DÜZENLEME MODU ---
        self.edit_container = QWidget()
        edit_layout = QVBoxLayout(self.edit_container)
        edit_layout.setContentsMargins(0,0,0,0)

        top_edit_row = QHBoxLayout()
        
        self.btn_go_back = QPushButton("⬅️ İptal / Geri Dön")
        self.btn_go_back.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_go_back.setStyleSheet("""
            QPushButton { background-color: #2e3248; color: #e4e6ed; border-radius: 6px; padding: 8px 16px; font-weight: bold; }
            QPushButton:hover { background-color: #3b405a; }
        """)
        self.btn_go_back.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        top_edit_row.addWidget(self.btn_go_back)
        
        top_edit_row.addSpacing(20)
        
        name_lbl = QLabel("Program Adı:")
        name_lbl.setStyleSheet("color: #9ca3af; font-size: 14px; font-weight: bold;")
        top_edit_row.addWidget(name_lbl)
        
        self.schedule_name_input = QLineEdit("(Güncel Sabit Program)")
        self.schedule_name_input.setPlaceholderText("Örn: 2026 Bahar Dönemi")
        self.schedule_name_input.setMinimumWidth(250)
        self.schedule_name_input.setStyleSheet("""
            QLineEdit { background-color: #1a1d26; color: #00e5a0; border: 1px solid #2e3248; border-radius: 6px; padding: 8px; font-size: 14px; font-weight: bold; }
            QLineEdit:focus { border: 1px solid #00e5a0; }
        """)
        top_edit_row.addWidget(self.schedule_name_input)
        
        top_edit_row.addStretch()
        edit_layout.addLayout(top_edit_row)

        self.upload_btn = QPushButton("\n📄\n\nPDF veya Görsel Yükle\n(Mevcut programın üzerine yazar)\n")
        self.upload_btn.setFont(QFont("Segoe UI", 12))
        self.upload_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.upload_btn.setStyleSheet("""
            QPushButton { background-color: #1a1d26; color: #6b7280; border: 2px dashed #2e3248; border-radius: 12px; padding: 30px; }
            QPushButton:hover { background-color: #1e2130; border: 2px dashed #00e5a0; color: #e4e6ed; }
        """)
        self.upload_btn.clicked.connect(self._import_file)
        edit_layout.addWidget(self.upload_btn)

        self.editor_wrapper = QWidget()
        editor_inner_layout = QVBoxLayout(self.editor_wrapper)
        editor_inner_layout.setContentsMargins(0,0,0,0)

        tools_row = QHBoxLayout()
        ocr_title = QLabel("📝 Manuel Düzenleme Alanı")
        ocr_title.setStyleSheet("color:#00e5a0; font-weight:bold; font-size:14px;")
        tools_row.addWidget(ocr_title)
        tools_row.addStretch()

        add_row_btn = QPushButton("+ Satır Ekle")
        add_row_btn.setStyleSheet("background:#2e3248; color:#e4e6ed; border-radius:6px; padding:8px 16px; font-weight: bold;")
        add_row_btn.clicked.connect(lambda: self._add_table_row()) 
        del_row_btn = QPushButton("- Seçili Satırı Sil")
        del_row_btn.setStyleSheet("background:#ff5c5c; color:#111318; border-radius:6px; padding:8px 16px; font-weight: bold;")
        del_row_btn.clicked.connect(self._delete_selected_row)
        tools_row.addWidget(add_row_btn)
        tools_row.addWidget(del_row_btn)
        editor_inner_layout.addLayout(tools_row)

        info_label = QLabel("💡 Kural: Sol taraftaki 'Ders Kodu' alanının doldurulması zorunludur. Sağ taraftaki 'Ders Adı' alanı ise isteğe bağlıdır.")
        info_label.setStyleSheet("color: #9ca3af; font-size: 13px; font-style: italic;")
        editor_inner_layout.addWidget(info_label)

        self.table = QTableWidget(0, 5) 
        self.table.setHorizontalHeaderLabels(["Gün", "Başlangıç", "Bitiş", "Ders Bilgisi (Kod - İsim)", "Tip"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(0, 160) 
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(1, 120)  
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(2, 120)  
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(4, 160) 
        self.table.verticalHeader().setDefaultSectionSize(60)
        self.table.verticalHeader().setVisible(False) 
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setStyleSheet("""
            QTableWidget { background-color: #111318; color: #e4e6ed; gridline-color: #1e2130; border: 1px solid #1e2130; border-radius: 8px; font-size: 18px; }
            QHeaderView::section { background-color: #1a1d26; color: #6b7280; padding: 10px; border: 1px solid #1e2130; font-weight: bold; font-size: 14px; }
            QTableWidget::item:selected { background-color: rgba(0, 229, 160, 0.15); border-top: 1px solid #00e5a0; border-bottom: 1px solid #00e5a0; color: #e4e6ed; }
            QComboBox, QTimeEdit { background-color: #1a1d26; color: #e4e6ed; border: 1px solid #2e3248; border-radius: 6px; font-size: 16px; padding: 4px 10px; margin: 4px; }
            QComboBox::drop-down, QTimeEdit::up-button, QTimeEdit::down-button { border: none; }
            QComboBox QAbstractItemView { background-color: #1a1d26; color: #e4e6ed; border: 1px solid #00e5a0; border-radius: 6px; selection-background-color: #00e5a0; selection-color: #111318; outline: none; }
            QComboBox QAbstractItemView::item { min-height: 35px; padding-left: 10px; }
        """)
        editor_inner_layout.addWidget(self.table)

        self.save_btn = QPushButton("Veritabanına Kaydet")
        self.save_btn.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold)) 
        self.save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.save_btn.setStyleSheet("""
            QPushButton { background-color: #00e5a0; color: #111318; border-radius: 8px; padding: 16px; }
            QPushButton:hover { background-color: #00c88c; }
        """)
        self.save_btn.clicked.connect(self._save_to_db)
        editor_inner_layout.addWidget(self.save_btn)

        edit_layout.addWidget(self.editor_wrapper)
        self.editor_wrapper.setVisible(False)
        self.stacked_widget.addWidget(self.edit_container)

    def _load_current_schedule(self):
        if not self._check_internet():
            self.stacked_widget.setCurrentIndex(1) 
            self.btn_go_back.setVisible(False) # İnternet yoksa geri dön butonunu gizle
            return

        success, data = self.db_manager.get_schedule(self.user_id)
        if success and isinstance(data, dict):
            self.btn_go_back.setVisible(True) # Veri varsa geri dön butonu görünsün
            self.view_table.setRowCount(0)
            self.table.setRowCount(0) 
            
            saved_name = data.get("schedule_name", "").strip()
            if not saved_name:
                saved_name = "(Güncel Sabit Program)"
                
            self.view_title.setText(f"📌 {saved_name}")
            self.schedule_name_input.setText(saved_name)
            
            routine = data.get("weekly_routine", {})
            days_order = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
            
            for day in days_order:
                for course in routine.get(day, []):
                    r_idx = self.view_table.rowCount()
                    self.view_table.insertRow(r_idx)
                    
                    c_name = course.get("course_name", "")
                    c_id = course.get("course_id", "")
                    display_text = f"{c_id.upper()} - {c_name}" if c_name else c_id.upper()

                    self.view_table.setItem(r_idx, 0, QTableWidgetItem(day))
                    self.view_table.setItem(r_idx, 1, QTableWidgetItem(course.get("start_time", "")))
                    self.view_table.setItem(r_idx, 2, QTableWidgetItem(course.get("end_time", "")))
                    self.view_table.setItem(r_idx, 3, QTableWidgetItem(display_text))
                    self.view_table.setItem(r_idx, 4, QTableWidgetItem(course.get("class_type", "")))

                    self._add_table_row(
                        day=day, 
                        start=course.get("start_time", "00:00"), 
                        end=course.get("end_time", "00:00"), 
                        course=display_text, 
                        ctype=course.get("class_type", "Teorik")
                    )
            
            self.editor_wrapper.setVisible(True) 
            self.stacked_widget.setCurrentIndex(0) 
        else:
            self.btn_go_back.setVisible(False) # Program yoksa geri dönemesin
            self.stacked_widget.setCurrentIndex(1) 

    def _sync_course_realtime(self, source_widget, is_code_change):
        group_id = source_widget.group_id
        if not group_id or group_id.startswith("manual_"): return
        new_text = source_widget.code_edit.text() if is_code_change else source_widget.name_edit.text()

        for row in range(self.table.rowCount()):
            target_widget = self.table.cellWidget(row, 3)
            if isinstance(target_widget, CourseEditWidget) and target_widget != source_widget:
                if target_widget.group_id == group_id:
                    target_edit = target_widget.code_edit if is_code_change else target_widget.name_edit
                    target_edit.blockSignals(True)
                    target_edit.setText(new_text)
                    target_edit.blockSignals(False)
                    if is_code_change:
                        target_widget._update_style(new_text)

    def _add_table_row(self, day="Pazartesi", start="09:00", end="10:00", course="", ctype="Teorik"):
        row_idx = self.table.rowCount()
        self.table.insertRow(row_idx)

        day_cb = QComboBox()
        day_cb.setView(QListView())
        day_cb.addItems(["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"])
        day_cb.setCurrentText(day)
        self.table.setCellWidget(row_idx, 0, day_cb)

        start_te = QTimeEdit(QTime.fromString(start, "HH:mm"))
        start_te.setDisplayFormat("HH:mm")
        self.table.setCellWidget(row_idx, 1, start_te)

        end_te = QTimeEdit(QTime.fromString(end, "HH:mm"))
        end_te.setDisplayFormat("HH:mm")
        self.table.setCellWidget(row_idx, 2, end_te)

        code_part = ""
        name_part = ""
        if course:
            if " - " in course:
                parts = course.split(" - ", 1)
                code_part = parts[0].strip()
                name_part = parts[1].strip()
            else:
                code_part = course.strip()
                
        group_id = code_part if code_part else f"manual_{row_idx}"
        
        course_widget = CourseEditWidget(code=code_part, name=name_part, group_id=group_id)
        course_widget.code_edit.textEdited.connect(lambda text, cw=course_widget: self._sync_course_realtime(cw, is_code_change=True))
        course_widget.name_edit.textEdited.connect(lambda text, cw=course_widget: self._sync_course_realtime(cw, is_code_change=False))
        self.table.setCellWidget(row_idx, 3, course_widget)

        type_cb = QComboBox()
        type_cb.setView(QListView())
        type_cb.addItems(["Teorik", "Uygulamalı"])
        type_cb.setCurrentText(ctype)
        self.table.setCellWidget(row_idx, 4, type_cb)

    def _import_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Ders Programı Seç", "", "PDF veya Resim (*.pdf *.png *.jpg *.jpeg)")
        if file_path:
            self.upload_btn.setText("\n⏳\n\nBelge OCR ve AI yardımı ile okunuyor...\nLütfen bekleyin.\n")
            self.upload_btn.setEnabled(False)

            self.upload_btn.setStyleSheet("""
                QPushButton { 
                    background-color: rgba(245, 158, 11, 0.15); 
                    color: #f59e0b; 
                    border: 2px dashed #f59e0b; 
                    border-radius: 12px; 
                    padding: 30px; 
                }
            """)

            self.upload_btn.repaint()
            
            self.ocr_worker = OCRWorker(file_path)
            self.ocr_worker.finished_signal.connect(self._on_import_finished)
            self.ocr_worker.start()

    def _on_import_finished(self, success, doc_type, result_data):
        self.upload_btn.setEnabled(True)

        self.upload_btn.setStyleSheet("""
            QPushButton { background-color: #1a1d26; color: #6b7280; border: 2px dashed #2e3248; border-radius: 12px; padding: 30px; }
            QPushButton:hover { background-color: #1e2130; border: 2px dashed #00e5a0; color: #e4e6ed; }
        """)

        if not success:
            QMessageBox.warning(self, "Hata", result_data)
            self.upload_btn.setText("\n📄\n\nPDF veya Görsel Yükle\n(Mevcut programın üzerine yazar)\n")
            return

        if doc_type == "exam":
            QMessageBox.warning(self, "Yanlış Menü", "Yüklediğiniz dosya bir 'Sınav Takvimi'.\nLütfen bu dosyayı soldaki 'Notlar' menüsünden yükleyin.")
            self.upload_btn.setText("\n📄\n\nPDF veya Görsel Yükle\n(Mevcut programın üzerine yazar)\n")
            return

        self.table.setRowCount(0)
        added_count = 0
        
        for day, courses in result_data.items():
            for item in courses:
                self._add_table_row(
                    day=day, start=item["start"], end=item["end"], 
                    course=item["course"], ctype=item["ctype"]
                )
                added_count += 1

        if added_count == 0:
            QMessageBox.information(self, "Uyarı", "Belge okundu ancak uygun formatta ders bulunamadı.")
            self.upload_btn.setText("\n📄\n\nPDF veya Görsel Yükle\n(Mevcut programın üzerine yazar)\n")
        else:
            self.editor_wrapper.setVisible(True)
            self.upload_btn.setText(f"\n✅\n\nBaşarıyla {added_count} Ders Okundu\n(Yeni yüklemek için tıkla)\n")

    def _delete_selected_row(self):
        current_row = self.table.currentRow()
        if current_row >= 0:
            self.table.removeRow(current_row)

    def _save_to_db(self):
        if not self._check_internet():
            QMessageBox.critical(self, "Bağlantı Hatası", "İnternet bağlantısı kurulamadı!\nLütfen bağlantınızı kontrol edip tekrar deneyin.")
            return
            
        schedule_name = self.schedule_name_input.text().strip()
        if not schedule_name:
            schedule_name = "(Güncel Sabit Program)"

        self.save_btn.setText("Kaydediliyor...")
        self.save_btn.setEnabled(False)
        self.save_btn.repaint()

        schedule_dict = { "Pazartesi": [], "Salı": [], "Çarşamba": [], "Perşembe": [], "Cuma": [], "Cumartesi": [], "Pazar": [] }
        course_hours_dict = {} 
        valid_courses_count = 0

        for row in range(self.table.rowCount()):
            course_widget = self.table.cellWidget(row, 3)
            if not course_widget: continue

            course_code = course_widget.code_edit.text().strip()
            course_name = course_widget.name_edit.text().strip()

            if not course_code and not course_name:
                continue

            if not course_code:
                QMessageBox.critical(self, "Eksik Bilgi", f"{row+1}. satırda DERS KODU BOŞ BIRAKILAMAZ!\n\nLütfen ilgili satırdaki kırmızı uyarı veren kodu doldurun veya silin.")
                self.save_btn.setText("Veritabanına Kaydet")
                self.save_btn.setEnabled(True)
                return
            
            valid_courses_count += 1
            
            clean_id = course_code.replace(" ", "").lower()
            
            day = self.table.cellWidget(row, 0).currentText()
            start_time = self.table.cellWidget(row, 1).time()
            end_time = self.table.cellWidget(row, 2).time()
            ctype = self.table.cellWidget(row, 4).currentText()
            
            mins_diff = start_time.secsTo(end_time) // 60
            hours = round(mins_diff / 50) if mins_diff > 0 else 1

            if clean_id in course_hours_dict:
                course_hours_dict[clean_id]["hours"] += hours
            else:
                course_hours_dict[clean_id] = {"name": course_name, "hours": hours}
            
            schedule_dict[day].append({
                "course_id": clean_id,
                "course_name": course_name,
                "start_time": start_time.toString("HH:mm"),
                "end_time": end_time.toString("HH:mm"),
                "type": "School_Class",
                "class_type": ctype
            })
            
        if valid_courses_count == 0:
            QMessageBox.warning(self, "Boş Tablo", "Kaydedilecek hiçbir ders bulunamadı!")
            self.save_btn.setText("Veritabanına Kaydet")
            self.save_btn.setEnabled(True)
            return
        
        success, msg = self.db_manager.save_full_schedule(self.user_id, schedule_name, schedule_dict, course_hours_dict)
        
        self.save_btn.setText("Veritabanına Kaydet")
        self.save_btn.setEnabled(True)

        if success:
            QMessageBox.information(self, "Başarılı", msg)
            self._load_current_schedule() 
        else:
            QMessageBox.critical(self, "Hata", msg)

    # --- YENİ EKLENEN SİLME İŞLEMİ ---
    def _delete_schedule_action(self):
        if not self._check_internet():
            QMessageBox.critical(self, "Bağlantı Hatası", "İnternet bağlantısı yok! Lütfen bağlantınızı kontrol edin.")
            return
            
        reply = QMessageBox.question(
            self, 'Programı Sil', 
            "Mevcut ders programını tamamen silmek istediğinize emin misiniz?\n\n(Bu işlem programdaki tüm dersleri 'Arşivlenmiş' olarak işaretleyecektir.)",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            success, msg = self.db_manager.delete_schedule(self.user_id)
            if success:
                QMessageBox.information(self, "Başarılı", "Program başarıyla silindi ve dersler arşive aktarıldı.")
                # Tabloları temizle ve Yükleme moduna geç
                self.view_table.setRowCount(0)
                self.table.setRowCount(0)
                self.editor_wrapper.setVisible(False)
                self.upload_btn.setText("\n📄\n\nPDF veya Görsel Yükle\n(Yeni program yüklemek için tıkla)\n")
                self.stacked_widget.setCurrentIndex(1)
                self.btn_go_back.setVisible(False) # Artık geri dönebileceği bir program yok
            else:
                QMessageBox.critical(self, "Hata", msg)