import sys
import types
import pytest

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox, QPushButton, QDialog

# Keep focus-page tests independent from webcam / AI implementation details.
class FakeSignal:
    def __init__(self):
        self._callbacks = []

    def connect(self, callback):
        self._callbacks.append(callback)

    def emit(self, *args, **kwargs):
        for callback in list(self._callbacks):
            callback(*args, **kwargs)


class FakeHeadTracker:
    def __init__(self):
        self.session_completed = FakeSignal()
        self.focus_status_changed = FakeSignal()
        self.face_missing = FakeSignal()
        self.error_occurred = FakeSignal()
        self.frame_processed = FakeSignal()
        self.started = False
        self.stopped = False
        self.is_running = False
        self.total_session_time = 10
        self.total_focus_time = 8

    def start(self):
        self.started = True
        self.is_running = True

    def stop(self):
        self.stopped = True
        self.is_running = False


fake_head_tracker_module = types.ModuleType("head_tracker")
fake_head_tracker_module.HeadTracker = FakeHeadTracker
sys.modules["head_tracker"] = fake_head_tracker_module

fake_decision_engine_module = types.ModuleType("decision_engine")
fake_decision_engine_module.GeneticScheduler = object
fake_decision_engine_module.FocusDecisionEngine = lambda: object()

class FakeSimulatedAnnealingScheduler:
    def __init__(self, courses, history):
        self.courses = courses
        self.history = history

    def generate_plan(self):
        return {"09:00": self.courses[0] if self.courses else "Genel Çalışma"}

fake_decision_engine_module.SimulatedAnnealingScheduler = FakeSimulatedAnnealingScheduler
sys.modules["decision_engine"] = fake_decision_engine_module

from ui.courses_page import CourseDialog, CoursesPage, CourseCard
import ui.focus_page as fp
from ui.focus_page import FocusPage, FocusCircle, NotificationBanner
import ui.dashboard_page as dashboard_module
import ui.profile_page as profile_module
import ui.focus_page as focus_module
from ui.main_window import MainWindow


class FakeDBManager:
    def __init__(self):
        self.add_course_calls = []
        self.delete_course_calls = []
        self.focus_session_ids = []
        self.focus_sessions = []
        self.study_plans = []
        self.deleted_courses = []
        self.courses = [
            {
                "course_id": "bm314",
                "course_name": "Software Engineering",
                "difficulty_level": 3.5,
                "weekly_hours": 4,
                "is_active": True,
                "target_grade": 85,
                "exam_date": "10.05.2026",
                "exam_grades": {"Vize 1": "80", "Final": ""},
                "exam_weights": {"Vize 1": 40, "Final": 60},
            },
            {
                "course_id": "archived",
                "course_name": "Archived Course",
                "difficulty_level": 2.0,
                "weekly_hours": 2,
                "is_active": False,
                "target_grade": 60,
            },
        ]

    # CoursesPage
    def get_schedule_course_ids(self, user_id):
        return True, ["bm314"]

    def get_courses(self, user_id):
        return True, list(self.courses)

    def add_course(self, **kwargs):
        self.add_course_calls.append(kwargs)
        return True, "Course saved."

    def delete_course(self, user_id, course_id):
        self.delete_course_calls.append((user_id, course_id))
        self.deleted_courses.append(course_id)
        return True, "Course deleted."

    # FocusPage
    def prepare_focus_session_id(self):
        session_id = "focus_123"
        self.focus_session_ids.append(session_id)
        return session_id

    def add_focus_session(self, user_id, study_plan_session_id, course_id, actual_focus_time, head_tilt_degree, focus_score, status):
        self.focus_sessions.append({
            "user_id": user_id,
            "study_plan_session_id": study_plan_session_id,
            "course_id": course_id,
            "actual_focus_time": actual_focus_time,
            "head_tilt_degree": head_tilt_degree,
            "focus_score": focus_score,
            "status": status,
        })
        return True, "Focus session saved."

    def get_weekly_analysis(self, user_id):
        return True, {"09:00": 70, "11:00": 80}

    def save_study_plan(self, **kwargs):
        self.study_plans.append(kwargs)
        return True, "Plan saved."

    def update_course_difficulty(self, user_id, course_id, direction):
        return True, "Difficulty updated."

    # DashboardPage used by MainWindow
    def get_dashboard_stats(self, user_id):
        return True, {
            "user_name": "Kerem",
            "avg_focus_score": 80,
            "course_count": 2,
            "total_study_time": 40,
            "violation_count": 1,
        }

    def get_course_risk_analysis(self, user_id):
        return True, []

    # ProfilePage used by MainWindow
    def get_user_profile(self, user_id):
        return True, {
            "name": "Kerem",
            "surname": "Kapısız",
            "school": "Gazi",
            "email": "kerem@example.com",
            "password": "oldpass",
        }

    def update_user_profile(self, *args, **kwargs):
        return True, "Profile updated."

    # Schedule / Exams used by MainWindow only if showEvent triggers
    def get_schedule(self, user_id):
        return False, None

    def get_exam_schedule(self, user_id):
        return False, None


