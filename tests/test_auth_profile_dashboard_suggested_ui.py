import pytest

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox, QPushButton, QLineEdit, QInputDialog

from ui.login_window import LoginWindow
from ui.profile_page import ProfilePage
from ui.dashboard_page import DashboardPage
from ui.suggested_plan_page import SuggestedPlanPage, DayColumn, SessionCard


class FakeDBManager:
    def __init__(self):
        self.login_calls = []
        self.register_calls = []
        self.profile_updates = []
        self.login_success = True
        self.register_success = True
        self.profile_success = True

    def login_user(self, email, password):
        self.login_calls.append((email, password))
        if self.login_success:
            return True, "user_123"
        return False, "E-posta veya şifre hatalı."

    def register_user(self, email, password):
        self.register_calls.append((email, password))
        if self.register_success:
            return True, "Kayıt başarılı."
        return False, "Bu e-posta zaten kayıtlı."

    def get_user_profile(self, user_id):
        if not self.profile_success:
            return False, "Profil okunamadı."
        return True, {
            "name": "Kerem",
            "surname": "Kapısız",
            "school": "Gazi Üniversitesi",
            "email": "kerem@example.com",
            "password": "oldpass",
        }

    def update_user_profile(self, user_id, name, surname, school, new_password):
        self.profile_updates.append({
            "user_id": user_id,
            "name": name,
            "surname": surname,
            "school": school,
            "new_password": new_password,
        })
        return True, "Profil güncellendi."

    def get_dashboard_stats(self, user_id):
        return True, {
            "user_name": "Kerem",
            "avg_focus_score": 87,
            "course_count": 5,
            "total_study_time": 140,
            "violation_count": 3,
        }

    def get_weekly_analysis(self, user_id):
        return True, {
            "Pzt": 80,
            "Sal": 60,
            "Çar": 40,
            "Per": 20,
            "Cum": 100,
            "Cmt": 0,
            "Paz": 50,
        }

    def get_course_risk_analysis(self, user_id):
        return True, [
            {
                "course_name": "Microprocessors",
                "target": 85,
                "status": "iyi",
                "color": "#00e5a0",
            }
        ]


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

    monkeypatch.setattr(QMessageBox, "warning", fake_warning)
    monkeypatch.setattr(QMessageBox, "information", fake_information)
    monkeypatch.setattr(QMessageBox, "critical", fake_critical)
    return calls


def find_button(widget, text):
    for button in widget.findChildren(QPushButton):
        if text in button.text():
            return button
    available = [b.text() for b in widget.findChildren(QPushButton)]
    raise AssertionError(f"Button not found: {text}. Available: {available}")


# =============================================================================
# LoginWindow UI tests
# =============================================================================

def test_login_window_initial_state(qtbot, message_calls):
    win = LoginWindow(FakeDBManager())
    qtbot.addWidget(win)

    assert win.windowTitle() == "FocuSync – Giriş"
    assert win.stack.currentIndex() == 0
    assert win.login_email.placeholderText() == "ornek@email.com"
    assert win.login_password.echoMode() == QLineEdit.EchoMode.Password


def test_login_missing_fields_shows_inline_error(qtbot, message_calls):
    db = FakeDBManager()
    win = LoginWindow(db)
    qtbot.addWidget(win)

    win._do_login()

    assert "zorunludur" in win.login_error.text()
    assert db.login_calls == []


def test_login_success_emits_user_id(qtbot, message_calls):
    db = FakeDBManager()
    win = LoginWindow(db)
    qtbot.addWidget(win)

    emitted = []
    win.login_success.connect(lambda user_id: emitted.append(user_id))

    win.login_email.setText("kerem@example.com")
    win.login_password.setText("secret")
    win._do_login()

    assert db.login_calls == [("kerem@example.com", "secret")]
    assert emitted == ["user_123"]
    assert win.login_error.text() == ""


def test_login_failure_clears_password_and_sets_error(qtbot, message_calls):
    db = FakeDBManager()
    db.login_success = False
    win = LoginWindow(db)
    qtbot.addWidget(win)

    win.login_email.setText("kerem@example.com")
    win.login_password.setText("wrong")
    win._do_login()

    assert "hatalı" in win.login_error.text().lower()
    assert win.login_password.text() == ""


def test_switch_to_register_and_back(qtbot, message_calls):
    win = LoginWindow(FakeDBManager())
    qtbot.addWidget(win)

    login_page = win.stack.widget(0)
    register_page = win.stack.widget(1)

    qtbot.mouseClick(find_button(login_page, "Kayıt Ol"), Qt.MouseButton.LeftButton)
    assert win.stack.currentIndex() == 1

    qtbot.mouseClick(find_button(register_page, "Giriş Yap"), Qt.MouseButton.LeftButton)
    assert win.stack.currentIndex() == 0


def test_register_password_mismatch_stays_on_register_page(qtbot, message_calls):
    db = FakeDBManager()
    win = LoginWindow(db)
    qtbot.addWidget(win)
    win.stack.setCurrentIndex(1)

    win.reg_email.setText("kerem@example.com")
    win.reg_password.setText("abcdef")
    win.reg_password2.setText("abcdeg")
    win._do_register()

    assert "eşleşmiyor" in win.reg_error.text()
    assert db.register_calls == []
    assert win.stack.currentIndex() == 1


