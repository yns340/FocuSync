"""
ui/main_window.py  — FocuSync Ana Pencere
Tüm sayfaları barındıran sidebar + stacked widget mimarisi.
"""
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton, QStackedWidget, QFrame, QMessageBox,
    QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# Menü sıralaması ve isimler güncellendi (Notlar Eklendi)
NAV_ITEMS = [
    ("🏠", "Dashboard",               "dashboard"),
    ("📚", "Sabit Ders Programı",     "schedule"),
    ("📅", "Notlar",                    "exams"),         # YENİ EKLENDİ
    ("💡", "Önerilen Ders Programı",  "suggested_plan"),
    ("📊", "Dersler",                 "courses"),
    ("🎯", "Odak Modu",               "focus"),
    ("🛡️", "Beyaz Liste",             "whitelist"),
]

class MainWindow(QMainWindow):
    def __init__(self, user_id, db_manager):
        super().__init__()
        self.user_id = user_id
        self.db_manager = db_manager
        self.setWindowTitle(f"FocuSync — Profil: {self.user_id}")
        self.setMinimumSize(1200, 760)
        self.resize(1400, 860)
        self._nav_buttons: dict[str, QPushButton] = {}
        self._build_ui()
        self._navigate("dashboard") 

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0,0,0,0)
        root.setSpacing(0)

        # ── Sidebar ──────────────────────────────────────────────────────
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        sb = QVBoxLayout(sidebar)
        sb.setContentsMargins(0,0,0,16)
        sb.setSpacing(2)

        logo = QLabel("⚡ FocuSync")
        logo.setObjectName("logo_label")
        logo.setFont(QFont("Segoe UI",18,QFont.Weight.Bold))
        logo.setAlignment(Qt.AlignmentFlag.AlignLeft)
        sb.addWidget(logo)

        user_frame = QFrame()
        user_frame.setStyleSheet("background:#1a1d26;border:1px solid #1e2130;border-radius:10px;margin:4px 10px 12px 10px;")
        uf = QVBoxLayout(user_frame)
        uf.setContentsMargins(12,10,12,10)
        uf.setSpacing(2)
        name_lbl = QLabel("Kullanıcı ID:")
        name_lbl.setFont(QFont("Segoe UI",10,QFont.Weight.Bold))
        name_lbl.setStyleSheet("background:transparent;color:#e4e6ed;border:none;")
        uname_lbl = QLabel(str(self.user_id))
        uname_lbl.setStyleSheet("background:transparent;color:#00e5a0;font-size:10px;border:none;")
        uf.addWidget(name_lbl); uf.addWidget(uname_lbl)
        sb.addWidget(user_frame)

        nav_sec = QLabel("  MODÜLLER")
        nav_sec.setStyleSheet("color:#2e3248;font-size:10px;font-weight:700;letter-spacing:1.5px;padding:4px 10px;")
        sb.addWidget(nav_sec)

        for icon, label, key in NAV_ITEMS:
            btn = QPushButton(f"  {icon}  {label}")
            btn.setObjectName("nav_button")
            btn.setFixedHeight(42)
            btn.setFont(QFont("Segoe UI",12))
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda _, k=key: self._navigate(k))
            self._nav_buttons[key] = btn
            sb.addWidget(btn)

        sb.addStretch()

        profile_btn = QPushButton("  👤  Profil")
        profile_btn.setObjectName("nav_button")
        profile_btn.setFixedHeight(42)
        profile_btn.setFont(QFont("Segoe UI",12))
        profile_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        profile_btn.clicked.connect(lambda _, k="profile": self._navigate(k))
        self._nav_buttons["profile"] = profile_btn
        sb.addWidget(profile_btn)

        logout_btn = QPushButton("  🚪  Çıkış Yap")
        logout_btn.setObjectName("nav_button")
        logout_btn.setFixedHeight(42)
        logout_btn.setFont(QFont("Segoe UI",12))
        logout_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        logout_btn.clicked.connect(self._logout)
        sb.addWidget(logout_btn)
        root.addWidget(sidebar)

        # ── Sayfaları Sisteme Kaydetme ─────────────
        self.stack = QStackedWidget()

        from ui.dashboard_page       import DashboardPage
        from ui.schedule_page        import SchedulePage
        from ui.exams_page           import ExamsPage         # YENİ EKLENDİ
        from ui.suggested_plan_page  import SuggestedPlanPage 
        from ui.courses_page         import CoursesPage       
        from ui.focus_page           import FocusPage
        from ui.whitelist_page       import WhitelistPage
        from ui.profile_page         import ProfilePage

        self.dashboard_page      = DashboardPage(self.user_id, self.db_manager)
        self.schedule_page       = SchedulePage(self.user_id, self.db_manager)
        self.exams_page          = ExamsPage(self.user_id, self.db_manager) # YENİ EKLENDİ
        self.suggested_plan_page = SuggestedPlanPage(self.user_id, self.db_manager)
        self.courses_page        = CoursesPage(self.user_id, self.db_manager)
        self.whitelist_page = WhitelistPage(self.user_id, self.db_manager)
        self.focus_page = FocusPage(
            self.user_id,
            self.db_manager,
            whitelist_page=self.whitelist_page
        )
        self.profile_page        = ProfilePage(self.user_id, self.db_manager) 

        # Sıralama güncellendi
        self._page_map = {
            "dashboard":      (0, self.dashboard_page),
            "schedule":       (1, self.schedule_page),
            "exams":          (2, self.exams_page),           # YENİ EKLENDİ
            "suggested_plan": (3, self.suggested_plan_page),
            "courses":        (4, self.courses_page),
            "focus":          (5, self.focus_page),
            "whitelist":      (6, self.whitelist_page),
            "profile":        (7, self.profile_page),
        }
        
        for _, page in self._page_map.values():
            self.stack.addWidget(page)

        root.addWidget(self.stack, stretch=1)

    def _navigate(self, key: str):
        if key not in self._page_map: return
        idx, page = self._page_map[key]
        self.stack.setCurrentIndex(idx)

        if hasattr(page, "refresh") and callable(page.refresh):
            page.refresh()
        
        for k, btn in self._nav_buttons.items():
            btn.setProperty("active", "true" if k == key else "false")
            btn.style().unpolish(btn); btn.style().polish(btn)

    def _logout(self):
        ans = QMessageBox.question(self, "Çıkış",
            "Oturumu kapatmak istiyor musunuz?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if ans == QMessageBox.StandardButton.Yes:
            self.close()