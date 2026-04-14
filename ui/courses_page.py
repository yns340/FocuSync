from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QGridLayout, QFrame, QMessageBox, QDialog, 
    QLineEdit, QSlider, QSpinBox, QFormLayout, QComboBox, QGroupBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# ── DERS EKLE / DÜZENLE AÇILIR PENCERESİ (MODAL) ──
class CourseDialog(QDialog):
    def __init__(self, parent=None, course_data=None, is_in_schedule=False, existing_ids=None):
        super().__init__(parent)
        self.is_edit = course_data is not None
        self.is_in_schedule = is_in_schedule 
        self.existing_ids = existing_ids if existing_ids is not None else []
        self.existing_exam_date = course_data.get("exam_date") if self.is_edit else None

        self.setWindowTitle("Dersi Düzenle" if self.is_edit else "Yeni Ders Ekle")
        self.setMinimumWidth(450)
        self.setStyleSheet("""
            QDialog { background-color: #111318; color: #e4e6ed; }
            QLabel { font-size: 14px; font-weight: bold; }
            QLineEdit, QSpinBox, QComboBox { background-color: #1a1d26; color: #e4e6ed; border: 1px solid #2e3248; border-radius: 6px; padding: 8px; font-size: 14px; }
            QLineEdit:focus, QSpinBox:focus, QComboBox:focus { border: 1px solid #00e5a0; }
            QComboBox::drop-down { border: none; }
            QComboBox QAbstractItemView { background-color: #1a1d26; color: #e4e6ed; selection-background-color: #00e5a0; selection-color: #111318; }
            QGroupBox { font-weight: bold; color: #00e5a0; border: 1px solid #2e3248; border-radius: 8px; margin-top: 15px; padding-top: 20px; }
            QGroupBox::title { subcontrol-origin: margin; left: 15px; padding: 0 5px; }
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        form_layout = QFormLayout()
        form_layout.setSpacing(15)

        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("Örn: CENG318 (Zorunlu)")
        if self.is_edit:
            self.id_input.setText(course_data.get("course_id", ""))
            self.id_input.setReadOnly(True)
            self.id_input.setStyleSheet("background-color: #2e3248; color: #9ca3af; border: none;")
        form_layout.addRow("Ders Kodu (ID):", self.id_input)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Örn: Mikroişlemciler")
        if self.is_edit:
            self.name_input.setText(course_data.get("course_name", ""))
        form_layout.addRow("Ders Adı:", self.name_input)

        active_layout = QVBoxLayout()
        active_layout.setSpacing(2)
        self.active_cb = QComboBox()
        self.active_cb.addItems(["✅ Aktif", "📦 Aktif Değil (Arşivlendi)"])
        self.active_lbl = QLabel() 
        if self.is_edit and not course_data.get("is_active", True):
            self.active_cb.setCurrentIndex(1)
        if self.is_in_schedule:
            self.active_cb.setCurrentIndex(0)
            self.active_cb.setEnabled(False)
            self.active_cb.setStyleSheet("background-color: #2e3248; color: #9ca3af;")
            self.active_lbl.setText("📌 Program Dersi")
            self.active_lbl.setStyleSheet("color: #3b82f6; font-size: 11px;")
        active_layout.addWidget(self.active_cb)
        if self.is_in_schedule: active_layout.addWidget(self.active_lbl) 
        form_layout.addRow("Durum:", active_layout)

        slider_layout = QHBoxLayout()
        self.diff_slider = QSlider(Qt.Orientation.Horizontal)
        self.diff_slider.setRange(10, 50)
        self.diff_slider.setSingleStep(5)
        self.diff_slider.setStyleSheet("QSlider::groove:horizontal { border-radius: 4px; height: 8px; background: #2e3248; } QSlider::handle:horizontal { background: #00e5a0; width: 16px; margin: -4px 0; border-radius: 8px; }")
        self.diff_label = QLabel("3.0")
        self.diff_label.setStyleSheet("color: #00e5a0; font-weight: bold; font-size: 16px;")
        start_diff = float(course_data.get("difficulty_level", 3.0)) if self.is_edit else 3.0
        self.diff_slider.setValue(int(start_diff * 10))
        self.diff_label.setText(str(start_diff))
        self.diff_slider.valueChanged.connect(lambda v: self.diff_label.setText(f"{v/10.0:.1f}"))
        slider_layout.addWidget(self.diff_slider); slider_layout.addWidget(self.diff_label)
        form_layout.addRow("Zorluk (1-5):", slider_layout)

        hours_layout = QVBoxLayout()
        hours_layout.setSpacing(2)
        self.hours_input = QSpinBox()
        self.hours_input.setRange(0, 20)
        if self.is_edit: self.hours_input.setValue(int(course_data.get("weekly_hours", 0)))
        self.type_lbl = QLabel()
        if self.is_in_schedule:
            self.hours_input.setEnabled(False) 
            self.hours_input.setStyleSheet("background-color: #2e3248; color: #9ca3af;")
            self.type_lbl.setText("📌 Program Dersi")
            self.type_lbl.setStyleSheet("color: #3b82f6; font-size: 11px;")
        hours_layout.addWidget(self.hours_input)
        hours_layout.addWidget(self.type_lbl)
        form_layout.addRow("Haftalık Saat:", hours_layout)

        # --- YENİ: HEDEF NOT ---
        self.target_input = QSpinBox()
        self.target_input.setRange(0, 100)
        self.target_input.setSuffix(" Puan")
        if self.is_edit:
            self.target_input.setValue(int(course_data.get("target_grade", 0)))
        form_layout.addRow("🎯 Hedef Not:", self.target_input)
        layout.addLayout(form_layout)

        # --- YENİ: SINAV AĞIRLIKLARI (YÜZDELİKLER) ---
        self.weights_dict = {}
        exam_grades = course_data.get("exam_grades", {}) if self.is_edit else {}
        
        if exam_grades:
            weight_group = QGroupBox("📊 Sınav Ağırlıkları (Yüzdelik)")
            wg_layout = QFormLayout(weight_group)
            
            info_lbl = QLabel("Uyarı: Sınav notlarını değiştirmek veya yeni sınav eklemek\niçin sol menüden 'Notlar' sekmesini kullanın.")
            info_lbl.setStyleSheet("color: #9ca3af; font-size: 12px; font-style: italic;")
            wg_layout.addRow(info_lbl)
            
            saved_weights = course_data.get("exam_weights", {})
            
            # Notları hiyerarşik sıralayarak ekrana bas
            priority = {"Vize": 1, "Final": 2, "Bütünleme": 3, "Quiz": 4, "Proje": 5, "Ödev": 6}
            def sort_key(item):
                key = item[0]
                parts = key.rsplit(' ', 1)
                base = parts[0]
                num = int(parts[1]) if len(parts) == 2 and parts[1].isdigit() else 0
                return (priority.get(base, 99), num)

            sorted_grades = sorted(exam_grades.items(), key=sort_key)
            
            for e_type, e_grade in sorted_grades:
                w_spin = QSpinBox()
                w_spin.setRange(0, 100)
                w_spin.setSuffix(" %")
                w_spin.setValue(int(saved_weights.get(e_type, 0)))
                w_spin.valueChanged.connect(self._check_weights)
                self.weights_dict[e_type] = w_spin
                
                grade_disp = f"({e_grade})" if e_grade else "(Girmedi)"
                wg_layout.addRow(f"{e_type} {grade_disp}:", w_spin)
                
            self.weight_total_lbl = QLabel("Toplam Ağırlık: 0%")
            self.weight_total_lbl.setStyleSheet("color: #00e5a0; font-weight: bold; font-size: 15px; margin-top: 5px;")
            wg_layout.addRow("", self.weight_total_lbl)
            
            layout.addWidget(weight_group)

        # BUTONLAR
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("💾 Kaydet")
        self.save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.save_btn.setStyleSheet("""
            QPushButton { background-color: #00e5a0; color: #111318; border-radius: 6px; padding: 10px; font-weight: bold; font-size: 14px; }
            QPushButton:hover { background-color: #00c88c; }
            QPushButton:disabled { background-color: #2e3248; color: #6b7280; }
        """)
        self.save_btn.clicked.connect(self.validate_and_accept)

        cancel_btn = QPushButton("İptal")
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.setStyleSheet("""
            QPushButton { background-color: transparent; color: #6b7280; border: 1px solid #6b7280; border-radius: 6px; padding: 10px; font-weight: bold; }
            QPushButton:hover { background-color: rgba(255, 255, 255, 0.05); color: #e4e6ed; }
        """)
        cancel_btn.clicked.connect(self.reject)

        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(self.save_btn)
        layout.addLayout(btn_layout)
        
        if exam_grades:
            self._check_weights() # İlk açılışta kontrol et

    def _check_weights(self):
        total = sum(spin.value() for spin in self.weights_dict.values())
        self.weight_total_lbl.setText(f"Toplam Ağırlık: {total}%")
        
        if total > 100:
            self.weight_total_lbl.setStyleSheet("color: #ff5c5c; font-weight: bold; font-size: 15px; margin-top: 5px;")
            self.save_btn.setEnabled(False)
            self.save_btn.setText("Ağırlık %100'ü Aşamaz!")
        else:
            self.weight_total_lbl.setStyleSheet("color: #00e5a0; font-weight: bold; font-size: 15px; margin-top: 5px;")
            self.save_btn.setEnabled(True)
            self.save_btn.setText("💾 Kaydet")

    def validate_and_accept(self):
        course_id = self.id_input.text().strip().replace(" ", "").lower()
        if not course_id:
            QMessageBox.warning(self, "Eksik Bilgi", "Lütfen bir Ders Kodu girin!")
            return
        if not self.is_edit and course_id in self.existing_ids:
            QMessageBox.warning(self, "Hata", f"'{course_id.upper()}' kodlu ders zaten mevcut!\nLütfen farklı bir kod girin veya olanı düzenleyin.")
            return
        self.accept()

    def get_data(self):
        weights = {e_type: spin.value() for e_type, spin in self.weights_dict.items()}
        return {
            "course_id": self.id_input.text().strip().replace(" ", "").lower(),
            "course_name": self.name_input.text().strip(),
            "difficulty_level": self.diff_slider.value() / 10.0,
            "weekly_hours": self.hours_input.value(),
            "exam_date": self.existing_exam_date, 
            "is_active": self.active_cb.currentIndex() == 0,
            "target_grade": self.target_input.value(),
            "exam_weights": weights
        }


# ── ÖZEL DERS KARTI (CARD) WIDGET'I ──
class CourseCard(QFrame):
    def __init__(self, course_data, delete_callback, edit_callback, parent=None):
        super().__init__(parent)
        self.course_data = course_data
        self.delete_callback = delete_callback
        self.edit_callback = edit_callback
        
        self.setObjectName("CourseCard")
        self.setStyleSheet("""
            QFrame#CourseCard {
                border: 2px solid #00e5a0;
                border-radius: 12px;
                background-color: transparent;
            }
        """)
        self.setFixedHeight(290) # Kart yüksekliğini biraz artırdık

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # --- %30 ÜST KISIM ---
        self.header = QWidget() 
        self._set_header_style(0.5) 
        header_layout = QVBoxLayout(self.header)
        header_layout.setContentsMargins(10, 10, 10, 10)
        
        code_lbl = QLabel(course_data.get("course_id", "KOD YOK").upper())
        code_lbl.setStyleSheet("color: #111318; font-weight: bold; font-size: 20px; background: transparent; border: none;")
        code_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(code_lbl)

        # --- %70 ALT KISIM ---
        body = QWidget()
        body.setStyleSheet("background-color: transparent;")
        body_layout = QVBoxLayout(body)
        body_layout.setContentsMargins(15, 12, 15, 12)
        body_layout.setSpacing(5)

        name_lbl = QLabel(course_data.get("course_name", "İsimsiz Ders"))
        name_lbl.setStyleSheet("color: #e4e6ed; font-size: 16px; font-weight: bold; border: none;")
        name_lbl.setWordWrap(True)

        diff_lbl = QLabel(f"🎯 Zorluk: {course_data.get('difficulty_level', '-')}")
        diff_lbl.setStyleSheet("color: #9ca3af; font-size: 13px; border: none;")

        hours_lbl = QLabel(f"⏱️ Haftalık: {course_data.get('weekly_hours', '-')} Saat")
        hours_lbl.setStyleSheet("color: #9ca3af; font-size: 13px; border: none;")

        target = course_data.get("target_grade", 0)
        target_str = f"{target}" if target > 0 else "Belirlenmedi"
        target_lbl = QLabel(f"⛳ Hedef Not: {target_str}")
        target_lbl.setStyleSheet("color: #3b82f6; font-size: 13px; font-weight: bold; border: none;")

        # --- MATEMATİKSEL ORTALAMA HESAPLAMA ---
        exam_grades = course_data.get('exam_grades', {})
        exam_weights = course_data.get('exam_weights', {})
        
        total_earned_points = 0.0
        total_entered_weight = 0
        grades_text_parts = []
        
        if exam_grades:
            priority = {"Vize": 1, "Final": 2, "Bütünleme": 3, "Quiz": 4, "Proje": 5, "Ödev": 6}
            def sort_key(item):
                key = item[0]
                parts = key.rsplit(' ', 1)
                base = parts[0]
                num = int(parts[1]) if len(parts) == 2 and parts[1].isdigit() else 0
                return (priority.get(base, 99), num)
            
            sorted_grades = sorted(exam_grades.items(), key=sort_key)
            
            for e_type, grade_str in sorted_grades:
                grades_text_parts.append(f"{e_type}: {grade_str}")
                
                weight = exam_weights.get(e_type, 0)
                try:
                    grade_val = float(grade_str)
                    if weight > 0:
                        total_earned_points += (grade_val * weight) / 100.0
                        total_entered_weight += weight
                except ValueError:
                    pass
                    
            grades_text = " | ".join(grades_text_parts)
        else:
            grades_text = "Henüz sınav girilmedi."

        grade_lbl = QLabel(f"📝 Notlar: {grades_text}")
        grade_lbl.setStyleSheet("color: #9ca3af; font-size: 12px; border: none;")
        grade_lbl.setWordWrap(True)

        # Güncel Ortalama Çıktısı
        if total_entered_weight > 0:
            current_avg = (total_earned_points * 100) / total_entered_weight
            avg_lbl = QLabel(f"📈 Güncel Ort: {current_avg:.1f} (Cepte: {total_earned_points:.1f} Puan)")
            avg_lbl.setStyleSheet("color: #00e5a0; font-size: 13px; font-weight: bold; border: none;")
        else:
            avg_lbl = QLabel("📈 Güncel Ort: Hesaplanamıyor (Ağırlık Yok)")
            avg_lbl.setStyleSheet("color: #6b7280; font-size: 12px; font-style: italic; border: none;")

        body_layout.addWidget(name_lbl)
        body_layout.addWidget(diff_lbl)
        body_layout.addWidget(hours_lbl)
        body_layout.addWidget(target_lbl)
        body_layout.addWidget(avg_lbl)
        body_layout.addWidget(grade_lbl) 
        body_layout.addStretch() 

        # BUTONLAR
        edit_btn = QPushButton("✏️ Ağırlıkları / Dersi Düzenle")
        edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        edit_btn.setStyleSheet("""
            QPushButton { background-color: rgba(59, 130, 246, 0.1); color: #3b82f6; border: 1px solid #3b82f6; border-radius: 6px; padding: 6px; font-size: 13px; font-weight: bold; }
            QPushButton:hover { background-color: #3b82f6; color: #ffffff; }
        """)
        edit_btn.clicked.connect(lambda: self.edit_callback(self.course_data))
        body_layout.addWidget(edit_btn)

        del_btn = QPushButton("🗑️ Sil")
        del_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        del_btn.setStyleSheet("""
            QPushButton { background-color: rgba(255, 92, 92, 0.1); color: #ff5c5c; border: 1px solid #ff5c5c; border-radius: 6px; padding: 6px; font-size: 13px; font-weight: bold; margin-top: 2px; }
            QPushButton:hover { background-color: #ff5c5c; color: #111318; }
        """)
        del_btn.clicked.connect(lambda: self.delete_callback(self.course_data))
        body_layout.addWidget(del_btn)

        layout.addWidget(self.header, 3)
        layout.addWidget(body, 7)

    def _set_header_style(self, opacity):
        self.header.setStyleSheet(f"""
            QWidget {{ background-color: rgba(255, 255, 255, {opacity}); border-top-left-radius: 10px; border-top-right-radius: 10px; }}
        """)
    def enterEvent(self, event):
        self._set_header_style(0.7) 
        super().enterEvent(event)
    def leaveEvent(self, event):
        self._set_header_style(0.5) 
        super().leaveEvent(event)


# ── ANA SAYFA (COURSES PAGE) ──
class CoursesPage(QWidget):
    def __init__(self, user_id, db_manager, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.db_manager = db_manager
        self.schedule_course_ids = [] 
        self.all_course_ids = [] 
        
        self.scrollbar_style = """
            QScrollArea { border: none; background-color: transparent; }
            QScrollBar:vertical { border: none; background: #111318; width: 10px; border-radius: 5px; }
            QScrollBar::handle:vertical { background: #2e3248; min-height: 30px; border-radius: 5px; }
            QScrollBar::handle:vertical:hover { background: #00e5a0; }
        """
        self._build_ui()

    def showEvent(self, event):
        super().showEvent(event)
        self.load_data()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(28, 24, 28, 24)
        root.setSpacing(20)

        hdr = QHBoxLayout()
        title = QLabel("Derslerim")
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        title.setStyleSheet("color:#e4e6ed;")
        hdr.addWidget(title)
        
        add_btn = QPushButton("➕ Yeni Ders Ekle")
        add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_btn.setStyleSheet("""
            QPushButton { background-color: #00e5a0; color: #111318; border-radius: 6px; padding: 8px 16px; font-weight: bold; font-size: 14px; }
            QPushButton:hover { background-color: #00c88c; }
        """)
        add_btn.clicked.connect(self._show_add_dialog)
        hdr.addWidget(add_btn)
        
        hdr.addStretch()
        root.addLayout(hdr)

        # --- ÜST (AKTİF) ---
        top_widget = QWidget()
        top_layout = QVBoxLayout(top_widget)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_header_bg = QWidget()
        top_header_bg.setStyleSheet("background-color: #1a1d26; border-radius: 8px;")
        top_header_layout = QHBoxLayout(top_header_bg)
        top_header_layout.setContentsMargins(15, 12, 15, 12)
        top_title = QLabel("✅ Aktif Dersler")
        top_title.setStyleSheet("color: #00e5a0; font-size: 16px; font-weight: bold; background: transparent;")
        top_header_layout.addWidget(top_title)
        top_header_layout.addStretch()
        top_layout.addWidget(top_header_bg)

        self.active_scroll = QScrollArea()
        self.active_scroll.setWidgetResizable(True)
        self.active_scroll.setStyleSheet(self.scrollbar_style)
        self.active_container = QWidget()
        self.active_container.setStyleSheet("background-color: transparent;")
        self.active_grid = QGridLayout(self.active_container)
        self.active_grid.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.active_grid.setSpacing(25) 
        for i in range(3): self.active_grid.setColumnStretch(i, 1)
        self.active_scroll.setWidget(self.active_container)
        top_layout.addWidget(self.active_scroll)
        
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setStyleSheet("background-color: #2e3248;")

        # --- ALT (PASİF) ---
        bottom_widget = QWidget()
        bottom_layout = QVBoxLayout(bottom_widget)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_header_bg = QWidget()
        bottom_header_bg.setStyleSheet("background-color: #1a1d26; border-radius: 8px;")
        bottom_header_layout = QHBoxLayout(bottom_header_bg)
        bottom_header_layout.setContentsMargins(15, 12, 15, 12)
        bottom_title = QLabel("📦 Aktif Olmayan Dersler (Arşivlenmiş)")
        bottom_title.setStyleSheet("color: #6b7280; font-size: 16px; font-weight: bold; background: transparent;")
        bottom_header_layout.addWidget(bottom_title)
        bottom_header_layout.addStretch()
        bottom_layout.addWidget(bottom_header_bg)

        self.inactive_scroll = QScrollArea()
        self.inactive_scroll.setWidgetResizable(True)
        self.inactive_scroll.setStyleSheet(self.scrollbar_style)
        self.inactive_container = QWidget()
        self.inactive_container.setStyleSheet("background-color: transparent;")
        self.inactive_grid = QGridLayout(self.inactive_container)
        self.inactive_grid.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.inactive_grid.setSpacing(15)
        for i in range(3): self.inactive_grid.setColumnStretch(i, 1)
        self.inactive_scroll.setWidget(self.inactive_container)
        bottom_layout.addWidget(self.inactive_scroll)

        root.addWidget(top_widget, 1) 
        root.addWidget(divider)
        root.addWidget(bottom_widget, 1) 

    def load_data(self):
        succ_sched, sched_ids = self.db_manager.get_schedule_course_ids(self.user_id)
        self.schedule_course_ids = sched_ids if succ_sched else []

        success, courses = self.db_manager.get_courses(self.user_id)
        if success:
            active_courses = []
            inactive_courses = []
            self.all_course_ids = []
            for course in courses:
                self.all_course_ids.append(course.get("course_id"))
                if course.get("is_active", True):
                    active_courses.append(course)
                else:
                    inactive_courses.append(course)
                    
            self._populate_grid(self.active_grid, active_courses)
            self._populate_grid(self.inactive_grid, inactive_courses)

    def _populate_grid(self, grid, data_list):
        for i in reversed(range(grid.count())): 
            widget_to_remove = grid.itemAt(i).widget()
            grid.removeWidget(widget_to_remove)
            widget_to_remove.setParent(None)

        col_count = 3
        for index, course in enumerate(data_list):
            row = index // col_count
            col = index % col_count
            card = CourseCard(course, self._delete_course, self._edit_course) 
            grid.addWidget(card, row, col)

    def _show_add_dialog(self):
        dialog = CourseDialog(self, is_in_schedule=False, existing_ids=self.all_course_ids)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            self._save_course_to_db(data)

    def _edit_course(self, course_data):
        is_in_schedule = course_data.get("course_id") in self.schedule_course_ids
        dialog = CourseDialog(self, course_data, is_in_schedule, existing_ids=self.all_course_ids)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            self._save_course_to_db(data)

    def _save_course_to_db(self, data):
        success, msg = self.db_manager.add_course(
            user_id=self.user_id,
            course_id=data["course_id"],
            course_name=data["course_name"],
            difficulty_level=data["difficulty_level"],
            weekly_hours=data["weekly_hours"],
            exam_date=data["exam_date"],
            is_active=data["is_active"],
            target_grade=data["target_grade"],
            exam_weights=data["exam_weights"] 
        )
        if success:
            self.load_data() 
        else:
            QMessageBox.critical(self, "Hata", msg)

    def _delete_course(self, course_data):
        course_id = course_data.get('course_id')
        reply = QMessageBox.question(
            self, 'Dersi Sil', 
            f"'{course_id.upper()}' dersini tamamen silmek istediğinize emin misiniz?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            success, msg = self.db_manager.delete_course(self.user_id, course_id)
            if success:
                self.load_data()