def test_register_success_returns_to_login_page(qtbot, message_calls):
    db = FakeDBManager()
    win = LoginWindow(db)
    qtbot.addWidget(win)
    win.stack.setCurrentIndex(1)

    win.reg_email.setText("kerem@example.com")
    win.reg_password.setText("abcdef")
    win.reg_password2.setText("abcdef")
    win._do_register()

    assert db.register_calls == [("kerem@example.com", "abcdef")]
    assert win.stack.currentIndex() == 0
    assert win.login_email.text() == "kerem@example.com"
    assert any(call[0] == "information" for call in message_calls)


# =============================================================================
# ProfilePage UI tests
# =============================================================================

def test_profile_loads_user_data(qtbot, message_calls):
    page = ProfilePage("user_123", FakeDBManager())
    qtbot.addWidget(page)

    assert page.name_input.text() == "Kerem"
    assert page.surname_input.text() == "Kapısız"
    assert page.school_input.text() == "Gazi Üniversitesi"
    assert page.email_input.text() == "kerem@example.com"
    assert page.email_input.isReadOnly() is True
    assert page._current_password == "oldpass"


def test_profile_save_without_password_updates_profile(qtbot, message_calls):
    db = FakeDBManager()
    page = ProfilePage("user_123", db)
    qtbot.addWidget(page)

    page.name_input.setText("Kerem")
    page.surname_input.setText("K")
    page.school_input.setText("Gazi")
    page._save_profile()

    assert len(db.profile_updates) == 1
    assert db.profile_updates[0]["new_password"] is None
    assert any(call[0] == "information" for call in message_calls)


def test_profile_wrong_current_password_blocks_update(qtbot, message_calls):
    db = FakeDBManager()
    page = ProfilePage("user_123", db)
    qtbot.addWidget(page)

    page.current_pass.setText("wrong")
    page.new_pass.setText("newpass")
    page.new_pass_confirm.setText("newpass")
    page._save_profile()

    assert db.profile_updates == []
    assert any("yanlış" in call[2].lower() for call in message_calls)


def test_profile_password_change_updates_cached_password_and_clears_fields(qtbot, message_calls):
    db = FakeDBManager()
    page = ProfilePage("user_123", db)
    qtbot.addWidget(page)

    page.current_pass.setText("oldpass")
    page.new_pass.setText("newpass")
    page.new_pass_confirm.setText("newpass")
    page._save_profile()

    assert db.profile_updates[0]["new_password"] == "newpass"
    assert page._current_password == "newpass"
    assert page.current_pass.text() == ""
    assert page.new_pass.text() == ""
    assert page.new_pass_confirm.text() == ""


# =============================================================================
# DashboardPage UI tests
# =============================================================================

def test_dashboard_refresh_updates_stat_cards_and_greeting(qtbot, message_calls):
    page = DashboardPage("user_123", FakeDBManager())
    qtbot.addWidget(page)

    assert page.greeting_lbl.text() == "MERHABA, KEREM!"
    assert page.card_score.val_lbl.text() == "%87"
    assert page.card_courses.val_lbl.text() == "5"
    assert page.card_time.val_lbl.text() == "140"
    assert page.card_viol.val_lbl.text() == "3"


def test_dashboard_weekly_chart_updates_bar_heights(qtbot, message_calls):
    page = DashboardPage("user_123", FakeDBManager())
    qtbot.addWidget(page)

    page.update_weekly_chart({"Pzt": 100, "Sal": 50, "Çar": 0})

    assert page.daily_bars["Pzt"].height() == 120
    assert page.daily_bars["Sal"].height() == 60
    assert page.daily_bars["Çar"].height() == 0


def test_dashboard_grade_calculator_cancel_does_nothing(qtbot, monkeypatch, message_calls):
    page = DashboardPage("user_123", FakeDBManager())
    qtbot.addWidget(page)

    monkeypatch.setattr(QInputDialog, "getDouble", lambda *args, **kwargs: (60, False))
    page.open_grade_calculator()

    assert not any(call[1] == "Detaylı Not Analizi" for call in message_calls)


# =============================================================================
# SuggestedPlanPage UI tests
# =============================================================================

def test_suggested_plan_initializes_week_columns(qtbot, message_calls):
    page = SuggestedPlanPage("user_123", FakeDBManager())
    qtbot.addWidget(page)

    assert len(page.day_columns) == 7
    assert all(isinstance(col, DayColumn) for col in page.day_columns)
    assert page.refresh_btn.isEnabled() is True


def test_suggested_plan_refresh_button_state(qtbot, message_calls):
    page = SuggestedPlanPage("user_123", FakeDBManager())
    qtbot.addWidget(page)

    page._on_refresh()
    assert page.refresh_btn.isEnabled() is False
    assert "Oluşturuluyor" in page.refresh_btn.text()

    page._finish_refresh()
    assert page.refresh_btn.isEnabled() is True
    assert "Yeniden Oluştur" in page.refresh_btn.text()


def test_session_card_scale_updates_size(qtbot, message_calls):
    session = {
        "course": "BM314",
        "name": "Yazılım Mühendisliği",
        "start": "09:00",
        "end": "11:00",
        "type": "Yeni Konu",
        "priority": "high",
    }
    card = SessionCard(session)
    qtbot.addWidget(card)

    card.apply_scale(0.75)

    assert card.minimumHeight() > 0
    assert card.code_label.text() == "BM314"
    assert "09:00" in card.time_label.text()
