import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, 
                             QLineEdit, QPushButton, QMessageBox, QLabel)
from PyQt6.QtCore import Qt
from db_manager import DatabaseManager

class DashboardWindow(QWidget):
    """Giriş yaptıktan sonra açılacak olan Ana Panel (Dashboard) ekranı."""
    def __init__(self, user_id, db_handler):
        super().__init__()
        self.user_id = user_id
        self.db_handler = db_handler # db_manager.py'deki bağlantıyı buraya taşıdık
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('FocuSync Ana Panel')
        self.setFixedSize(400, 250)
        layout = QVBoxLayout()

        self.lbl_welcome = QLabel(f"Hoş Geldin! ID: {self.user_id}", self)
        self.lbl_welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.lbl_welcome)

        # Mimarini test etmen için sihirli buton
        self.btn_create_db = QPushButton('Veritabanı Mimarisi Oluştur (Test Verisi Bas)')
        self.btn_create_db.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px;")
        self.btn_create_db.clicked.connect(self.on_create_db_clicked)
        layout.addWidget(self.btn_create_db)

        self.setLayout(layout)

    def on_create_db_clicked(self):
        # 1. ADIM (Profil): Dersin kimliğini ekliyoruz
        c_success, c_msg = self.db_handler.add_course(self.user_id, "Mikroişlemciler", 5, "2026-04-15")
        
        # 2. ADIM (OCR): Sabit okul programını ekliyoruz
        s_success, s_msg = self.db_handler.add_base_schedule(self.user_id, "Pazartesi", "Mikroişlemciler", "10:00", "11:30")
        
        # 3. ADIM (Algoritma): Akıllı çalışma planı ekliyoruz
        p_success, p_msg = self.db_handler.add_study_plan(self.user_id, "Mikroişlemciler", "2026-03-16", 45)
        
        # 4. ADIM (Kamera): Gerçekleşen odaklanma seansını ekliyoruz (Örnek bir plan_id ile)
        f_success, f_msg = self.db_handler.add_focus_session(self.user_id, "ornek_plan_id_123", "Mikroişlemciler", 35, 78, "Completed")
        
        # 5. ADIM (Whitelist): İhlal kaydını ekliyoruz (Örnek bir session_id ile)
        v_success, v_msg = self.db_handler.add_violation(self.user_id, "ornek_session_id_456", "Instagram.exe", 120)

        # Eğer herhangi bir adımda hata olursa (False dönerse) uyar, hepsi True ise başarılı mesajı ver
        if all([c_success, s_success, p_success, f_success, v_success]):
            QMessageBox.information(self, "Başarılı", "Tüm modüller çalıştı! Firebase Console'a gidip 5 farklı tablonu görebilirsin.")
        else:
            QMessageBox.warning(self, "Uyarı", "Bazı veriler eklenirken hata oluştu. Lütfen konsolu kontrol et.")


class LoginApp(QWidget):
    """İlk açılan Giriş ekranı."""
    def __init__(self):
        super().__init__()
        self.db_handler = DatabaseManager()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('FocuSync Giriş Testi')
        self.setFixedSize(300, 200)
        layout = QVBoxLayout()

        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText('E-posta Adresi')
        layout.addWidget(self.email_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText('Şifre')
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        self.btn_register = QPushButton('Veritabanına Kaydol')
        self.btn_register.clicked.connect(self.on_register_clicked)
        layout.addWidget(self.btn_register)

        self.btn_login = QPushButton('Giriş Yap')
        self.btn_login.clicked.connect(self.on_login_clicked)
        layout.addWidget(self.btn_login)

        self.setLayout(layout)

    def on_register_clicked(self):
        email = self.email_input.text()
        password = self.password_input.text()
        success, message = self.db_handler.register_user(email, password)
        if success:
            QMessageBox.information(self, "Başarılı", message)
        else:
            QMessageBox.critical(self, "Hata", message)

    def on_login_clicked(self):
        email = self.email_input.text()
        password = self.password_input.text()
        success, result = self.db_handler.login_user(email, password)
        
        if success:
            self.hide() 
            self.dashboard = DashboardWindow(user_id=result, db_handler=self.db_handler)
            self.dashboard.show()
        else:
            QMessageBox.warning(self, "Giriş Başarısız", result)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginApp()
    window.show()
    sys.exit(app.exec())