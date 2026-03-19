from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QStackedWidget, QMessageBox, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

class LoginWindow(QWidget):
    login_success = pyqtSignal(str) # Artık sadece user_id dönüyor

    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.setWindowTitle("FocuSync – Giriş")
        self.setFixedSize(440, 580)
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0,0,0,0)

        header = QFrame()
        header.setFixedHeight(165)
        header.setStyleSheet("background-color:#111318;border-bottom:1px solid #1e2130;")
        hl = QVBoxLayout(header); hl.setAlignment(Qt.AlignmentFlag.AlignCenter); hl.setSpacing(6)
        logo = QLabel("⚡ FocuSync")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setFont(QFont("Segoe UI",26,QFont.Weight.Bold))
        logo.setStyleSheet("color:#00e5a0;background:transparent;")
        subtitle = QLabel("Akıllı Odaklanma Sistemi")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color:#6b7280;font-size:13px;background:transparent;")
        
        fb_lbl = QLabel("☁  Firebase Modu Aktif")
        fb_lbl.setStyleSheet("color:#00e5a0;font-size:10px;background:transparent;")
        fb_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hl.addWidget(logo); hl.addWidget(subtitle); hl.addWidget(fb_lbl)
        root.addWidget(header)

        self.stack = QStackedWidget()
        self.stack.addWidget(self._build_login_page())
        self.stack.addWidget(self._build_register_page())
        root.addWidget(self.stack)

    def _build_login_page(self):
        page = QWidget()
        lay = QVBoxLayout(page); lay.setContentsMargins(40,32,40,32); lay.setSpacing(12)
        title = QLabel("Giriş Yap")
        title.setFont(QFont("Segoe UI",16,QFont.Weight.Bold))
        title.setStyleSheet("color:#e4e6ed;")
        lay.addWidget(title); lay.addSpacing(6)

        lbl1 = QLabel("E-posta Adresi"); lbl1.setStyleSheet("color:#6b7280;font-size:11px;font-weight:600;")
        lay.addWidget(lbl1)
        self.login_email = QLineEdit(); self.login_email.setPlaceholderText("ornek@email.com"); self.login_email.setFixedHeight(42)
        lay.addWidget(self.login_email)

        lbl2 = QLabel("Şifre"); lbl2.setStyleSheet("color:#6b7280;font-size:11px;font-weight:600;")
        lay.addWidget(lbl2)
        pw_row = QHBoxLayout()
        self.login_password = QLineEdit(); self.login_password.setPlaceholderText("••••••••")
        self.login_password.setEchoMode(QLineEdit.EchoMode.Password); self.login_password.setFixedHeight(42)
        self.login_password.returnPressed.connect(self._do_login)
        show = QPushButton("👁"); show.setFixedSize(42,42); show.setCheckable(True)
        show.toggled.connect(lambda c: self.login_password.setEchoMode(
            QLineEdit.EchoMode.Normal if c else QLineEdit.EchoMode.Password))
        pw_row.addWidget(self.login_password); pw_row.addWidget(show)
        lay.addLayout(pw_row)

        self.login_error = QLabel(""); self.login_error.setStyleSheet("color:#ff6b35;font-size:12px;")
        self.login_error.setWordWrap(True); lay.addWidget(self.login_error)

        btn = QPushButton("Giriş Yap"); btn.setObjectName("primary_btn")
        btn.setFixedHeight(44); btn.setFont(QFont("Segoe UI",13,QFont.Weight.Bold))
        btn.clicked.connect(self._do_login); lay.addWidget(btn)
        lay.addStretch()

        sw = QHBoxLayout(); sw.addStretch()
        sw.addWidget(QLabel("Hesabın yok mu?"))
        rb = QPushButton("Kayıt Ol"); rb.setStyleSheet("background:transparent;border:none;color:#00e5a0;font-size:12px;font-weight:700;padding:0;")
        rb.setCursor(Qt.CursorShape.PointingHandCursor); rb.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        sw.addWidget(rb); sw.addStretch(); lay.addLayout(sw)
        return page

    def _build_register_page(self):
        page = QWidget()
        lay = QVBoxLayout(page); lay.setContentsMargins(40,24,40,24); lay.setSpacing(8)
        title = QLabel("Kayıt Ol")
        title.setFont(QFont("Segoe UI",16,QFont.Weight.Bold))
        title.setStyleSheet("color:#e4e6ed;")
        lay.addWidget(title); lay.addSpacing(4)

        # db_manager sadece email ve password aldığı için fullname kaldırıldı
        for attr, lbl_text, ph, echo in [
            ("reg_email","E-posta Adresi","ornek@email.com",False),
            ("reg_password","Şifre (en az 6 karakter)","••••••••",True),
            ("reg_password2","Şifre Tekrar","••••••••",True),
        ]:
            lbl = QLabel(lbl_text); lbl.setStyleSheet("color:#6b7280;font-size:11px;font-weight:600;")
            lay.addWidget(lbl)
            inp = QLineEdit(); inp.setPlaceholderText(ph); inp.setFixedHeight(40)
            if echo: inp.setEchoMode(QLineEdit.EchoMode.Password)
            setattr(self, attr, inp); lay.addWidget(inp)

        self.reg_error = QLabel(""); self.reg_error.setStyleSheet("color:#ff6b35;font-size:12px;")
        self.reg_error.setWordWrap(True); lay.addWidget(self.reg_error)

        btn = QPushButton("Hesap Oluştur"); btn.setObjectName("primary_btn")
        btn.setFixedHeight(44); btn.setFont(QFont("Segoe UI",13,QFont.Weight.Bold))
        btn.clicked.connect(self._do_register); lay.addWidget(btn)
        lay.addStretch()

        sw = QHBoxLayout(); sw.addStretch()
        sw.addWidget(QLabel("Hesabın var mı?"))
        bb = QPushButton("Giriş Yap"); bb.setStyleSheet("background:transparent;border:none;color:#00e5a0;font-size:12px;font-weight:700;padding:0;")
        bb.setCursor(Qt.CursorShape.PointingHandCursor); bb.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        sw.addWidget(bb); sw.addStretch(); lay.addLayout(sw)
        return page

    def _do_login(self):
        email = self.login_email.text().strip()
        pw = self.login_password.text()
        if not email or not pw:
            self.login_error.setText("E-posta ve şifre zorunludur.")
            return
        
        success, result = self.db_manager.login_user(email, pw)
        if success:
            self.login_error.setText("")
            self.login_success.emit(result) # result = user.id
        else:
            self.login_error.setText(result)
            self.login_password.clear()

    def _do_register(self):
        email = self.reg_email.text().strip()
        pw1 = self.reg_password.text()
        pw2 = self.reg_password2.text()
        if not email or not pw1:
            self.reg_error.setText("E-posta ve şifre zorunludur.")
            return
        if pw1 != pw2:
            self.reg_error.setText("Şifreler eşleşmiyor.")
            return
            
        success, msg = self.db_manager.register_user(email, pw1)
        if success:
            self.reg_error.setText("")
            QMessageBox.information(self, "Başarılı", msg)
            self.stack.setCurrentIndex(0)
            self.login_email.setText(email)
            self.login_password.setFocus()
        else:
            self.reg_error.setText(msg)