class FakeWhitelistPage:
    def __init__(self):
        self.focus_session_id = None
        self.started = False
        self.stopped = False

    def set_focus_session_id(self, focus_session_id):
        self.focus_session_id = focus_session_id

    def start_monitoring(self):
        self.started = True
        return True

    def stop_monitoring(self):
        self.stopped = True


@pytest.fixture
def message_calls(monkeypatch):
    calls = []

    def fake_warning(*args, **kwargs):
        calls.append(("warning", args[1] if len(args) > 1 else "", args[2] if len(args) > 2 else ""))
        return QMessageBox.StandardButton.Ok

    def fake_information(*args, **kwargs):
        calls.append(("information", args[1] if len(args) > 1 else "", args[2] if len(args) > 2 else ""))
        return QMessageBox.StandardButton.Ok

    def fake_critical(*args, **kwargs):
        calls.append(("critical", args[1] if len(args) > 1 else "", args[2] if len(args) > 2 else ""))
        return QMessageBox.StandardButton.Ok

    def fake_question(*args, **kwargs):
        calls.append(("question", args[1] if len(args) > 1 else "", args[2] if len(args) > 2 else ""))
        return QMessageBox.StandardButton.Yes

    monkeypatch.setattr(QMessageBox, "warning", fake_warning)
    monkeypatch.setattr(QMessageBox, "information", fake_information)
    monkeypatch.setattr(QMessageBox, "critical", fake_critical)
    monkeypatch.setattr(QMessageBox, "question", fake_question)
    return calls


def find_button(widget, text):
    for button in widget.findChildren(QPushButton):
        if text in button.text():
            return button
    available = [b.text() for b in widget.findChildren(QPushButton)]
    raise AssertionError(f"Button not found: {text}. Available: {available}")


# =============================================================================
# CourseDialog / CoursesPage UI tests
# =============================================================================

def test_course_dialog_empty_id_shows_warning(qtbot, message_calls):
    dialog = CourseDialog(existing_ids=[])
    qtbot.addWidget(dialog)

    dialog.name_input.setText("Software Engineering")
    dialog.validate_and_accept()

    assert dialog.result() == 0
    assert any(call[0] == "warning" for call in message_calls)


def test_course_dialog_duplicate_id_blocks_accept(qtbot, message_calls):
    dialog = CourseDialog(existing_ids=["bm314"])
    qtbot.addWidget(dialog)

    dialog.id_input.setText("BM314")
    dialog.name_input.setText("Software Engineering")
    dialog.validate_and_accept()

    assert dialog.result() == 0
    assert any("zaten mevcut" in call[2] for call in message_calls)


def test_course_dialog_get_data_normalizes_values(qtbot, message_calls):
    dialog = CourseDialog(existing_ids=[])
    qtbot.addWidget(dialog)

    dialog.id_input.setText(" BM 314 ")
    dialog.name_input.setText("Software Engineering")
    dialog.diff_slider.setValue(45)
    dialog.hours_input.setValue(4)
    dialog.target_input.setValue(85)

    data = dialog.get_data()

    assert data["course_id"] == "bm314"
    assert data["course_name"] == "Software Engineering"
    assert data["difficulty_level"] == 4.5
    assert data["weekly_hours"] == 4
    assert data["target_grade"] == 85


