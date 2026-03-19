# ui/statistics_page.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
class StatisticsPage(QWidget):
    def __init__(self, user_id, db_manager, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("İstatistikler - (Okuma işlemleri db_manager'a eklendiğinde aktifleşecek)"))