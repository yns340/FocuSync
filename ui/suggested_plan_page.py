# ui/suggested_plan_page.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QFrame, QSizePolicy, QGraphicsDropShadowEffect,
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QColor, QPainter, QPen, QLinearGradient, QBrush

# ─────────────────────────────────────────────
#  MOCK DATA
# ─────────────────────────────────────────────
MOCK_SUGGESTIONS = {
    "Pazartesi": [
        {"course": "BM314", "name": "Yazılım Mühendisliği", "start": "09:00", "end": "11:00", "type": "Yeni Konu",  "priority": "high"},
        {"course": "BM318", "name": "Veritabanı Yönetimi",  "start": "14:00", "end": "15:30", "type": "Tekrar",     "priority": "medium"},
    ],
    "Salı": [
        {"course": "BM312", "name": "Mikro İşlemciler",     "start": "10:00", "end": "12:00", "type": "Yeni Konu",  "priority": "high"},
        {"course": "BM316", "name": "İşletim Sistemleri",   "start": "15:00", "end": "16:30", "type": "Alıştırma",  "priority": "medium"},
    ],
    "Çarşamba": [
        {"course": "BM318", "name": "Veritabanı Yönetimi",  "start": "09:00", "end": "11:00", "type": "Yeni Konu",  "priority": "high"},
        {"course": "BM314", "name": "Yazılım Mühendisliği", "start": "13:00", "end": "14:00", "type": "Tekrar",     "priority": "low"},
    ],
    "Perşembe": [
        {"course": "BM312", "name": "Mikro İşlemciler",     "start": "11:00", "end": "13:00", "type": "Alıştırma",  "priority": "high"},
    ],
    "Cuma": [
        {"course": "BM316", "name": "İşletim Sistemleri",   "start": "10:00", "end": "12:00", "type": "Yeni Konu",  "priority": "medium"},
        {"course": "BM314", "name": "Yazılım Mühendisliği", "start": "14:00", "end": "15:30", "type": "Proje",      "priority": "high"},
    ],
    "Cumartesi": [
        {"course": "BM318", "name": "Veritabanı Yönetimi",  "start": "10:00", "end": "13:00", "type": "Alıştırma",  "priority": "medium"},
        {"course": "BM312", "name": "Mikro İşlemciler",     "start": "14:00", "end": "15:00", "type": "Tekrar",     "priority": "low"},
    ],
    "Pazar": [
        {"course": "BM316", "name": "İşletim Sistemleri",   "start": "11:00", "end": "12:30", "type": "Tekrar",     "priority": "low"},
    ],
}

MOCK_INSIGHTS = [
    {"icon": "⚡", "title": "BM312 Kritik!",        "body": "Mikro İşlemciler dersinde geçen haftadan bu yana hiç çalışmadınız. Yaklaşan sınav riski yüksek.", "color": "#ff5c5c"},
    {"icon": "✅", "title": "Denge İyi Görünüyor",  "body": "Haftalık yük dağılımı dengeli. En yoğun gün Cumartesi ile 3 saat çalışma önerisi var.",           "color": "#00e5a0"},
    {"icon": "🎯", "title": "Odak Tavsiyesi",       "body": "BM314 için Proje seansını Cuma günü 14:00'e koyduk; hafta sonu baskısını önceden azaltır.",       "color": "#3b82f6"},
    {"icon": "📈", "title": "Verimlilik Artışı",    "body": "Pomodoro tekniğini kullanırsanız bu planla tahmini verimlilik %23 artabilir.",                     "color": "#f59e0b"},
]

# ─────────────────────────────────────────────
#  SABİTLER
# ─────────────────────────────────────────────
BG_MAIN   = "#111318"
BG_CARD   = "#1a1d26"
BG_HOVER  = "#1e2130"
BORDER    = "#2e3248"
BORDER_LT = "#1e2130"
ACCENT    = "#00e5a0"
BLUE      = "#3b82f6"
AMBER     = "#f59e0b"
RED       = "#ff5c5c"
TEXT_HI   = "#e4e6ed"
TEXT_MID  = "#9ca3af"
TEXT_LO   = "#6b7280"

