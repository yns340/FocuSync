# ui/suggested_plan_page.py

import uuid
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QFrame, QSizePolicy, QGraphicsDropShadowEffect, QMessageBox
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QColor, QPainter, QPen, QLinearGradient, QBrush
from datetime import datetime

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
DAYS_ORDER      = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]

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
        self._pc = PRIORITY_COLORS.get(session.get("priority", "medium"), ACCENT)

        self.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Fixed)
        self.setMinimumWidth(0)
        self._set_style(False)

        self.lay = QVBoxLayout(self)
        self.lay.setContentsMargins(8, 6, 8, 6)
        self.lay.setSpacing(2)

        row1 = QHBoxLayout()
        row1.setContentsMargins(0, 0, 0, 0)
        row1.setSpacing(4)

        # Veritabanı modeline uygun anahtarlar kullanılıyor
        self.code_label = QLabel(str(session.get("course_id", "DERS")))
        self.code_label.setMinimumWidth(0)

        self.time_label = QLabel(f"{session.get('start_time', '')}–{session.get('end_time', '')}")
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.time_label.setMinimumWidth(0)

        row1.addWidget(self.code_label, 1)
        row1.addWidget(self.time_label, 0)
        self.lay.addLayout(row1)

        self.name_label = QLabel(str(session.get("course_name", "")))
        self.name_label.setWordWrap(True)
        self.name_label.setMinimumWidth(0)
        self.lay.addWidget(self.name_label)

        row2 = QHBoxLayout()
        row2.setContentsMargins(0, 0, 0, 0)
        row2.setSpacing(4)

        stype = session.get("type", "Tekrar")
        self.tip_label = QLabel(f"{TYPE_ICONS.get(stype, '📌')} {stype}")
        self.tip_label.setMinimumWidth(0)

        self.pr_label = QLabel(PRIORITY_LABELS.get(session.get("priority", "medium"), "Orta"))
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

        self.current_plan = {}
        self.current_insights = []
        self.stats = {"total_hours": 0, "active_courses": 0, "busiest_day": "-", "focus_score": "%0"}
        
        self.day_columns = []
        self.dynamic_container = None 

        self._build_ui()
        self._load_data() 

    def _build_ui(self):
        self.outer = QVBoxLayout(self)
        self.outer.setContentsMargins(0, 0, 0, 0)
        self.outer.setSpacing(0)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll.setStyleSheet(f"""
            QScrollArea {{ background:{BG_MAIN}; border:none; }}
            QScrollBar:vertical {{ width:6px; background:{BG_CARD}; border-radius:3px; }}
            QScrollBar::handle:vertical {{ background:{BORDER}; border-radius:3px; min-height:30px; }}
            QScrollBar::handle:vertical:hover {{ background:{ACCENT}; }}
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {{ height:0; }}
        """)

        self.content = QWidget()
        self.content.setStyleSheet(f"background-color:{BG_MAIN};")
        self.scroll.setWidget(self.content)
        self.outer.addWidget(self.scroll)

        self.root = QVBoxLayout(self.content)
        self.root.setContentsMargins(28, 24, 28, 20)
        self.root.setSpacing(0)

        self._render_header()
        
        self.root.addStretch()

    def _render_header(self):
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
        
        self.wk_b = QLabel(f"Başlangıç: {datetime.now().strftime('%d %b %Y')}")
        self.wk_b.setFont(QFont("Segoe UI", 9))
        self.wk_b.setStyleSheet(f"color:{TEXT_LO};")

        badge_row.addWidget(ai_b)
        badge_row.addWidget(self.wk_b)
        badge_row.addStretch()
        left_col.addLayout(badge_row)
        hdr.addLayout(left_col)
        hdr.addStretch()

        self.pdf_import_btn = QPushButton("📄 PDF'den Aktar")
        self.pdf_import_btn.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self.pdf_import_btn.setFixedHeight(42)
        self.pdf_import_btn.setMinimumWidth(150)
        self.pdf_import_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.pdf_import_btn.setStyleSheet(f"""
            QPushButton {{ background-color: #0099ff; color:#111318; border-radius:8px; padding:0 15px; }}
            QPushButton:hover {{ background-color:#007acc; }}
            QPushButton:pressed {{ background-color:#005c99; }}
        """)
        self.pdf_import_btn.clicked.connect(self.start_pdf_import)
        hdr.addWidget(self.pdf_import_btn, alignment=Qt.AlignmentFlag.AlignVCenter)
        hdr.addSpacing(10)

        self.refresh_btn = QPushButton("  🔄  Yeniden Oluştur")
        self.refresh_btn.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self.refresh_btn.setFixedHeight(42)
        self.refresh_btn.setMinimumWidth(180)
        self.refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.refresh_btn.setStyleSheet(f"""
            QPushButton {{ background-color:{ACCENT}; color:#111318; border-radius:8px; padding:0 20px; }}
            QPushButton:hover {{ background-color:#00c88c; }}
            QPushButton:pressed {{ background-color:#00a876; }}
        """)
        self.refresh_btn.clicked.connect(self._on_refresh)
        hdr.addWidget(self.refresh_btn, alignment=Qt.AlignmentFlag.AlignVCenter)

        self.root.insertLayout(0, hdr)
        self.root.insertSpacing(1, 14)
        self.root.insertWidget(2, GradientSep())
        self.root.insertSpacing(3, 16)

    def _render_content(self):
        if self.dynamic_container is not None:
            self.root.removeWidget(self.dynamic_container)
            self.dynamic_container.deleteLater()
            
        self.dynamic_container = QWidget()
        self.dynamic_container.setStyleSheet("background-color: transparent;")
        self.dynamic_layout = QVBoxLayout(self.dynamic_container)
        self.dynamic_layout.setContentsMargins(0, 0, 0, 0)
        self.dynamic_layout.setSpacing(0)
        
        self.root.insertWidget(4, self.dynamic_container)

        if not self.current_plan:
            no_plan_lbl = QLabel("Henüz oluşturulmuş bir çalışma planınız yok. 'Yeniden Oluştur' butonuna tıklayarak verilerinize göre bir plan oluşturabilirsiniz.")
            no_plan_lbl.setStyleSheet(f"color:{TEXT_MID}; font-size: 14px;")
            self.dynamic_layout.addWidget(no_plan_lbl)
            return

        # ── 2. İSTATİSTİK KARTLARI ─────────────
        stats_row = QHBoxLayout()
        stats_row.setSpacing(12)
        stats_row.addWidget(StatCard("⏱", f"{self.stats.get('total_hours', 0)} sa", "Haftalık Çalışma", ACCENT))
        stats_row.addWidget(StatCard("📚", f"{self.stats.get('active_courses', 0)} Ders", "Aktif Ders", BLUE))
        stats_row.addWidget(StatCard("🔥", self.stats.get('busiest_day', '-'), "En Yoğun Gün", AMBER))
        stats_row.addWidget(StatCard("🎯", self.stats.get('focus_score', '%0'), "Tahmini Odak", "#a78bfa"))
        self.dynamic_layout.addLayout(stats_row)
        self.dynamic_layout.addSpacing(16)

        # ── 3. İÇGÖRÜ ŞERİDİ ──────────────────
        insight_lbl = QLabel("💡  Yapay Zeka İçgörüleri")
        insight_lbl.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        insight_lbl.setStyleSheet(f"color:{TEXT_MID};")
        self.dynamic_layout.addWidget(insight_lbl)
        self.dynamic_layout.addSpacing(8)

        iscroll = QScrollArea()
        iscroll.setFixedHeight(135)
        iscroll.setWidgetResizable(True)
        iscroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        iscroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        iscroll.setStyleSheet(f"""
            QScrollArea {{ background:transparent; border:none; }}
            QScrollBar:horizontal {{ height:4px; background:{BG_CARD}; border-radius:2px; }}
            QScrollBar::handle:horizontal {{ background:{BORDER}; border-radius:2px; min-width:40px; }}
            QScrollBar::handle:horizontal:hover {{ background:{ACCENT}; }}
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{ width:0; }}
        """)
        icont = QWidget()
        icont.setStyleSheet("background:transparent;")
        ihbox = QHBoxLayout(icont)
        ihbox.setContentsMargins(0, 0, 0, 6)
        ihbox.setSpacing(12)
        
        for d in self.current_insights:
            ihbox.addWidget(InsightCard(d["icon"], d["title"], d["body"], d["color"]))
        
        ihbox.addStretch()
        iscroll.setWidget(icont)
        self.dynamic_layout.addWidget(iscroll)
        self.dynamic_layout.addSpacing(16)

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

        self.dynamic_layout.addLayout(whdr)
        self.dynamic_layout.addSpacing(8)

        # ── 5. HAFTALIK GRID ──────────────────
        self.grid_frame = QFrame()
        self.grid_frame.setStyleSheet(f"background-color:{BG_MAIN}; border:1px solid {BORDER_LT}; border-radius:12px;")
        self.grid_layout = QHBoxLayout(self.grid_frame)
        self.grid_layout.setContentsMargins(10, 10, 10, 10)
        self.grid_layout.setSpacing(6)
        
        self.day_columns.clear()
        for day in DAYS_ORDER:
            col = DayColumn(day, self.current_plan.get(day, []))
            self.day_columns.append(col)
            self.grid_layout.addWidget(col, stretch=1)
            
        self.dynamic_layout.addWidget(self.grid_frame)
        self.dynamic_layout.addSpacing(14)
        
        # ── 6. ALT NOT ─────────────────────────
        foot = QLabel(
            "Bu program ders takviminiz, geçmiş çalışma veriniz ve AI analizi baz alınarak oluşturulmuştur.  "
            "Manuel düzenleme için 'Ders Programı' ekranını kullanın."
        )
        foot.setFont(QFont("Segoe UI", 9))
        foot.setWordWrap(True)
        foot.setStyleSheet(f"color:{TEXT_LO}; background:transparent;")
        self.dynamic_layout.addWidget(foot)

        QTimer.singleShot(0, self._update_week_grid_scale)

    def _load_data(self):
        success, plan_data = self.db_manager.get_study_plan(self.user_id)
        if success and isinstance(plan_data, dict):
            self.current_plan = plan_data.get("weekly_sessions", {})
            self._calculate_stats_and_insights()
            self._render_content()
        else:
            self._render_content()

    def _on_refresh(self):
        self.refresh_btn.setText("  ⏳  Oluşturuluyor...")
        self.refresh_btn.setEnabled(False)
        QTimer.singleShot(500, self._run_algorithm)

    def _run_algorithm(self):
        success_c, courses = self.db_manager.get_courses(self.user_id)
        success_s, schedule_data = self.db_manager.get_schedule(self.user_id)
        
        if not success_c or not isinstance(courses, list):
            QMessageBox.warning(self, "Hata", "Plan oluşturulabilmesi için kayıtlı derslerinizin olması gereklidir.")
            self._reset_btn()
            return
            
        active_courses = [c for c in courses if isinstance(c, dict) and c.get("is_active", True)]
        if not active_courses:
            QMessageBox.warning(self, "Hata", "Aktif durumda hiçbir dersiniz yok. Lütfen programınıza ders ekleyin.")
            self._reset_btn()
            return

        raw_routine = schedule_data.get("weekly_routine", {}) if success_s and isinstance(schedule_data, dict) else {}
        routine = raw_routine if isinstance(raw_routine, dict) else {}
        
        new_plan = {day: [] for day in DAYS_ORDER}
        
        for course in active_courses:
            diff = course.get("difficulty_level", 3.0)
            hours = course.get("weekly_hours", 2)
            
            required_hours = int(hours * (diff / 2.0))
            if required_hours < 1: required_hours = 1
            
            priority = "high" if diff >= 4.0 else ("medium" if diff >= 2.5 else "low")
            
            assigned_hours = 0
            for day in DAYS_ORDER:
                if assigned_hours >= required_hours: break
                
                day_str = str(day)
                fixed_classes_today = 0
                
                if day_str in routine:
                    day_data = routine[day_str]
                    if isinstance(day_data, list):
                        fixed_classes_today = len(day_data)

                if fixed_classes_today >= 4: continue 
                
                start_hour = 17 + len(new_plan[day]) * 2 
                if start_hour > 22: continue
                
                session_len = 1.5 if diff > 3 else 1.0
                end_hour = int(start_hour + session_len)
                end_min = "30" if session_len == 1.5 else "00"
                
                # --- VERİTABANI DÖKÜMANIYLA %100 UYUMLU FORMAT ---
                # Arkadaşının hazırladığı standartlara tam uyumlu yapı kuruldu
                new_plan[day].append({
                    "session_id": str(uuid.uuid4()),  # Eşsiz kimlik oluşturucu
                    "course_id": course.get("course_id", "DERS"),
                    "course_name": course.get("course_name", ""),
                    "planned_duration": int(session_len * 60), # Dakika cinsinden
                    "is_completed": False,
                    
                    # Arayüzün (UI) bozulmaması için ekstra alanlar
                    "start_time": f"{start_hour:02d}:00",
                    "end_time": f"{end_hour:02d}:{end_min}",
                    "type": "Yeni Konu" if assigned_hours == 0 else "Tekrar",
                    "priority": priority
                })
                assigned_hours += session_len

        start_date = datetime.now().strftime('%Y-%m-%d')
        save_success, msg = self.db_manager.save_study_plan(self.user_id, start_date, new_plan)
        
        if save_success:
            self.current_plan = new_plan
            self._calculate_stats_and_insights()
            self._render_content()
        else:
            QMessageBox.critical(self, "Kayıt Hatası", msg)
            
        self._reset_btn()

    def _calculate_stats_and_insights(self):
        total_hours = 0
        courses_set = set()
        day_counts = {}
        
        if not isinstance(self.current_plan, dict):
            self.current_plan = {}
            
        for day, sessions in self.current_plan.items():
            if not isinstance(sessions, list):
                continue
                
            day_counts[day] = len(sessions)
            for s in sessions:
                if not isinstance(s, dict):
                    continue
                    
                # course_id'ye göre güncellendi
                courses_set.add(str(s.get("course_id", "")))
                
                # start_time ve end_time alanlarına göre güncellendi
                start_val = s.get("start_time", "")
                end_val = s.get("end_time", "")
                
                start_str = str(start_val).strip() if start_val is not None else ""
                end_str = str(end_val).strip() if end_val is not None else ""
                
                h1, m1, h2, m2 = 0, 0, 0, 0
                
                try:
                    if ":" in start_str:
                        h1_s, m1_s = start_str.split(":", 1)
                        h1 = int(h1_s) if h1_s.strip() else 0
                        m1 = int(m1_s) if m1_s.strip() else 0
                        
                    if ":" in end_str:
                        h2_s, m2_s = end_str.split(":", 1)
                        h2 = int(h2_s) if h2_s.strip() else 0
                        m2 = int(m2_s) if m2_s.strip() else 0
                        
                    if h2 > 0 or m2 > 0:
                        total_hours += (h2 - h1) + ((m2 - m1) / 60.0)
                except Exception:
                    pass
                
        busiest_day = max(day_counts, key=day_counts.get) if day_counts and sum(day_counts.values()) > 0 else "-"
        
        self.stats = {
            "total_hours": round(total_hours, 1) if total_hours > 0 else 0,
            "active_courses": len(courses_set),
            "busiest_day": busiest_day[:3] if busiest_day != "-" else "-", 
            "focus_score": "%85" 
        }
        
        self.current_insights = []
        if total_hours > 20:
            self.current_insights.append({"icon": "⚡", "title": "Yoğun Hafta!", "body": f"Bu hafta {round(total_hours, 1)} saatlik ağır bir planınız var. Molaları aksatmayın.", "color": RED})
        elif total_hours > 0:
            self.current_insights.append({"icon": "✅", "title": "Denge İyi", "body": "Haftalık yük dağılımı dengeli. Planınıza uymak veriminizi artıracaktır.", "color": ACCENT})
            
        if self.stats["active_courses"] > 0 and busiest_day != "-":
            self.current_insights.append({"icon": "🎯", "title": "Algoritma Tavsiyesi", "body": f"Öncelikli dersler {busiest_day} gününe yoğunlaştırıldı. Erken saatleri değerlendirin.", "color": BLUE})

    def _reset_btn(self):
        self.refresh_btn.setText("  🔄  Yeniden Oluştur")
        self.refresh_btn.setEnabled(True)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self._update_week_grid_scale()

    def _update_week_grid_scale(self):
        try:
            if getattr(self, "grid_frame", None) is None or getattr(self, "grid_layout", None) is None:
                return

            margins = self.grid_layout.contentsMargins()
            spacing = self.grid_layout.spacing()
            available_width = self.grid_frame.width() - margins.left() - margins.right() - spacing * 6

            if available_width <= 0: return
            per_col_width = available_width / 7
            base_col_width = 170.0

            scale = per_col_width / base_col_width
            scale = max(0.68, min(scale, 1.0))
            
            grid_margin = max(6, int(10 * scale))
            grid_spacing = max(4, int(6 * scale))

            self.grid_layout.setContentsMargins(grid_margin, grid_margin, grid_margin, grid_margin)
            self.grid_layout.setSpacing(grid_spacing)

            for col in self.day_columns:
                col.apply_scale(scale)
        except Exception:
            pass

    def start_pdf_import(self):
        """Gelişmiş Regex ile PDF okuma ve Düzenleme Tablosu"""
        import pdfplumber
        import re
        from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QFileDialog, QDialog

        file_path, _ = QFileDialog.getOpenFileName(self, "PDF Seç", "", "PDF Dosyaları (*.pdf)")
        if not file_path: return

        try:
            with pdfplumber.open(file_path) as pdf:
                full_text = "\n".join([page.extract_text() for page in pdf.pages])

            # 1. Gelişmiş Regex 
            pattern = r"([A-Z]{2,4}[-\s]?\d{3})\s+([A-Za-zÇŞĞÜİÖçşğüiö\s\-\(\)]+)"
            matches = re.findall(pattern, full_text)
            
            if not matches:
                QMessageBox.warning(self, "Hata", "Ders formatı algılanamadı! Manuel girişe yönlendiriliyorsunuz.") 
                return

            # 2. Onay ve Düzenleme Diyaloğu 
            dialog = QDialog(self)
            dialog.setWindowTitle("Ders Programı Düzenleme ve Onay")
            dialog.setMinimumWidth(600)
            d_lay = QVBoxLayout(dialog)

            desc = QLabel("PDF'ten çekilen dersler aşağıdadır. Hatalı olanları üzerine tıklayıp düzeltebilirsiniz.")
            desc.setWordWrap(True)
            d_lay.addWidget(desc)

            table = QTableWidget(len(matches), 3)
            table.setHorizontalHeaderLabels(["Ders Kodu", "Ders Adı", "Başlangıç Zorluğu"])
            table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

            for i, (code, name) in enumerate(matches):
                table.setItem(i, 0, QTableWidgetItem(code.strip()))
                table.setItem(i, 1, QTableWidgetItem(name.strip()))
                table.setItem(i, 2, QTableWidgetItem("3.0")) 

            d_lay.addWidget(table)

            btn_box = QHBoxLayout()
            save_btn = QPushButton("Veritabanına Kaydet")
            save_btn.setStyleSheet("background: #00e5a0; color: #111318; font-weight: bold; padding: 10px;")
            cancel_btn = QPushButton("İptal")
            btn_box.addWidget(cancel_btn)
            btn_box.addWidget(save_btn)
            d_lay.addLayout(btn_box)

            save_btn.clicked.connect(dialog.accept)
            cancel_btn.clicked.connect(dialog.reject)

            # 3. Onay Verildiyse Kaydet
            if dialog.exec() == QDialog.DialogCode.Accepted:
                try:
                    success_count = 0
                    for row in range(table.rowCount()):
                        c_id = table.item(row, 0).text().strip()
                        c_name = table.item(row, 1).text().strip()
                    
                        try:
                            c_diff = float(table.item(row, 2).text().replace(',', '.'))
                        except:
                            c_diff = 3.0 
                            
                        success, _ = self.db_manager.add_course(
                            user_id=self.user_id,
                            course_id=c_id,
                            course_name=c_name,
                            difficulty_level=c_diff,
                            weekly_hours=3
                        )
                        if success:
                            success_count += 1

                    if success_count > 0:
                        QMessageBox.information(self, "Başarılı", f"{success_count} ders Firebase'e işlendi.")
                        self._load_data() 
                
                except Exception as db_e:
                    QMessageBox.critical(self, "Hata", f"Veritabanı kaydı sırasında hata oluştu: {db_e}")

        except Exception as e:
            # Genel PDF işleme hatası
            QMessageBox.critical(self, "Hata", f"PDF işleme hatası: {e}")