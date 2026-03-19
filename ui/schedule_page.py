from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QDialog, QLineEdit, QComboBox, QTimeEdit, 
    QDoubleSpinBox, QMessageBox, QFrame, QTabWidget, QDateEdit
)
from PyQt6.QtCore import Qt, QTime, QDate
from PyQt6.QtGui import QFont

DAYS = ["Pazartesi","Salı","Çarşamba","Perşembe","Cuma","Cumartesi","Pazar"]

class AddScheduleDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Programa Ders Ekle")
        self.setFixedSize(420, 360)
        self._build()

    def _build(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(24,24,24,24)
        lay.setSpacing(10)

        t = QLabel("Haftalık Programa Ekle")
        t.setFont(QFont("Segoe UI",14,QFont.Weight.Bold))
        lay.addWidget(t)

        self.name_input = QLineEdit(); self.name_input.setPlaceholderText("Veri Yapıları")
        lay.addWidget(QLabel("Ders Adı")); lay.addWidget(self.name_input)

        self.day_combo = QComboBox(); self.day_combo.addItems(DAYS)
        lay.addWidget(QLabel("Gün")); lay.addWidget(self.day_combo)

        self.start_time = QTimeEdit(QTime(8,30)); self.start_time.setDisplayFormat("HH:mm")
        self.end_time = QTimeEdit(QTime(10,0)); self.end_time.setDisplayFormat("HH:mm")
        lay.addWidget(QLabel("Başlangıç")); lay.addWidget(self.start_time)
        lay.addWidget(QLabel("Bitiş")); lay.addWidget(self.end_time)

        lay.addStretch()
        btn_row = QHBoxLayout()
        c = QPushButton("İptal"); c.clicked.connect(self.reject)
        a = QPushButton("Ekle"); a.setObjectName("primary_btn"); a.clicked.connect(self.accept)
        btn_row.addWidget(c); btn_row.addWidget(a); lay.addLayout(btn_row)

    def get_values(self):
        return {
            "name": self.name_input.text().strip(),
            "day": self.day_combo.currentText(),
            "start": self.start_time.time().toString("HH:mm"),
            "end": self.end_time.time().toString("HH:mm"),
        }

class AddCourseProfileDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ders Profili Ekle")
        self.setFixedSize(380, 280)
        self._build()

    def _build(self):
        lay = QVBoxLayout(self); lay.setContentsMargins(24,24,24,24)
        lay.addWidget(QLabel("Ders Profili / Sınav Tarihi"))

        self.name_input = QLineEdit()
        lay.addWidget(QLabel("Ders Adı")); lay.addWidget(self.name_input)

        self.diff_spin = QDoubleSpinBox(); self.diff_spin.setRange(1.0,5.0)
        lay.addWidget(QLabel("Zorluk Seviyesi (1.0–5.0)")); lay.addWidget(self.diff_spin)

        self.exam_date = QDateEdit(QDate.currentDate().addDays(30))
        self.exam_date.setDisplayFormat("yyyy-MM-dd")
        lay.addWidget(QLabel("Sınav Tarihi")); lay.addWidget(self.exam_date)

        lay.addStretch()
        btn_row = QHBoxLayout()
        c = QPushButton("İptal"); c.clicked.connect(self.reject)
        a = QPushButton("Ekle"); a.setObjectName("primary_btn"); a.clicked.connect(self.accept)
        btn_row.addWidget(c); btn_row.addWidget(a); lay.addLayout(btn_row)

    def get_values(self):
        return {
            "name": self.name_input.text().strip(),
            "difficulty": self.diff_spin.value(),
            "exam_date": self.exam_date.date().toString("yyyy-MM-dd"),
        }

class SchedulePage(QWidget):
    def __init__(self, user_id, db_manager, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.db_manager = db_manager
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(28,24,28,24)

        hdr = QHBoxLayout()
        title = QLabel("Ders Programı")
        title.setFont(QFont("Segoe UI",18,QFont.Weight.Bold))
        hdr.addWidget(title); hdr.addStretch()

        add_sched_btn = QPushButton("+ Programa Ekle")
        add_sched_btn.clicked.connect(self._add_schedule_dialog)
        
        add_course_btn = QPushButton("+ Ders Profili")
        add_course_btn.clicked.connect(self._add_course_dialog)

        hdr.addWidget(add_sched_btn); hdr.addWidget(add_course_btn)
        root.addLayout(hdr)

        # db_manager'da okuma özelliği olmadığı için tablolar boş tutulur
        info = QLabel("Veritabanından veri çekme fonksiyonları (get_schedules vb.) henüz db_manager.py içerisinde tanımlı olmadığı için listeleme kapalıdır. Ancak ekleme işlemleri başarıyla Firebase'e yazılacaktır.")
        info.setWordWrap(True)
        info.setStyleSheet("color:#ff6b35; font-size:12px; padding:20px;")
        root.addWidget(info)
        root.addStretch()

    def _add_schedule_dialog(self):
        dlg = AddScheduleDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            v = dlg.get_values()
            if not v["name"]: return
            success, msg = self.db_manager.add_base_schedule(self.user_id, v["day"], v["name"], v["start"], v["end"])
            QMessageBox.information(self, "Sonuç", msg)

    def _add_course_dialog(self):
        dlg = AddCourseProfileDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            v = dlg.get_values()
            if not v["name"]: return
            success, msg = self.db_manager.add_course(self.user_id, v["name"], v["difficulty"], v["exam_date"])
            QMessageBox.information(self, "Sonuç", msg)