PRIORITY_COLORS = {"high": ACCENT, "medium": BLUE, "low": AMBER}
PRIORITY_LABELS = {"high": "Öncelikli", "medium": "Orta", "low": "Düşük"}
TYPE_ICONS      = {"Yeni Konu": "📖", "Tekrar": "🔄", "Alıştırma": "✏️", "Proje": "🛠️"}


def _shadow(radius=14, opacity=60):
    eff = QGraphicsDropShadowEffect()
    eff.setBlurRadius(radius)
    c = QColor("#000000")
    c.setAlpha(opacity)
    eff.setColor(c)
    eff.setOffset(0, 3)
    return eff


# ─────────────────────────────────────────────
#  İSTATİSTİK KARTI
# ─────────────────────────────────────────────
class StatCard(QFrame):
    def __init__(self, icon, value, label, accent_color=ACCENT, parent=None):
        super().__init__(parent)
        self.accent_color = accent_color
        self.setMinimumHeight(100)
        self.setMaximumHeight(130)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.setStyleSheet(f"""
            QFrame {{
                background-color:{BG_CARD};
                border:1px solid {BORDER_LT};
                border-radius:12px;
            }}
        """)
        self.setGraphicsEffect(_shadow())

        lay = QVBoxLayout(self)
        lay.setContentsMargins(16, 12, 16, 10)
        lay.setSpacing(2)

        ico = QLabel(icon)
        ico.setStyleSheet(f"font-size:20px; color:{accent_color}; background:transparent; border:none;")
        lay.addWidget(ico)

        v = QLabel(value)
        v.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        v.setStyleSheet(f"color:{TEXT_HI}; background:transparent; border:none;")
        lay.addWidget(v)

        lb = QLabel(label)
        lb.setFont(QFont("Segoe UI", 10))
        lb.setStyleSheet(f"color:{TEXT_LO}; background:transparent; border:none;")
        lay.addWidget(lb)

    def paintEvent(self, e):
        super().paintEvent(e)
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        c = QColor(self.accent_color)
        c.setAlpha(200)
        p.setPen(QPen(c, 2))
        p.drawLine(0, self.height() - 2, int(self.width() * 0.42), self.height() - 2)


# ─────────────────────────────────────────────
#  İÇGÖRÜ KARTI
# ─────────────────────────────────────────────
class InsightCard(QFrame):
    def __init__(self, icon, title, body, color=ACCENT, parent=None):
        super().__init__(parent)
        self.setFixedWidth(270)
        self.setMinimumHeight(115)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        self.setStyleSheet(f"""
            QFrame {{
                background-color:{BG_CARD};
                border:1px solid {BORDER_LT};
                border-left:3px solid {color};
                border-radius:10px;
            }}
        """)
        self.setGraphicsEffect(_shadow(10, 50))

        lay = QVBoxLayout(self)
        lay.setContentsMargins(12, 10, 12, 10)
        lay.setSpacing(6)

        top = QHBoxLayout()
        ico = QLabel(icon)
        ico.setStyleSheet("font-size:16px; background:transparent; border:none;")
        ttl = QLabel(title)
        ttl.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        ttl.setStyleSheet(f"color:{color}; background:transparent; border:none;")
        top.addWidget(ico)
        top.addWidget(ttl)
        top.addStretch()
        lay.addLayout(top)

        bd = QLabel(body)
        bd.setWordWrap(True)
        bd.setFont(QFont("Segoe UI", 9))
        bd.setStyleSheet(f"color:{TEXT_MID}; background:transparent; border:none;")
        lay.addWidget(bd)


