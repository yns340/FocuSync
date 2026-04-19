from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QFrame, QMessageBox
)
from PyQt6.QtCore import Qt

class ProfilePage(QWidget):
    def __init__(self, user_id, db_manager, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.db_manager = db_manager
        self._current_password = "" # Doğrulama için mevcut şifreyi burada tutacağız
        self._build_ui()
        self._load_profile() # Sayfa yüklenirken verileri çek

    def _build_ui(self):
        # Ana Düzen
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(30)

        # Sayfa Başlığı
        title = QLabel("Profil Ayarları")
        title.setObjectName("page_title") 
        main_layout.addWidget(title)

        # --- 1. BÖLÜM: Profil Fotoğrafı ve Kişisel Bilgiler ---
        top_section = QHBoxLayout()
        top_section.setSpacing(40)

        # Sol Taraf: Profil Fotoğrafı
        self.pp_btn = QPushButton("📷\nFotoğraf\nEkle")
        self.pp_btn.setFixedSize(140, 140)
        self.pp_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.pp_btn.setStyleSheet("""
            QPushButton {
                background-color: #1a1d26;
                border: 2px dashed #2e3248;
                border-radius: 70px;
                color: #6b7280;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                border-color: #00e5a0;
                color: #00e5a0;
                background-color: rgba(0, 229, 160, 0.05);
            }
        """)
        top_section.addWidget(self.pp_btn)

        # Sağ Taraf: Bilgi Formları (İsim, Soyisim, E-posta, Okul)
        info_layout = QVBoxLayout()
        info_layout.setSpacing(15)
        info_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        # İsim ve Soyisim Satırı (2 Eleman)
        name_row = QHBoxLayout()
        name_row.setSpacing(15)
        self.name_input = self._create_input("Ad")
        self.surname_input = self._create_input("Soyad")
        name_row.addWidget(self.name_input)
        name_row.addWidget(self.surname_input)
        info_layout.addLayout(name_row)

        # E-posta ve Okul Satırı (2 Eleman)
        edu_row = QHBoxLayout()
        edu_row.setSpacing(15)
        self.email_input = self._create_input("E-posta Adresi")
        self.email_input.setReadOnly(True) # E-posta değiştirilemez
        self.email_input.setStyleSheet("background-color: #111318; color: #6b7280;") # Soluk gösterim
        
        self.school_input = self._create_input("Okul")
        edu_row.addWidget(self.email_input)
        edu_row.addWidget(self.school_input)
        info_layout.addLayout(edu_row)

        top_section.addLayout(info_layout)
        main_layout.addLayout(top_section)

        # Bölümler arası ayırıcı ince çizgi
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("background-color: #1e2130;")
        main_layout.addWidget(line)

        # --- 2. BÖLÜM: Şifre Değiştirme ---
        pass_title = QLabel("Güvenlik ve Şifre")
        pass_title.setObjectName("page_title")
        pass_title.setStyleSheet("font-size: 16px; margin-top: 10px;") 
        main_layout.addWidget(pass_title)

        # Şifre Alanları (3 Eleman Yan Yana)
        pass_row = QHBoxLayout()
        pass_row.setSpacing(15)
        
        self.current_pass = self._create_input("Mevcut Şifre", is_password=True)
        self.new_pass = self._create_input("Yeni Şifre", is_password=True)
        self.new_pass_confirm = self._create_input("Yeni Şifre (Tekrar)", is_password=True)

        pass_row.addWidget(self.current_pass)
        pass_row.addWidget(self.new_pass)
        pass_row.addWidget(self.new_pass_confirm)
        main_layout.addLayout(pass_row)

        # --- 3. BÖLÜM: Kaydet Butonu ---
        self.save_btn = QPushButton("Değişiklikleri Kaydet")
        self.save_btn.setObjectName("primary_btn")
        self.save_btn.setFixedHeight(48)
        self.save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.save_btn.setStyleSheet("font-size: 15px; margin-top: 15px;")
        
        # Kaydet butonuna tıklandığında _save_profile fonksiyonunu çalıştır
        self.save_btn.clicked.connect(self._save_profile)
        main_layout.addWidget(self.save_btn)

        main_layout.addStretch()

    def _create_input(self, placeholder, is_password=False):
        """Global stilleri kullanan input oluşturucu"""
        field = QLineEdit()
        field.setPlaceholderText(placeholder)
        field.setFixedHeight(42)
        if is_password:
            field.setEchoMode(QLineEdit.EchoMode.Password)
        return field

    # ==========================================
    # VERİTABANI İŞLEMLERİ
    # ==========================================

    def _load_profile(self):
        """Sayfa açıldığında Firebase'den kullanıcı verilerini getirir ve arayüze yazar."""
        success, data = self.db_manager.get_user_profile(self.user_id)
        if success:
            self.name_input.setText(data.get("name", ""))
            self.surname_input.setText(data.get("surname", ""))
            self.school_input.setText(data.get("school", ""))
            self.email_input.setText(data.get("email", ""))
            self._current_password = data.get("password", "")
        else:
            QMessageBox.warning(self, "Bağlantı Hatası", f"Profil bilgileri alınamadı.\n{data}")

    def _save_profile(self):
        """Değişiklikleri doğrular ve Firebase'e kaydeder."""
        name = self.name_input.text().strip()
        surname = self.surname_input.text().strip()
        school = self.school_input.text().strip()
        
        c_pass = self.current_pass.text()
        n_pass = self.new_pass.text()
        n_pass_conf = self.new_pass_confirm.text()

        new_password_to_save = None

        # Eğer şifre alanlarından herhangi biri doldurulmuşsa güvenlik kontrollerini yap
        if c_pass or n_pass or n_pass_conf:
            if c_pass != self._current_password:
                QMessageBox.warning(self, "Hata", "Mevcut şifrenizi yanlış girdiniz!")
                return
            if n_pass != n_pass_conf:
                QMessageBox.warning(self, "Hata", "Yeni şifreler birbiriyle eşleşmiyor!")
                return
            if len(n_pass) < 6:
                QMessageBox.warning(self, "Hata", "Yeni şifreniz en az 6 karakter olmalıdır!")
                return
            new_password_to_save = n_pass

        # Tüm kontrollerden geçtiyse db_manager'a gönder
        success, msg = self.db_manager.update_user_profile(
            self.user_id, name, surname, school, new_password_to_save
        )

        if success:
            QMessageBox.information(self, "Başarılı", msg)
            if new_password_to_save:
                self._current_password = new_password_to_save
            # Başarılı kayıttan sonra şifre alanlarını temizle
            self.current_pass.clear()
            self.new_pass.clear()
            self.new_pass_confirm.clear()
        else:
            QMessageBox.warning(self, "Hata", f"Güncelleme başarısız:\n{msg}")