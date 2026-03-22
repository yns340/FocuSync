# ui/courses_page.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
class CoursesPage(QWidget):
    def __init__(self, user_id, db_manager, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Dersler - (Okuma işlemleri db_manager'a eklendiğinde aktifleşecek)"))