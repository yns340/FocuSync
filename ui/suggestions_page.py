# ui/suggestions_page.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
class SuggestionsPage(QWidget):
    def __init__(self, user_id, db_manager, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Öneriler - (Okuma işlemleri db_manager'a eklendiğinde aktifleşecek)"))