def test_course_dialog_weight_over_100_disables_save(qtbot, message_calls):
    course_data = {
        "course_id": "bm314",
        "course_name": "Software Engineering",
        "exam_grades": {"Vize 1": "80", "Final": ""},
        "exam_weights": {"Vize 1": 80, "Final": 30},
    }
    dialog = CourseDialog(course_data=course_data)
    qtbot.addWidget(dialog)

    assert dialog.save_btn.isEnabled() is False
    assert "Ağırlık" in dialog.save_btn.text()


def test_courses_page_load_data_populates_active_and_inactive_grids(qtbot, message_calls):
    page = CoursesPage("user_123", FakeDBManager())
    qtbot.addWidget(page)

    page.load_data()

    assert page.active_grid.count() == 1
    assert page.inactive_grid.count() == 1
    assert page.all_course_ids == ["bm314", "archived"]
    assert page.schedule_course_ids == ["bm314"]


def test_courses_page_save_course_calls_db_and_reload(qtbot, message_calls):
    db = FakeDBManager()
    page = CoursesPage("user_123", db)
    qtbot.addWidget(page)

    data = {
        "course_id": "ceng318",
        "course_name": "Microprocessors",
        "difficulty_level": 4.0,
        "weekly_hours": 3,
        "exam_date": None,
        "is_active": True,
        "target_grade": 90,
        "exam_weights": {},
    }

    page._save_course_to_db(data)

    assert len(db.add_course_calls) == 1
    assert db.add_course_calls[0]["course_id"] == "ceng318"


def test_courses_page_delete_course_calls_db_when_confirmed(qtbot, message_calls):
    db = FakeDBManager()
    page = CoursesPage("user_123", db)
    qtbot.addWidget(page)

    page._delete_course({"course_id": "archived"})

    assert db.delete_course_calls == [("user_123", "archived")]


# =============================================================================
# FocusPage UI tests
# =============================================================================

def test_focus_circle_clamps_value(qtbot):
    circle = FocusCircle()
    qtbot.addWidget(circle)

    circle.set_value(150, "#ff6b35")
    assert circle.value == 100
    assert circle.color == "#ff6b35"

    circle.set_value(-20)
    assert circle.value == 0


def test_notification_banner_show_warning(qtbot):
    banner = NotificationBanner()
    qtbot.addWidget(banner)

    banner.show_warning("⚠️", "Kamera bulunamadı", duration=100)

    assert banner.isVisible() is True
    assert banner.icon_lbl.text() == "⚠️"
    assert "Kamera" in banner.msg_lbl.text()


def test_focus_page_load_courses_adds_active_courses(qtbot, message_calls):
    page = FocusPage("user_123", FakeDBManager(), whitelist_page=FakeWhitelistPage())
    qtbot.addWidget(page)

    page._load_courses()

    assert page.course_combo.count() >= 1
    assert page.course_combo.itemData(0) == "bm314"


def test_focus_page_start_and_end_session_updates_ui_and_services(qtbot, monkeypatch, message_calls):
    db = FakeDBManager()
    whitelist = FakeWhitelistPage()
    monkeypatch.setattr(fp, "HeadTracker", FakeHeadTracker)

    page = FocusPage("user_123", db, whitelist_page=whitelist)
    qtbot.addWidget(page)
    page._load_courses()

    page._start_session()

    assert page._session_active is True
    assert whitelist.started is True
    assert whitelist.focus_session_id == "focus_123"
    assert page.course_combo.isEnabled() is False
    assert "Bitir" in page.start_btn.text()
    assert isinstance(page.tracker, FakeHeadTracker)
    assert page.tracker.started is True

    page._elapsed = 5
    page._end_session()

    assert page._session_active is False
    assert whitelist.stopped is True
    assert page.course_combo.isEnabled() is True
    assert "Başlat" in page.start_btn.text()
    assert db.focus_sessions[0]["actual_focus_time"] == 5


