from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox
)
from PyQt6.QtGui import QFont

class WhitelistPage(QWidget):
    def __init__(self, user_id, db_manager, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.db_manager = db_manager
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(28, 24, 28, 24)

        title = QLabel("Beyaz Liste & Denetim")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        root.addWidget(title)

        info = QLabel("Whitelist ve uygulama denetimi özellikleri şu an aktif değil.\ndb_manager.py dosyasına 'add_violation' metodu eklendi ancak okuma (get) yetenekleri olmadığı için listeleme kapalıdır.")
        info.setStyleSheet("color:#ff6b35; font-size:12px; padding:20px;")
        root.addWidget(info)
        
        # Test için manuel ihlal ekleme butonu
        test_btn = QPushButton("Test İhlali Ekle (Firebase'e yazar)")
        test_btn.clicked.connect(self._add_test_violation)
        root.addWidget(test_btn)
        
        root.addStretch()

    def _add_test_violation(self):
        # db_manager'daki mevcut fonksiyonu kullanıyoruz
        success, msg = self.db_manager.add_violation(self.user_id, "test_session", "chrome.exe", 120)
        QMessageBox.information(self, "Sonuç", msg)