# ─────────────────────────────────────────────
#  SEANS KARTI (RESPONSIVE)
# ─────────────────────────────────────────────
class SessionCard(QFrame):
    def __init__(self, session: dict, parent=None):
        super().__init__(parent)
        self.session = session
        self._pc = PRIORITY_COLORS.get(session["priority"], ACCENT)

        self.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Fixed)
        self.setMinimumWidth(0)
        self._set_style(False)

        self.lay = QVBoxLayout(self)
        self.lay.setContentsMargins(8, 6, 8, 6)
        self.lay.setSpacing(2)

        row1 = QHBoxLayout()
        row1.setContentsMargins(0, 0, 0, 0)
        row1.setSpacing(4)

        self.code_label = QLabel(session["course"])
        self.code_label.setMinimumWidth(0)

        self.time_label = QLabel(f"{session['start']}–{session['end']}")
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.time_label.setMinimumWidth(0)

        row1.addWidget(self.code_label, 1)
        row1.addWidget(self.time_label, 0)
        self.lay.addLayout(row1)

        self.name_label = QLabel(session["name"])
        self.name_label.setWordWrap(True)
        self.name_label.setMinimumWidth(0)
        self.lay.addWidget(self.name_label)

        row2 = QHBoxLayout()
        row2.setContentsMargins(0, 0, 0, 0)
        row2.setSpacing(4)

        stype = session["type"]
        self.tip_label = QLabel(f"{TYPE_ICONS.get(stype, '📌')} {stype}")
        self.tip_label.setMinimumWidth(0)

        self.pr_label = QLabel(PRIORITY_LABELS[session["priority"]])
        self.pr_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.pr_label.setMinimumWidth(0)

        row2.addWidget(self.tip_label, 1)
        row2.addWidget(self.pr_label, 0)
        self.lay.addLayout(row2)

        self.apply_scale(1.0)

    def apply_scale(self, scale: float):
        scale = max(0.68, min(scale, 1.00))

        self.setFixedHeight(max(74, int(90 * scale)))
        self.lay.setContentsMargins(
            max(5, int(8 * scale)),
            max(4, int(6 * scale)),
            max(5, int(8 * scale)),
            max(4, int(6 * scale)),
        )
        self.lay.setSpacing(max(2, int(2 * scale)))

        self.code_label.setFont(QFont("Segoe UI", max(8, int(10 * scale)), QFont.Weight.Bold))
        self.code_label.setStyleSheet(f"color:{self._pc}; background:transparent; border:none;")

        self.time_label.setFont(QFont("Segoe UI", max(7, int(8 * scale))))
        self.time_label.setStyleSheet(f"color:{TEXT_LO}; background:transparent; border:none;")

        self.name_label.setFont(QFont("Segoe UI", max(8, int(9 * scale))))
        self.name_label.setStyleSheet(f"color:{TEXT_HI}; background:transparent; border:none;")

        badge_v = max(1, int(1 * scale))
        badge_h = max(4, int(5 * scale))

        self.tip_label.setFont(QFont("Segoe UI", max(7, int(8 * scale)), QFont.Weight.Bold))
        self.tip_label.setStyleSheet(f"""
            color:{TEXT_MID};
            background:rgba(255,255,255,0.05);
            border-radius:4px;
            padding:{badge_v}px {badge_h}px;
            border:none;
        """)

        self.pr_label.setFont(QFont("Segoe UI", max(7, int(8 * scale)), QFont.Weight.Bold))
        self.pr_label.setStyleSheet(f"color:{self._pc}; background:transparent; border:none;")

    def _set_style(self, hov):
        bg = BG_HOVER if hov else BG_CARD
        self.setStyleSheet(f"""
            QFrame {{
                background-color:{bg};
                border:1px solid {BORDER_LT};
                border-left:3px solid {self._pc};
                border-radius:8px;
            }}
        """)

    def enterEvent(self, e):
        self._set_style(True)
        super().enterEvent(e)

    def leaveEvent(self, e):
        self._set_style(False)
        super().leaveEvent(e)