def test_focus_page_focus_changed_updates_state_and_violation_count(qtbot, monkeypatch, message_calls):
    page = FocusPage("user_123", FakeDBManager(), whitelist_page=FakeWhitelistPage())
    qtbot.addWidget(page)

    shown = []
    hidden = []
    monkeypatch.setattr(page, "_show_distraction_popup", lambda: shown.append(True))
    monkeypatch.setattr(page, "_hide_distraction_popup", lambda: hidden.append(True))

    page._on_focus_changed(False)
    assert page.is_user_focused is False
    assert page.current_violations == 1
    assert shown == [True]

    page._on_focus_changed(True)
    assert page.is_user_focused is True
    assert hidden == [True]


def test_focus_page_tick_updates_timer_and_focus_ring(qtbot, message_calls):
    page = FocusPage("user_123", FakeDBManager(), whitelist_page=FakeWhitelistPage())
    qtbot.addWidget(page)

    page._session_active = True
    page.time_left = 61
    page.tracker = FakeHeadTracker()
    page.tracker.total_session_time = 10
    page.tracker.total_focus_time = 5

    page._tick()

    assert page._elapsed == 1
    assert page.time_left == 60
    assert page.timer_lbl.text() == "01:00"
    assert page.focus_ring.value == 50


def test_focus_cleanup_stops_timer_popup_and_tracker(qtbot, monkeypatch, message_calls):
    page = FocusPage("user_123", FakeDBManager(), whitelist_page=FakeWhitelistPage())
    qtbot.addWidget(page)
    page.tracker = FakeHeadTracker()

    hidden = []
    monkeypatch.setattr(page, "_hide_distraction_popup", lambda: hidden.append(True))

    page.cleanup()

    assert hidden == [True]
    assert page.tracker.stopped is True


# =============================================================================
# MainWindow UI tests
# =============================================================================

def test_main_window_navigation_sets_stack_and_active_button(qtbot, monkeypatch, message_calls):
    # Avoid camera/AI and profile loading side effects during MainWindow creation.
    monkeypatch.setattr(focus_module.FocusPage, "_load_recommended_plan", lambda self: None)
    monkeypatch.setattr(profile_module.ProfilePage, "_load_profile", lambda self: None)
    monkeypatch.setattr(dashboard_module.DashboardPage, "refresh", lambda self: None)

    win = MainWindow("user_123", FakeDBManager())
    qtbot.addWidget(win)

    assert win.stack.count() == 8
    assert set(win._page_map.keys()) == {
        "dashboard", "schedule", "exams", "suggested_plan",
        "courses", "focus", "whitelist", "profile",
    }

    win._navigate("courses")

    assert win.stack.currentIndex() == win._page_map["courses"][0]
    assert win._nav_buttons["courses"].property("active") == "true"
    assert win._nav_buttons["dashboard"].property("active") == "false"


def test_main_window_unknown_navigation_is_ignored(qtbot, monkeypatch, message_calls):
    monkeypatch.setattr(focus_module.FocusPage, "_load_recommended_plan", lambda self: None)
    monkeypatch.setattr(profile_module.ProfilePage, "_load_profile", lambda self: None)
    monkeypatch.setattr(dashboard_module.DashboardPage, "refresh", lambda self: None)

    win = MainWindow("user_123", FakeDBManager())
    qtbot.addWidget(win)

    current = win.stack.currentIndex()
    win._navigate("unknown")

    assert win.stack.currentIndex() == current


def test_main_window_logout_closes_when_confirmed(qtbot, monkeypatch, message_calls):
    monkeypatch.setattr(focus_module.FocusPage, "_load_recommended_plan", lambda self: None)
    monkeypatch.setattr(profile_module.ProfilePage, "_load_profile", lambda self: None)
    monkeypatch.setattr(dashboard_module.DashboardPage, "refresh", lambda self: None)

    win = MainWindow("user_123", FakeDBManager())
    qtbot.addWidget(win)
    win.show()

    win._logout()

    assert win.isVisible() is False
