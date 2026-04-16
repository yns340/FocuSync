"""
main.py
FocuSync — Akıllı Odaklanma Sistemi
Sadece Firebase (db_manager.py) kullanan temizlenmiş giriş noktası.
"""
import os
import sys
os.environ["PYTHONUTF8"] = "1"
os.environ["PYTHONIOENCODING"] = "utf-8"

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont

from db_manager import DatabaseManager
from ui.login_window import LoginWindow
from ui.main_window import MainWindow
from ui.styles import APP_STYLE

def on_login_success(user_id):
    login_win.hide()
    # User ID ve veritabanı yöneticisi ana pencereye aktarılır
    main_win = MainWindow(user_id, db)
    main_win.setStyleSheet(APP_STYLE)
    main_win.show()
    app._main_win = main_win

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("FocuSync")
    app.setStyleSheet(APP_STYLE)

    default_font = QFont("Segoe UI", 12)
    app.setFont(default_font)

    # Veritabanı bağlantısı SADECE buradan başlatılır
    db = DatabaseManager()

    # Giriş ekranı
    login_win = LoginWindow(db)
    login_win.setStyleSheet(APP_STYLE)
    login_win.login_success.connect(on_login_success)
    login_win.show()

    sys.exit(app.exec())