# ─────────────────────────────────────────────
#  GÜN SÜTUNU (RESPONSIVE)
# ─────────────────────────────────────────────
class DayColumn(QWidget):
    def __init__(self, day_name: str, sessions: list, parent=None):
        super().__init__(parent)

        self.day_name = day_name
        self.sessions = sessions
        self.cards = []

        self.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Fixed)
        self.setMinimumWidth(0)

        self.lay = QVBoxLayout(self)
        self.lay.setContentsMargins(4, 0, 4, 0)
        self.lay.setSpacing(6)
        self.lay.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.hdr = QLabel(day_name)
        self.hdr.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hdr.setMinimumWidth(0)

        if sessions:
            self.hdr.setStyleSheet(f"""
                color:{TEXT_HI};
                background-color:{BG_CARD};
                border:1px solid {BORDER_LT};
                border-radius:8px;
            """)
        else:
            self.hdr.setStyleSheet(f"""
                color:{TEXT_LO};
                background-color:transparent;
                border:1px solid {BORDER_LT};
                border-radius:8px;
            """)

        self.lay.addWidget(self.hdr)

        if sessions:
            for s in sessions:
                card = SessionCard(s)
                self.cards.append(card)
                self.lay.addWidget(card)
        else:
            self.rest = QLabel("—\nDinlenme")
            self.rest.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.rest.setMinimumWidth(0)
            self.rest.setStyleSheet(f"color:{TEXT_LO}; background:transparent;")
            self.lay.addWidget(self.rest)

        self.apply_scale(1.0)

    def apply_scale(self, scale: float):
        scale = max(0.68, min(scale, 1.00))

        self.lay.setContentsMargins(
            max(2, int(4 * scale)),
            0,
            max(2, int(4 * scale)),
            0
        )
        self.lay.setSpacing(max(4, int(6 * scale)))

        self.hdr.setFixedHeight(max(28, int(34 * scale)))
        self.hdr.setFont(QFont("Segoe UI", max(8, int(10 * scale)), QFont.Weight.Bold))

        if self.sessions:
            for card in self.cards:
                card.apply_scale(scale)
        else:
            self.rest.setFixedHeight(max(46, int(60 * scale)))
            self.rest.setFont(QFont("Segoe UI", max(8, int(10 * scale))))


