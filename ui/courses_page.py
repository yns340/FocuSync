from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QGridLayout, QFrame, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# ── ÖZEL DERS KARTI (CARD) WIDGET'I ──
class CourseCard(QFrame):
    def __init__(self, course_data, delete_callback, parent=None):
        super().__init__(parent)
        self.course_data = course_data
        self.delete_callback = delete_callback
        
        self.setObjectName("CourseCard")
        self.setStyleSheet("""
            QFrame#CourseCard {
                border: 2px solid #00e5a0;
                border-radius: 12px;
                background-color: transparent;
            }
        """)
        self.setFixedHeight(240)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # --- %30 ÜST KISIM (CAM EFEKTLİ HEADER) ---
        self.header = QWidget() 
        self._set_header_style(0.5) # Başlangıçta %50 saydamlık
        
        header_layout = QVBoxLayout(self.header)
        header_layout.setContentsMargins(10, 10, 10, 10)
        
        code_lbl = QLabel(course_data.get("course_id", "KOD YOK").upper())
        code_lbl.setStyleSheet("color: #111318; font-weight: bold; font-size: 20px; background: transparent; border: none;")
        code_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(code_lbl)

        # --- %70 ALT KISIM (TRANSPARAN BODY) ---
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

        exam_date = course_data.get('exam_date')
        exam_text = exam_date if exam_date else "Belirtilmedi"
        exam_lbl = QLabel(f"📅 Sınav: {exam_text}")
        exam_lbl.setStyleSheet("color: #9ca3af; font-size: 13px; border: none;")

        del_btn = QPushButton("🗑️ Dersi Sil")
        del_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        del_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 92, 92, 0.1);
                color: #ff5c5c;
                border: 1px solid #ff5c5c;
                border-radius: 6px;
                padding: 6px;
                font-size: 13px;
                font-weight: bold;
                margin-top: 5px;
            }
            QPushButton:hover {
                background-color: #ff5c5c;
                color: #111318;
            }
        """)
        del_btn.clicked.connect(lambda: self.delete_callback(self.course_data))

        body_layout.addWidget(name_lbl)
        body_layout.addWidget(diff_lbl)
        body_layout.addWidget(hours_lbl)
        body_layout.addWidget(exam_lbl)
        body_layout.addStretch() 
        body_layout.addWidget(del_btn)

        layout.addWidget(self.header, 3)
        layout.addWidget(body, 7)

    # ── HOVER EFEKTLERİ ──
    def _set_header_style(self, opacity):
        self.header.setStyleSheet(f"""
            QWidget {{
                background-color: rgba(255, 255, 255, {opacity});
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                border-bottom-left-radius: 0px;
                border-bottom-right-radius: 0px;
            }}
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
        
        self.scrollbar_style = """
            QScrollArea { border: none; background-color: transparent; }
            QScrollBar:vertical { border: none; background: #111318; width: 10px; border-radius: 5px; }
            QScrollBar::handle:vertical { background: #2e3248; min-height: 30px; border-radius: 5px; }
            QScrollBar::handle:vertical:hover { background: #00e5a0; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { border: none; background: none; }
        """
        
        self._build_ui()
        self.load_data() # Artık sayfa açılır açılmaz DB'den verileri çekiyoruz!

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(28, 24, 28, 24)
        root.setSpacing(20)

        hdr = QHBoxLayout()
        title = QLabel("Derslerim")
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        title.setStyleSheet("color:#e4e6ed;")
        hdr.addWidget(title)
        
        # Yenile Butonu
        refresh_btn = QPushButton("🔄 Yenile")
        refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        refresh_btn.setStyleSheet("background-color: #2e3248; color: #e4e6ed; border-radius: 6px; padding: 8px 16px; font-weight: bold;")
        refresh_btn.clicked.connect(self.load_data)
        hdr.addWidget(refresh_btn)
        
        hdr.addStretch()
        root.addLayout(hdr)

        # --- 1. ÜST KISIM (AKTİF DERSLER) ---
        top_widget = QWidget()
        top_layout = QVBoxLayout(top_widget)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(10)

        top_header_bg = QWidget()
        top_header_bg.setStyleSheet("background-color: #1a1d26; border-radius: 8px;")
        top_header_layout = QHBoxLayout(top_header_bg)
        top_header_layout.setContentsMargins(15, 12, 15, 12)
        
        top_title = QLabel("✅ Aktif Dersler (Programda var veya Ekstra)")
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
        
        for i in range(3):
            self.active_grid.setColumnStretch(i, 1)
            
        self.active_scroll.setWidget(self.active_container)
        top_layout.addWidget(self.active_scroll)
        
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setStyleSheet("background-color: #2e3248;")

        # --- 2. ALT KISIM (ARŞİVLENMİŞ DERSLER) ---
        bottom_widget = QWidget()
        bottom_layout = QVBoxLayout(bottom_widget)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.setSpacing(15)

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
        
        for i in range(3):
            self.inactive_grid.setColumnStretch(i, 1)

        self.inactive_scroll.setWidget(self.inactive_container)
        bottom_layout.addWidget(self.inactive_scroll)

        root.addWidget(top_widget, 1) 
        root.addWidget(divider)
        root.addWidget(bottom_widget, 1) 

    def load_data(self):
        """Veritabanından dersleri çeker ve aktiflik durumuna göre UI'a yerleştirir."""
        success, courses = self.db_manager.get_courses(self.user_id)
        
        if success:
            active_courses = []
            inactive_courses = []
            
            for course in courses:
                # 'is_active' alanı yoksa bile güvenlik için default True kabul et
                if course.get("is_active", True):
                    active_courses.append(course)
                else:
                    inactive_courses.append(course)
                    
            self._populate_grid(self.active_grid, active_courses)
            self._populate_grid(self.inactive_grid, inactive_courses)
        else:
            QMessageBox.warning(self, "Bağlantı Hatası", "Dersler veritabanından çekilirken bir hata oluştu.")

    def _populate_grid(self, grid, data_list):
        """Verilen verileri 3 sütunlu ızgaraya (Grid) yerleştirir."""
        for i in reversed(range(grid.count())): 
            widget_to_remove = grid.itemAt(i).widget()
            grid.removeWidget(widget_to_remove)
            widget_to_remove.setParent(None)

        col_count = 3
        for index, course in enumerate(data_list):
            row = index // col_count
            col = index % col_count
            card = CourseCard(course, self._delete_course)
            grid.addWidget(card, row, col)

    def _delete_course(self, course_data):
        """Sil butonuna basıldığında onay isteyip veritabanından siler."""
        course_id = course_data.get('course_id')
        
        reply = QMessageBox.question(
            self, 'Dersi Sil', 
            f"'{course_id}' dersini ve ona ait istatistikleri tamamen silmek istediğinize emin misiniz?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            success, msg = self.db_manager.delete_course(self.user_id, course_id)
            if success:
                self.load_data() # Sildikten sonra ekranı anında yenile
            else:
                QMessageBox.warning(self, "Hata", msg)