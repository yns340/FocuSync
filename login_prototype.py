import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, 
                             QLineEdit, QPushButton, QMessageBox)
from db_manager import DatabaseManager #db motoru import edildi.

class LoginApp(QWidget):
    def __init__(self):
        super().__init__()
        # Veritabanı yöneticisini başlat
        self.db_handler = DatabaseManager()
        self.init_ui()

    def init_ui(self):
        # Pencere ayarları ve başlığı
        self.setWindowTitle('FocuSync Giriş Testi')
        self.setFixedSize(300, 200)
        layout = QVBoxLayout()

        # Giriş alanları
        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText('E-posta Adresi')
        layout.addWidget(self.email_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText('Şifre')
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        # Butonlar
        self.btn_register = QPushButton('Veritabanına Kaydol')
        self.btn_register.clicked.connect(self.on_register_clicked)
        layout.addWidget(self.btn_register)

        self.btn_login = QPushButton('Giriş Yap (Sorgula)')
        self.btn_login.clicked.connect(self.on_login_clicked)
        layout.addWidget(self.btn_login)

        self.setLayout(layout)

    def on_register_clicked(self):
        """Kayıt butonuna basıldığında çalışır."""
        email = self.email_input.text()
        password = self.password_input.text()
        success, message = self.db_handler.register_user(email, password)
        
        if success:
            QMessageBox.information(self, "Başarılı", message)
        else:
            QMessageBox.critical(self, "Hata", message)

    def on_login_clicked(self):
        """Giriş butonuna basıldığında çalışır."""
        email = self.email_input.text()
        password = self.password_input.text()
        success, result = self.db_handler.login_user(email, password)
        
        if success:
            QMessageBox.information(self, "Giriş Başarılı", f"Kullanıcı ID: {result}")
        else:
            QMessageBox.warning(self, "Giriş Başarısız", result)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginApp()
    window.show()
    sys.exit(app.exec())