# ─────────────────────────────────────────────
#  GRADİENT ÇİZGİ
# ─────────────────────────────────────────────
class GradientSep(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(1)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    def paintEvent(self, e):
        p = QPainter(self)
        g = QLinearGradient(0, 0, self.width(), 0)
        g.setColorAt(0.0, QColor(BORDER))
        g.setColorAt(0.4, QColor(ACCENT))
        g.setColorAt(1.0, QColor(BORDER))
        p.fillRect(self.rect(), QBrush(g))


# ─────────────────────────────────────────────
#  ANA SAYFA
# ─────────────────────────────────────────────
class SuggestedPlanPage(QWidget):
    def __init__(self, user_id, db_manager, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.db_manager = db_manager

        self.setStyleSheet(f"background-color:{BG_MAIN};")
        self.setMinimumWidth(1180)

        self.day_columns = []

        self._build_ui()

    def _build_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setStyleSheet(f"""
            QScrollArea {{
                background:{BG_MAIN};
                border:none;
            }}
            QScrollBar:vertical {{
                width:6px;
                background:{BG_CARD};
                border-radius:3px;
            }}
            QScrollBar::handle:vertical {{
                background:{BORDER};
                border-radius:3px;
                min-height:30px;
            }}
            QScrollBar::handle:vertical:hover {{
                background:{ACCENT};
            }}
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {{
                height:0;
            }}
        """)

        content = QWidget()
        content.setStyleSheet(f"background-color:{BG_MAIN};")
        scroll.setWidget(content)
        outer.addWidget(scroll)

        root = QVBoxLayout(content)
        root.setContentsMargins(28, 24, 28, 20)
        root.setSpacing(0)

        # ── 1. BAŞLIK ──────────────────────────
        hdr = QHBoxLayout()
        left_col = QVBoxLayout()
        left_col.setSpacing(5)

        title = QLabel("Önerilen Ders Programı")
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        title.setStyleSheet(f"color:{TEXT_HI};")
        left_col.addWidget(title)

        badge_row = QHBoxLayout()
        badge_row.setSpacing(8)

        ai_b = QLabel("✦ AI Önerisi")
        ai_b.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        ai_b.setFixedHeight(22)
        ai_b.setStyleSheet(f"""
            color:{ACCENT};
            background:rgba(0,229,160,0.10);
            border:1px solid rgba(0,229,160,0.35);
            border-radius:5px;
            padding:2px 10px;
        """)

        wk_b = QLabel("Hafta: 21 Nis – 27 Nis 2025")
        wk_b.setFont(QFont("Segoe UI", 9))
        wk_b.setStyleSheet(f"color:{TEXT_LO};")

        badge_row.addWidget(ai_b)
        badge_row.addWidget(wk_b)
        badge_row.addStretch()
        left_col.addLayout(badge_row)

        hdr.addLayout(left_col)
        hdr.addStretch()

        self.refresh_btn = QPushButton("  🔄  Yeniden Oluştur")
        self.refresh_btn.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self.refresh_btn.setFixedHeight(42)
        self.refresh_btn.setMinimumWidth(180)
        self.refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.refresh_btn.setStyleSheet(f"""
            QPushButton {{
                background-color:{ACCENT};
                color:#111318;
                border-radius:8px;
                padding:0 20px;
            }}
            QPushButton:hover {{
                background-color:#00c88c;
            }}
            QPushButton:pressed {{
                background-color:#00a876;
            }}
        """)
        self.refresh_btn.clicked.connect(self._on_refresh)
        hdr.addWidget(self.refresh_btn, alignment=Qt.AlignmentFlag.AlignVCenter)

        root.addLayout(hdr)
        root.addSpacing(14)
        root.addWidget(GradientSep())
        root.addSpacing(16)

        # ── 2. İSTATİSTİK KARTLARI ─────────────
        stats_row = QHBoxLayout()
        stats_row.setSpacing(12)
        for icon, val, lbl, col in [
            ("⏱", "17.5 sa", "Haftalık Çalışma", ACCENT),
            ("📚", "4 Ders", "Aktif Ders", BLUE),
            ("🔥", "Cmt", "En Yoğun Gün", AMBER),
            ("🎯", "%87", "Odak Skoru", "#a78bfa"),
        ]:
            stats_row.addWidget(StatCard(icon, val, lbl, col))
        root.addLayout(stats_row)
        root.addSpacing(16)

        # ── 3. İÇGÖRÜ ŞERİDİ ──────────────────
        insight_lbl = QLabel("💡  Yapay Zeka İçgörüleri")
        insight_lbl.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        insight_lbl.setStyleSheet(f"color:{TEXT_MID};")
        root.addWidget(insight_lbl)
        root.addSpacing(8)

        iscroll = QScrollArea()
        iscroll.setFixedHeight(135)
        iscroll.setWidgetResizable(True)
        iscroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        iscroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        iscroll.setStyleSheet(f"""
            QScrollArea {{
                background:transparent;
                border:none;
            }}
            QScrollBar:horizontal {{
                height:4px;
                background:{BG_CARD};
                border-radius:2px;
            }}
            QScrollBar::handle:horizontal {{
                background:{BORDER};
                border-radius:2px;
                min-width:40px;
            }}
            QScrollBar::handle:horizontal:hover {{
                background:{ACCENT};
            }}
            QScrollBar::add-line:horizontal,
            QScrollBar::sub-line:horizontal {{
                width:0;
            }}
        """)

        icont = QWidget()
        icont.setStyleSheet("background:transparent;")
        ihbox = QHBoxLayout(icont)
        ihbox.setContentsMargins(0, 0, 0, 6)
        ihbox.setSpacing(12)

        for d in MOCK_INSIGHTS:
            ihbox.addWidget(InsightCard(d["icon"], d["title"], d["body"], d["color"]))

        ihbox.addStretch()
        iscroll.setWidget(icont)
        root.addWidget(iscroll)
        root.addSpacing(16)

        # ── 4. HAFTALIK PLAN BAŞLIĞI ───────────
        whdr = QHBoxLayout()
        wlbl = QLabel("📅  Haftalık Çalışma Planı")
        wlbl.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        wlbl.setStyleSheet(f"color:{TEXT_MID};")
        whdr.addWidget(wlbl)
        whdr.addStretch()

        for key, color in PRIORITY_COLORS.items():
            dot = QLabel("●")
            dot.setStyleSheet(f"color:{color}; font-size:9px; background:transparent;")

            nlbl = QLabel(PRIORITY_LABELS[key])
            nlbl.setStyleSheet(f"color:{TEXT_LO}; font-size:10px; background:transparent;")

            whdr.addWidget(dot)
            whdr.addWidget(nlbl)
            whdr.addSpacing(6)

        root.addLayout(whdr)
        root.addSpacing(8)

        # ── 4b. HAFTALIK GRID ──────────────────
        self.grid_frame = QFrame()
        self.grid_frame.setStyleSheet(f"""
            QFrame {{
                background-color:{BG_MAIN};
                border:1px solid {BORDER_LT};
                border-radius:12px;
            }}
        """)

        self.grid_layout = QHBoxLayout(self.grid_frame)
        self.grid_layout.setContentsMargins(10, 10, 10, 10)
        self.grid_layout.setSpacing(6)

        self.day_columns = []

        for day in ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]:
            col = DayColumn(day, MOCK_SUGGESTIONS.get(day, []))
            self.day_columns.append(col)
            self.grid_layout.addWidget(col, stretch=1)

        root.addWidget(self.grid_frame)
        root.addSpacing(14)

        # ── 5. ALT NOT ─────────────────────────
        foot = QLabel(
            "Bu program ders takviminiz, geçmiş çalışma veriniz ve AI analizi baz alınarak oluşturulmuştur.  "
            "Manuel düzenleme için 'Ders Programı' ekranını kullanın."
        )
        foot.setFont(QFont("Segoe UI", 9))
        foot.setWordWrap(True)
        foot.setStyleSheet(f"color:{TEXT_LO}; background:transparent;")
        root.addWidget(foot)
        root.addStretch()

        QTimer.singleShot(0, self._update_week_grid_scale)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self._update_week_grid_scale()

    def _update_week_grid_scale(self):
        if not hasattr(self, "grid_frame") or not hasattr(self, "grid_layout"):
            return

        margins = self.grid_layout.contentsMargins()
        spacing = self.grid_layout.spacing()

        available_width = (
            self.grid_frame.width()
            - margins.left()
            - margins.right()
            - spacing * 6
        )

        if available_width <= 0:
            return

        per_col_width = available_width / 7
        base_col_width = 170.0

        scale = per_col_width / base_col_width
        scale = max(0.68, min(scale, 1.0))

        grid_margin = max(6, int(10 * scale))
        grid_spacing = max(4, int(6 * scale))

        self.grid_layout.setContentsMargins(
            grid_margin, grid_margin, grid_margin, grid_margin
        )
        self.grid_layout.setSpacing(grid_spacing)

        for col in self.day_columns:
            col.apply_scale(scale)

    def _on_refresh(self):
        self.refresh_btn.setText("  ⏳  Oluşturuluyor...")
        self.refresh_btn.setEnabled(False)
        QTimer.singleShot(1800, self._finish_refresh)

    def _finish_refresh(self):
        self.refresh_btn.setText("  🔄  Yeniden Oluştur")
        self.refresh_btn.setEnabled(True)