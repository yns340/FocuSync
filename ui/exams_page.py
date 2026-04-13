import socket
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QFileDialog, QHeaderView,
    QMessageBox, QComboBox, QTimeEdit, QAbstractItemView, QListView,
    QLineEdit, QStackedWidget, QCheckBox, QSpinBox, QDateEdit
)
from PyQt6.QtCore import Qt, QTime, QDate, pyqtSignal
from PyQt6.QtGui import QFont

# --- 1. ÖZEL DERS BİLGİSİ WIDGET'I ---
class ExamEditWidget(QWidget):
    def __init__(self, code="", name="", parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        self.code_edit = QLineEdit(code)
        self.code_edit.setPlaceholderText("KOD")
        self.code_edit.setMinimumWidth(75) 
        self.code_edit.setMaximumWidth(95)
        
        self.sep_label = QLabel("-")
        self.sep_label.setStyleSheet("color: #6b7280; font-weight: bold; font-size: 16px;")

        self.name_edit = QLineEdit(name)
        self.name_edit.setPlaceholderText("Ders Adı")
        self.name_edit.setStyleSheet("""
            QLineEdit { background: transparent; border: none; color: #ffffff; }
            QLineEdit:focus { background-color: #1a1d26; border-radius: 4px; }
        """)

        layout.addWidget(self.code_edit)
        layout.addWidget(self.sep_label)
        layout.addWidget(self.name_edit)
        
        layout.setStretch(2, 1)
        self.code_edit.textChanged.connect(self._update_style)
        self._update_style(code) 

    def _update_style(self, text):
        if not text.strip():
            self.code_edit.setStyleSheet("QLineEdit { background: rgba(255, 92, 92, 0.15); border: 1px solid #ff5c5c; border-radius: 4px; color: #ff5c5c; font-weight: bold; text-transform: uppercase;}")
        else:
            self.code_edit.setStyleSheet("QLineEdit { background: transparent; border: none; color: #ffffff; font-weight: bold; text-transform: uppercase;}")

# --- 2. YENİ AKILLI SINAV TÜRÜ WIDGET'I ---
class ExamTypeWidget(QWidget):
    typeChanged = pyqtSignal()

    def __init__(self, full_type="Vize 1", parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        self.type_cb = QComboBox()
        self.type_cb.addItems(["Vize", "Final", "Bütünleme", "Quiz", "Ödev", "Proje"])
        self.type_cb.setStyleSheet("""
            QComboBox { background-color: #1a1d26; color: #e4e6ed; border: 1px solid #2e3248; border-radius: 6px; padding: 4px; font-size: 14px; }
            QComboBox::drop-down { border: none; }
            QComboBox QAbstractItemView { background-color: #1a1d26; color: #e4e6ed; selection-background-color: #00e5a0; selection-color: #111318; outline: none; }
        """)
        
        self.num_sb = QSpinBox()
        self.num_sb.setRange(1, 10)
        self.num_sb.setFixedWidth(40)
        self.num_sb.setStyleSheet("""
            QSpinBox { background-color: #1a1d26; color: #00e5a0; border: 1px solid #2e3248; border-radius: 6px; padding: 4px; font-size: 14px; font-weight: bold; }
            QSpinBox::up-button, QSpinBox::down-button { width: 0px; height: 0px; border: none; }
        """)
        
        layout.addWidget(self.type_cb)
        layout.addWidget(self.num_sb)
        
        self.set_full_type(full_type)
        
        self.type_cb.currentTextChanged.connect(self._on_change)
        self.num_sb.valueChanged.connect(self._on_change)

    def _toggle_num(self):
        t = self.type_cb.currentText()
        if t in ["Final", "Bütünleme"]:
            self.num_sb.setEnabled(False)
            self.num_sb.hide()
        else:
            self.num_sb.setEnabled(True)
            self.num_sb.show()

    def get_full_type(self):
        t = self.type_cb.currentText()
        if t in ["Final", "Bütünleme"]:
            return t
        return f"{t} {self.num_sb.value()}"

    def set_full_type(self, full_type):
        self.type_cb.blockSignals(True)
        self.num_sb.blockSignals(True)
        
        parts = full_type.rsplit(' ', 1)
        if len(parts) == 2 and parts[1].isdigit():
            base_type = parts[0]
            num = int(parts[1])
        else:
            base_type = full_type
            num = 1
            
        if base_type in ["Vize", "Final", "Bütünleme", "Quiz", "Ödev", "Proje"]:
            self.type_cb.setCurrentText(base_type)
        else:
            self.type_cb.setCurrentText("Vize")
            
        self.num_sb.setValue(num)
        self._toggle_num()
        
        self.type_cb.blockSignals(False)
        self.num_sb.blockSignals(False)

    def _on_change(self, *args):
        self._toggle_num()
        self.typeChanged.emit()

# --- 3. ANA SAYFA MİMARİSİ ---
class ExamsPage(QWidget):
    def __init__(self, user_id, db_manager, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.db_manager = db_manager
        self._build_ui()

    def showEvent(self, event):
        super().showEvent(event)
        self._load_current_exams()

    def _check_internet(self):
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except OSError: pass
        return False

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(28, 24, 28, 24)
        root.setSpacing(20)

        header_layout = QVBoxLayout()
        header_layout.setSpacing(5)
        
        title = QLabel("Notlar") 
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        title.setStyleSheet("color:#e4e6ed;")
        header_layout.addWidget(title)
        
        self.nearest_exam_lbl = QLabel("💡 Sistem taranıyor...")
        self.nearest_exam_lbl.setStyleSheet("color: #9ca3af; font-size: 14px; font-style: italic;")
        header_layout.addWidget(self.nearest_exam_lbl)
        
        root.addLayout(header_layout)

        self.stacked_widget = QStackedWidget()
        root.addWidget(self.stacked_widget)

        # --- MOD 0: GÖRÜNTÜLEME ---
        self.view_container = QWidget()
        view_layout = QVBoxLayout(self.view_container)
        view_layout.setContentsMargins(0,0,0,0)
        
        self.view_title = QLabel("📌 (Güncel Notlar)")
        self.view_title.setStyleSheet("color: #00e5a0; font-size: 16px; font-weight: bold;")
        view_layout.addWidget(self.view_title)

        self.view_table = QTableWidget(0, 6)
        self.view_table.setHorizontalHeaderLabels(["Tarih", "Saat", "Ders Bilgisi", "Tür", "Salon", "Not"])
        
        self.view_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.view_table.setColumnWidth(0, 130) 
        self.view_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        self.view_table.setColumnWidth(1, 90)  
        self.view_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch) 
        self.view_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        self.view_table.setColumnWidth(3, 140) 
        self.view_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        self.view_table.setColumnWidth(4, 110) 
        self.view_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)
        self.view_table.setColumnWidth(5, 75)  
        
        self.view_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.view_table.setStyleSheet("QTableWidget { background-color: #111318; color: #e4e6ed; border: 1px solid #1e2130; border-radius: 8px; }")
        view_layout.addWidget(self.view_table)

        self.btn_recreate = QPushButton("✏️ Notları Düzenle / Yeni Sınav Takvimi Yükle")
        self.btn_recreate.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_recreate.setStyleSheet("background-color: #3b82f6; color: #ffffff; border-radius: 8px; padding: 12px; font-weight: bold;")
        self.btn_recreate.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        view_layout.addWidget(self.btn_recreate)

        self.btn_delete_exams = QPushButton("🗑️ Tüm Notları Sil")
        self.btn_delete_exams.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_delete_exams.setStyleSheet("""
            QPushButton { background-color: transparent; color: #ff5c5c; border: 1px solid #ff5c5c; border-radius: 8px; padding: 10px; font-weight: bold; margin-top: 5px; }
            QPushButton:hover { background-color: rgba(255, 92, 92, 0.1); }
        """)
        self.btn_delete_exams.clicked.connect(self._delete_exams_action)
        view_layout.addWidget(self.btn_delete_exams)

        self.stacked_widget.addWidget(self.view_container)

        # --- MOD 1: DÜZENLEME ---
        self.edit_container = QWidget()
        edit_layout = QVBoxLayout(self.edit_container)
        edit_layout.setContentsMargins(0,0,0,0)

        top_row = QHBoxLayout()
        self.btn_go_back = QPushButton("⬅️ İptal / Geri Dön")
        self.btn_go_back.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_go_back.setStyleSheet("background-color: #2e3248; color: #e4e6ed; border-radius: 6px; padding: 8px 16px; font-weight: bold;")
        self.btn_go_back.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        top_row.addWidget(self.btn_go_back)
        top_row.addSpacing(20)

        name_lbl = QLabel("Başlık:")
        name_lbl.setStyleSheet("color: #9ca3af; font-size: 14px; font-weight: bold;")
        top_row.addWidget(name_lbl)
        
        self.exam_name_input = QLineEdit("(Güncel Notlar)")
        self.exam_name_input.setMinimumWidth(250)
        self.exam_name_input.setStyleSheet("QLineEdit { background-color: #1a1d26; color: #00e5a0; border: 1px solid #2e3248; border-radius: 6px; padding: 8px; font-weight: bold; }")
        top_row.addWidget(self.exam_name_input)
        top_row.addStretch()
        edit_layout.addLayout(top_row)

        self.upload_btn = QPushButton("\n📄\n\nSınav Takvimi Yükle\n(Mevcut kayıtların üzerine eklenir)\n")
        self.upload_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.upload_btn.setStyleSheet("QPushButton { background-color: #1a1d26; color: #6b7280; border: 2px dashed #2e3248; border-radius: 12px; padding: 30px; }")
        self.upload_btn.clicked.connect(self._import_file)
        edit_layout.addWidget(self.upload_btn)

        self.editor_wrapper = QWidget()
        self.editor_layout = QVBoxLayout(self.editor_wrapper)
        self.editor_layout.setContentsMargins(0,0,0,0)

        tools = QHBoxLayout()
        ocr_title = QLabel("📝 Manuel Düzenleme Alanı")
        ocr_title.setStyleSheet("color:#00e5a0; font-weight:bold; font-size:14px;")
        tools.addWidget(ocr_title)
        tools.addStretch()
        
        add_btn = QPushButton("+ Sınav Ekle")
        add_btn.setStyleSheet("background:#2e3248; color:#e4e6ed; border-radius:6px; padding:8px 16px; font-weight: bold;")
        add_btn.clicked.connect(lambda: self._add_table_row())
        
        del_btn = QPushButton("- Sil")
        del_btn.setStyleSheet("background:#ff5c5c; color:#111318; border-radius:6px; padding:8px 16px; font-weight: bold;")
        del_btn.clicked.connect(self._delete_selected_row)
        
        tools.addWidget(add_btn); tools.addWidget(del_btn)
        self.editor_layout.addLayout(tools)

        info_label = QLabel("💡 Akıllı Seçim: Sistem, yeni eklenen sınavlardan aktif derslerinizle eşleşenleri otomatik seçer (☑). Yalnızca seçili olanlar kaydedilir.")
        info_label.setStyleSheet("color: #9ca3af; font-size: 13px; font-style: italic;")
        self.editor_layout.addWidget(info_label)

        self.table = QTableWidget(0, 7)
        self.table.setHorizontalHeaderLabels(["Seç", "Tarih (DD.MM.YY)", "Saat", "Ders Bilgisi", "Sınav Türü", "Salon", "Not"])
        
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(0, 45) 
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(1, 145) 
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(2, 95)  
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch) 
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(4, 160) 
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(5, 110) 
        self.table.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(6, 75) 
        
        self.table.verticalHeader().setDefaultSectionSize(60)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        
        self.table.setStyleSheet("""
            QTableWidget { background-color: #111318; color: #e4e6ed; gridline-color: #1e2130; border: 1px solid #1e2130; border-radius: 8px; font-size: 18px; }
            QHeaderView::section { background-color: #1a1d26; color: #6b7280; padding: 10px; border: 1px solid #1e2130; font-weight: bold; font-size: 14px; }
            QTableWidget::item:selected { background-color: rgba(0, 229, 160, 0.15); border-top: 1px solid #00e5a0; border-bottom: 1px solid #00e5a0; color: #e4e6ed; }
            QLineEdit { background-color: #1a1d26; color: #e4e6ed; border: 1px solid #2e3248; border-radius: 6px; font-size: 14px; padding: 4px; margin: 4px; }
            QTimeEdit, QDateEdit { background-color: #1a1d26; color: #e4e6ed; border: 1px solid #2e3248; border-radius: 6px; font-size: 16px; padding: 4px; margin: 4px; }
            QTimeEdit::up-button, QTimeEdit::down-button, QDateEdit::drop-down { border: none; }
        """)
        self.editor_layout.addWidget(self.table)

        self.save_btn = QPushButton("Seçilenleri Kaydet")
        self.save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.save_btn.setStyleSheet("background-color: #00e5a0; color: #111318; border-radius: 8px; padding: 16px; font-weight: bold; font-size: 14px;")
        self.save_btn.clicked.connect(self._save_to_db)
        self.editor_layout.addWidget(self.save_btn)

        edit_layout.addWidget(self.editor_wrapper)
        self.editor_wrapper.setVisible(False)
        self.stacked_widget.addWidget(self.edit_container)

    def _calculate_nearest_exam(self, exams_list):
        if not exams_list:
            self.nearest_exam_lbl.setText("💡 Yaklaşan sınavınız bulunmamaktadır.")
            self.nearest_exam_lbl.setStyleSheet("color: #6b7280; font-size: 14px; font-style: italic;")
            return

        today = QDate.currentDate()
        nearest_exam = None
        min_days = 9999

        for ex in exams_list:
            date_str = ex.get("exam_date", "")
            parsed_date = QDate.fromString(date_str, "dd.MM.yyyy")
            if not parsed_date.isValid():
                parsed_date = QDate.fromString(f"{date_str}.{today.year()}", "dd.MM.yyyy")
                
            if parsed_date.isValid() and today.daysTo(parsed_date) >= 0:
                days_diff = today.daysTo(parsed_date)
                if days_diff < min_days:
                    min_days = days_diff
                    nearest_exam = ex

        if nearest_exam:
            days_text = "BUGÜN!" if min_days == 0 else f"{min_days} gün kaldı"
            c_code = nearest_exam.get('course_id', '').upper()
            e_type = nearest_exam.get('exam_type', '')
            e_date = nearest_exam.get('exam_date', '')
            self.nearest_exam_lbl.setText(f"🔥 En Yakın Sınav: {c_code} ({e_type}) — {e_date} ⏳ {days_text}")
            self.nearest_exam_lbl.setStyleSheet("color: #00e5a0; font-size: 15px; font-weight: bold;")
        else:
            self.nearest_exam_lbl.setText("💡 Yaklaşan sınavınız bulunmamaktadır.")
            self.nearest_exam_lbl.setStyleSheet("color: #6b7280; font-size: 14px; font-style: italic;")

    def _load_current_exams(self):
        if not self._check_internet():
            self.stacked_widget.setCurrentIndex(1)
            self.btn_go_back.setVisible(False)
            self.nearest_exam_lbl.setText("Bağlantı koptu, veriler okunamıyor.")
            return

        success, data = self.db_manager.get_exam_schedule(self.user_id)
        
        self.view_table.setRowCount(0)
        self.table.setRowCount(0)
        
        if success and isinstance(data, dict) and data.get("exams"):
            self.btn_go_back.setVisible(True) # Veri varsa Geri Dön butonu görünür
            saved_name = data.get("exam_schedule_name", "").strip()
            if not saved_name: saved_name = "(Güncel Notlar)"
            self.view_title.setText(f"📌 {saved_name}")
            self.exam_name_input.setText(saved_name)

            exams = data.get("exams", [])
            self._calculate_nearest_exam(exams)

            for ex in exams:
                # Görüntüleme Tablosu
                r = self.view_table.rowCount()
                self.view_table.insertRow(r)
                display_text = f"{ex.get('course_id', '').upper()} - {ex.get('course_name', '')}"
                self.view_table.setItem(r, 0, QTableWidgetItem(ex.get("exam_date", "")))
                self.view_table.setItem(r, 1, QTableWidgetItem(ex.get("exam_time", "")))
                self.view_table.setItem(r, 2, QTableWidgetItem(display_text))
                self.view_table.setItem(r, 3, QTableWidgetItem(ex.get("exam_type", "")))
                self.view_table.setItem(r, 4, QTableWidgetItem(ex.get("exam_room", "")))
                self.view_table.setItem(r, 5, QTableWidgetItem(ex.get("exam_grade", "")))

                # Düzenleme Tablosu
                self._add_table_row(ex.get("exam_date", ""), ex.get("exam_time", "10:00"),
                                   ex.get("course_id", ""), ex.get("course_name", ""),
                                   ex.get("exam_type", "Vize 1"), ex.get("exam_room", ""), 
                                   ex.get("exam_grade", ""), is_selected=True)
            
            self.editor_wrapper.setVisible(True)
            self.stacked_widget.setCurrentIndex(0)
        else:
            self.btn_go_back.setVisible(False) # Veri yoksa Geri Dön butonu GİZLENİR
            self.view_title.setText("📌 (Güncel Notlar)")
            self.exam_name_input.setText("(Güncel Notlar)")
            self.nearest_exam_lbl.setText("💡 Yaklaşan sınavınız bulunmamaktadır.")
            self.nearest_exam_lbl.setStyleSheet("color: #6b7280; font-size: 14px; font-style: italic;")
            self.editor_wrapper.setVisible(False)
            
            # Veri yoksa doğrudan düzenleme/yükleme sekmesine git
            self.stacked_widget.setCurrentIndex(1)

    def _on_code_changed(self, cw):
        code = cw.code_edit.text().strip().lower()
        if not code: return
        for r in range(self.table.rowCount()):
            other_cw = self.table.cellWidget(r, 3)
            if other_cw and other_cw != cw and other_cw.code_edit.text().strip().lower() == code:
                existing_name = other_cw.name_edit.text().strip()
                if existing_name:
                    cw.name_edit.blockSignals(True)
                    cw.name_edit.setText(existing_name)
                    cw.name_edit.blockSignals(False)
                    break

    def _on_name_changed(self, cw):
        code = cw.code_edit.text().strip().lower()
        name = cw.name_edit.text().strip()
        if not code: return
        for r in range(self.table.rowCount()):
            other_cw = self.table.cellWidget(r, 3)
            if other_cw and other_cw != cw and other_cw.code_edit.text().strip().lower() == code:
                other_cw.name_edit.blockSignals(True)
                other_cw.name_edit.setText(name)
                other_cw.name_edit.blockSignals(False)

    def _on_type_changed(self, type_w, cw):
        code = cw.code_edit.text().strip().lower()
        current_full = type_w.get_full_type()
        
        if not code:
            type_w.setProperty("prev_text", current_full)
            return

        for r in range(self.table.rowCount()):
            other_cw = self.table.cellWidget(r, 3)
            other_tw = self.table.cellWidget(r, 4)
            if other_cw and other_tw and other_tw != type_w:
                if other_cw.code_edit.text().strip().lower() == code:
                    if other_tw.get_full_type() == current_full:
                        QMessageBox.warning(self, "Kritik Çakışma!", f"'{code.upper()}' dersi için '{current_full}' zaten eklenmiş!\nLütfen farklı bir sınav türü belirleyin.")
                        
                        prev = type_w.property("prev_text")
                        if not prev: prev = "Vize 1"
                        
                        type_w.blockSignals(True)
                        type_w.set_full_type(prev)
                        type_w.blockSignals(False)
                        return

        type_w.setProperty("prev_text", current_full)

    def _get_available_exam_type(self, course_code, base_type="Vize"):
        if base_type in ["Final", "Bütünleme"]:
            return base_type
            
        used_nums = []
        for r in range(self.table.rowCount()):
            cw = self.table.cellWidget(r, 3)
            tw = self.table.cellWidget(r, 4)
            if cw and tw and cw.code_edit.text().strip().lower() == course_code.lower():
                ft = tw.get_full_type()
                parts = ft.rsplit(' ', 1)
                if len(parts) == 2 and parts[0] == base_type and parts[1].isdigit():
                    used_nums.append(int(parts[1]))
        
        num = 1
        while num in used_nums:
            num += 1
        return f"{base_type} {num}"

    def _add_table_row(self, date="", time="10:00", code="", name="", etype="Vize 1", room="", grade="", is_selected=True):
        r = self.table.rowCount()
        self.table.insertRow(r)
        
        chk_container = QWidget()
        chk_layout = QHBoxLayout(chk_container)
        chk_layout.setContentsMargins(0, 0, 0, 0)
        chk_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        chk = QCheckBox()
        chk.setChecked(is_selected)
        chk.setCursor(Qt.CursorShape.PointingHandCursor)
        chk.setStyleSheet("""
            QCheckBox::indicator { width: 22px; height: 22px; border-radius: 4px; border: 2px solid #2e3248; background: #1a1d26; }
            QCheckBox::indicator:checked { background: #00e5a0; border: 2px solid #00e5a0; }
        """)
        chk_layout.addWidget(chk)
        self.table.setCellWidget(r, 0, chk_container)
        
        date_edit = QDateEdit()
        date_edit.setCalendarPopup(True)
        date_edit.setDisplayFormat("dd.MM.yyyy")
        
        if date:
            parsed_date = QDate.fromString(date, "dd.MM.yyyy")
            if not parsed_date.isValid():
                parsed_date = QDate.fromString(f"{date}.{QDate.currentDate().year()}", "dd.MM.yyyy")
            if parsed_date.isValid():
                date_edit.setDate(parsed_date)
            else:
                date_edit.setDate(QDate.currentDate())
        else:
            date_edit.setDate(QDate.currentDate())
            
        self.table.setCellWidget(r, 1, date_edit)
        
        time_edit = QTimeEdit(QTime.fromString(time, "HH:mm"))
        time_edit.setDisplayFormat("HH:mm")
        self.table.setCellWidget(r, 2, time_edit)
        
        cw = ExamEditWidget(code, name)
        cw.code_edit.textEdited.connect(lambda t, w=cw: self._on_code_changed(w))
        cw.name_edit.textEdited.connect(lambda t, w=cw: self._on_name_changed(w))
        self.table.setCellWidget(r, 3, cw)
        
        tw = ExamTypeWidget(etype)
        tw.setProperty("prev_text", tw.get_full_type())
        tw.typeChanged.connect(lambda type_w=tw, c=cw: self._on_type_changed(type_w, c))
        self.table.setCellWidget(r, 4, tw)
        
        room_edit = QLineEdit(room)
        room_edit.setPlaceholderText("Salon M101 vb.")
        self.table.setCellWidget(r, 5, room_edit)

        grade_edit = QLineEdit(grade)
        grade_edit.setPlaceholderText("Not")
        grade_edit.setStyleSheet("QLineEdit { text-align: center; }")
        self.table.setCellWidget(r, 6, grade_edit)

    def _import_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Sınav Takvimi Seç", "", "PDF Dosyaları (*.pdf)")
        if file_path:
            self.upload_btn.setText("\n⏳\n\nPDF Okunuyor, Lütfen Bekleyin...\n")
            self.upload_btn.repaint()
            
            from ocr_manager import OCRManager
            ocr = OCRManager()
            success, doc_type, result_data = ocr.parse_pdf(file_path)

            if not success:
                QMessageBox.warning(self, "Hata", result_data)
                self.upload_btn.setText("\n📄\n\nSınav Takvimi Yükle\n(Mevcut kayıtların üzerine eklenir)\n")
                return
                
            if doc_type == "schedule":
                QMessageBox.warning(self, "Yanlış Menü", "Yüklediğiniz dosya bir 'Haftalık Ders Programı'.\nLütfen bu dosyayı soldaki 'Sabit Ders Programı' menüsünden yükleyin.")
                self.upload_btn.setText("\n📄\n\nSınav Takvimi Yükle\n(Mevcut kayıtların üzerine eklenir)\n")
                return

            success_c, courses_data = self.db_manager.get_courses(self.user_id)
            active_course_ids = []
            if success_c:
                active_course_ids = [c.get("course_id", "").lower() for c in courses_data if c.get("is_active", True)]

            added_count = 0
            selected_count = 0
            
            for ex in result_data:
                c_code = ex.get("course_id", "")
                
                safe_etype = self._get_available_exam_type(c_code, ex.get("exam_type", "Vize"))
                
                is_sel = (c_code.lower() in active_course_ids) if c_code else False
                if is_sel: selected_count += 1
                
                self._add_table_row(
                    date=ex.get("exam_date", ""),
                    time=ex.get("exam_time", "10:00"),
                    code=c_code,
                    name=ex.get("course_name", ""),
                    etype=safe_etype,
                    room=ex.get("notes", ""), 
                    grade="", 
                    is_selected=is_sel
                )
                added_count += 1

            if added_count == 0:
                QMessageBox.information(self, "Uyarı", "PDF okundu ancak uygun formatta kayıt bulunamadı.")
                self.upload_btn.setText("\n📄\n\nSınav Takvimi Yükle\n(Mevcut kayıtların üzerine eklenir)\n")
            else:
                self.editor_wrapper.setVisible(True)
                msg = f"\n✅\n\nBaşarıyla {added_count} Not Eklendi\n"
                msg += f"({selected_count} tanesi mevcut derslerinizle eşleşti)\n"
                self.upload_btn.setText(msg)

    def _delete_selected_row(self):
        cur = self.table.currentRow()
        if cur >= 0: self.table.removeRow(cur)

    def _save_to_db(self):
        if not self._check_internet():
            QMessageBox.critical(self, "Bağlantı Hatası", "İnternet bağlantısı kurulamadı!")
            return

        name = self.exam_name_input.text().strip()
        if not name: name = "(Güncel Notlar)"
        
        success_c, courses_data = self.db_manager.get_courses(self.user_id)
        valid_course_ids = []
        if success_c:
            valid_course_ids = [c.get("course_id", "").lower() for c in courses_data]
            
        exams_list = []
        seen_exams = set() 
        
        for r in range(self.table.rowCount()):
            chk_container = self.table.cellWidget(r, 0)
            if chk_container:
                chk = chk_container.findChild(QCheckBox)
                if chk and not chk.isChecked():
                    continue

            cw = self.table.cellWidget(r, 3) 
            if not cw: continue
            
            course_code = cw.code_edit.text().strip().lower()
            exam_type = self.table.cellWidget(r, 4).get_full_type()
            
            if not course_code:
                QMessageBox.critical(self, "Eksik Bilgi", f"Seçili olan {r+1}. satırda DERS KODU boş bırakılamaz!\n\nLütfen ders kodunu girin veya kaydetmek istemiyorsanız o satırın solundaki seçimi (☑) kaldırın.")
                return
                
            if course_code not in valid_course_ids:
                QMessageBox.critical(self, "Ders Bulunamadı", f"Seçili olan {r+1}. satırdaki '{course_code.upper()}' kodlu ders kayıtlarınızda bulunamadı!\n\nLütfen önce sol menüdeki 'Dersler' sekmesinden bu dersi sisteme ekleyin veya kaydetmek istemiyorsanız o satırdaki tiki (☑) kaldırın.")
                return
                
            if (course_code, exam_type) in seen_exams:
                QMessageBox.critical(self, "Kritik Çakışma", f"'{course_code.upper()}' dersine ait birden fazla '{exam_type}' seçimi var!\nLütfen çakışan satırlardan birinin türünü değiştirin veya tikini kaldırın.")
                return
            seen_exams.add((course_code, exam_type))
            
            exams_list.append({
                "course_id": course_code,
                "course_name": cw.name_edit.text().strip(),
                "exam_date": self.table.cellWidget(r, 1).date().toString("dd.MM.yyyy"),
                "exam_time": self.table.cellWidget(r, 2).time().toString("HH:mm"),
                "exam_type": exam_type,
                "exam_room": self.table.cellWidget(r, 5).text().strip(),
                "exam_grade": self.table.cellWidget(r, 6).text().strip()
            })

        if not exams_list:
            QMessageBox.warning(self, "Hata", "Seçili (işaretli) hiçbir kayıt bulunamadı! Lütfen kaydetmek istediklerinizi sol taraftan işaretleyin.")
            return

        self.save_btn.setText("Kaydediliyor...")
        self.save_btn.setEnabled(False)
        self.save_btn.repaint()

        success, msg = self.db_manager.save_exam_schedule(self.user_id, name, exams_list)
        
        self.save_btn.setText("Seçilenleri Kaydet")
        self.save_btn.setEnabled(True)
        
        if success:
            QMessageBox.information(self, "Başarılı", msg)
            self._load_current_exams()
        else:
            QMessageBox.critical(self, "Hata", msg)

    def _delete_exams_action(self):
        if not self._check_internet():
            QMessageBox.critical(self, "Bağlantı Hatası", "İnternet bağlantısı yok! Lütfen bağlantınızı kontrol edin.")
            return
            
        reply = QMessageBox.question(
            self, 'Notları Sil', 
            "Mevcut tüm notları ve sınav kayıtlarını tamamen silmek istediğinize emin misiniz?\n\n(Bu işlem, Dersler sekmesindeki kartlarda bulunan tüm sınav tarihlerini ve notları da temizleyecektir.)",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            success, msg = self.db_manager.delete_exam_schedule(self.user_id)
            if success:
                QMessageBox.information(self, "Başarılı", "Notlar başarıyla silindi.")
                self.view_table.setRowCount(0)
                self.table.setRowCount(0)
                self.editor_wrapper.setVisible(False)
                self.upload_btn.setText("\n📄\n\nSınav Takvimi Yükle\n(Mevcut kayıtların üzerine eklenir)\n")
                self.stacked_widget.setCurrentIndex(1)
                self.btn_go_back.setVisible(False) 
                self.nearest_exam_lbl.setText("💡 Yaklaşan sınavınız bulunmamaktadır.")
            else:
                QMessageBox.critical(self, "Hata", msg)