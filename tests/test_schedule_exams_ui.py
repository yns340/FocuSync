import pytest

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox, QFileDialog, QCheckBox

from ui.schedule_page import SchedulePage, CourseEditWidget
from ui.exams_page import ExamsPage, ExamTypeWidget, ExamEditWidget


class FakeDBManager:
    def __init__(self):
        self.saved_schedules = []
        self.deleted_schedule = False
        self.saved_exams = []
        self.deleted_exams = False
        self.courses = [
            {"course_id": "bm314", "course_name": "Software Engineering", "is_active": True},
            {"course_id": "ceng318", "course_name": "Microprocessors", "is_active": True},
            {"course_id": "archived", "course_name": "Archived", "is_active": False},
        ]

    def get_schedule(self, user_id):
        return False, None

    def save_full_schedule(self, user_id, schedule_name, schedule_dict, course_hours_dict):
        self.saved_schedules.append({
            "user_id": user_id,
            "schedule_name": schedule_name,
            "schedule_dict": schedule_dict,
            "course_hours_dict": course_hours_dict,
        })
        return True, "Schedule saved."

    def delete_schedule(self, user_id):
        self.deleted_schedule = True
        return True, "Schedule deleted."

    def get_courses(self, user_id):
        return True, list(self.courses)

    def get_exam_schedule(self, user_id):
        return False, None

    def save_exam_schedule(self, user_id, name, exams_list):
        self.saved_exams.append({
            "user_id": user_id,
            "name": name,
            "exams_list": exams_list,
        })
        return True, "Exams saved."

    def delete_exam_schedule(self, user_id):
        self.deleted_exams = True
        return True, "Exams deleted."


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


@pytest.fixture
def schedule_page(qtbot, monkeypatch, message_calls):
    db = FakeDBManager()
    page = SchedulePage("user_123", db)
    monkeypatch.setattr(page, "_check_internet", lambda: True)
    qtbot.addWidget(page)
    return page


@pytest.fixture
def exams_page(qtbot, monkeypatch, message_calls):
    db = FakeDBManager()
    page = ExamsPage("user_123", db)
    monkeypatch.setattr(page, "_check_internet", lambda: True)
    qtbot.addWidget(page)
    return page


# =============================================================================
# SchedulePage UI tests
# =============================================================================

def test_schedule_initial_ui_state(schedule_page):
    assert schedule_page.stacked_widget.count() == 2
    assert schedule_page.view_table.columnCount() == 5
    assert schedule_page.table.columnCount() == 5
    assert schedule_page.editor_wrapper.isVisible() is False


def test_schedule_recreate_and_back_buttons_change_stack(schedule_page, qtbot):
    qtbot.mouseClick(schedule_page.btn_recreate, Qt.MouseButton.LeftButton)
    assert schedule_page.stacked_widget.currentIndex() == 1

    qtbot.mouseClick(schedule_page.btn_go_back, Qt.MouseButton.LeftButton)
    assert schedule_page.stacked_widget.currentIndex() == 0


def test_schedule_add_and_delete_table_row(schedule_page):
    schedule_page._add_table_row(
        day="Salı",
        start="09:00",
        end="10:30",
        course="BM314 - Software Engineering",
        ctype="Teorik",
    )

    assert schedule_page.table.rowCount() == 1
    assert schedule_page.table.cellWidget(0, 0).currentText() == "Salı"
    assert isinstance(schedule_page.table.cellWidget(0, 3), CourseEditWidget)
    assert schedule_page.table.cellWidget(0, 3).code_edit.text() == "BM314"

    schedule_page.table.selectRow(0)
    schedule_page._delete_selected_row()

    assert schedule_page.table.rowCount() == 0


def test_schedule_sync_course_code_for_same_group(schedule_page):
    schedule_page._add_table_row(course="BM314 - Software Engineering")
    schedule_page._add_table_row(course="BM314 - Software Engineering")

    first = schedule_page.table.cellWidget(0, 3)
    second = schedule_page.table.cellWidget(1, 3)

    first.code_edit.setText("BM999")
    schedule_page._sync_course_realtime(first, is_code_change=True)

    assert second.code_edit.text() == "BM999"


def test_schedule_import_finished_success_populates_rows(schedule_page):
    result_data = {
        "Pazartesi": [
            {
                "start": "09:00",
                "end": "10:00",
                "course": "BM314 - Software Engineering",
                "ctype": "Teorik",
            }
        ],
        "Salı": [],
    }

    schedule_page._on_import_finished(True, "schedule", result_data)

    assert schedule_page.table.rowCount() == 1
    assert schedule_page.editor_wrapper.isHidden() is False
    assert "Başarıyla 1 Ders Okundu" in schedule_page.upload_btn.text()

def test_schedule_import_finished_wrong_document_type_shows_warning(schedule_page, message_calls):
    schedule_page._on_import_finished(True, "exam", [])

    assert any(call[0] == "warning" and "Yanlış Menü" in call[1] for call in message_calls)
    assert schedule_page.table.rowCount() == 0


def test_schedule_save_to_db_creates_schedule_payload(schedule_page, message_calls):
    schedule_page._add_table_row(
        day="Pazartesi",
        start="09:00",
        end="10:40",
        course="BM314 - Software Engineering",
        ctype="Teorik",
    )
    schedule_page.schedule_name_input.setText("2026 Bahar")

    schedule_page._save_to_db()

    assert len(schedule_page.db_manager.saved_schedules) == 1
    saved = schedule_page.db_manager.saved_schedules[0]
    assert saved["schedule_name"] == "2026 Bahar"
    assert saved["schedule_dict"]["Pazartesi"][0]["course_id"] == "bm314"
    assert saved["course_hours_dict"]["bm314"]["hours"] >= 1
    assert any(call[0] == "information" for call in message_calls)


def test_schedule_save_empty_table_shows_warning(schedule_page, message_calls):
    schedule_page._save_to_db()

    assert schedule_page.db_manager.saved_schedules == []
    assert any(call[0] == "warning" and "Boş Tablo" in call[1] for call in message_calls)


def test_schedule_delete_action_calls_db(schedule_page, message_calls):
    schedule_page._delete_schedule_action()

    assert schedule_page.db_manager.deleted_schedule is True
    assert any(call[0] == "information" for call in message_calls)


# =============================================================================
# ExamsPage UI tests
# =============================================================================

def test_exam_type_widget_basic_behavior(qtbot):
    widget = ExamTypeWidget("Vize 2")
    qtbot.addWidget(widget)

    assert widget.get_full_type() == "Vize 2"

    widget.set_full_type("Final")
    assert widget.get_full_type() == "Final"
    assert widget.num_sb.isVisible() is False

    widget.set_full_type("Quiz 3")
    assert widget.get_full_type() == "Quiz 3"


def test_exams_initial_ui_state(exams_page):
    assert exams_page.stacked_widget.count() == 2
    assert exams_page.view_table.columnCount() == 6
    assert exams_page.table.columnCount() == 7
    assert "Sistem" in exams_page.nearest_exam_lbl.text()


def test_exams_recreate_and_back_buttons_change_stack(exams_page, qtbot):
    qtbot.mouseClick(exams_page.btn_recreate, Qt.MouseButton.LeftButton)
    assert exams_page.stacked_widget.currentIndex() == 1

    qtbot.mouseClick(exams_page.btn_go_back, Qt.MouseButton.LeftButton)
    assert exams_page.stacked_widget.currentIndex() == 0


def test_exams_add_row_creates_expected_widgets_and_grade_cap(exams_page):
    exams_page._add_table_row(
        date="10.05.2026",
        time="13:30",
        code="BM314",
        name="Software Engineering",
        etype="Vize 1",
        room="M101",
        grade="90",
        is_selected=True,
    )

    assert exams_page.table.rowCount() == 1
    assert exams_page.table.cellWidget(0, 0).findChild(QCheckBox).isChecked() is True
    assert isinstance(exams_page.table.cellWidget(0, 3), ExamEditWidget)
    assert exams_page.table.cellWidget(0, 4).get_full_type() == "Vize 1"

    grade_edit = exams_page.table.cellWidget(0, 6)
    grade_edit.setText("150")
    assert grade_edit.text() == "100"


def test_exams_import_finished_success_adds_rows_and_selects_known_courses(exams_page):
    result_data = [
        {
            "course_id": "bm314",
            "course_name": "Software Engineering",
            "exam_date": "10.05.2026",
            "exam_time": "13:30",
            "exam_type": "Vize",
            "notes": "M101",
        },
        {
            "course_id": "unknown",
            "course_name": "Unknown Course",
            "exam_date": "11.05.2026",
            "exam_time": "10:00",
            "exam_type": "Quiz",
            "notes": "M102",
        },
    ]

    exams_page._on_import_finished(True, "exam", result_data)

    assert exams_page.table.rowCount() == 2
    assert exams_page.table.cellWidget(0, 0).findChild(QCheckBox).isChecked() is True
    assert exams_page.table.cellWidget(1, 0).findChild(QCheckBox).isChecked() is False
    assert "Başarıyla 2 Not" in exams_page.upload_btn.text()


def test_exams_import_finished_wrong_document_type_shows_warning(exams_page, message_calls):
    exams_page._on_import_finished(True, "schedule", [])

    assert any(call[0] == "warning" and "Yanlış Menü" in call[1] for call in message_calls)
    assert exams_page.table.rowCount() == 0


def test_exams_save_to_db_saves_selected_valid_exam(exams_page, message_calls):
    exams_page._add_table_row(
        date="10.05.2026",
        time="13:30",
        code="bm314",
        name="Software Engineering",
        etype="Vize 1",
        room="M101",
        grade="85",
        is_selected=True,
    )
    exams_page.exam_name_input.setText("2026 Vize Takvimi")

    exams_page._save_to_db()

    assert len(exams_page.db_manager.saved_exams) == 1
    saved = exams_page.db_manager.saved_exams[0]
    assert saved["name"] == "2026 Vize Takvimi"
    assert saved["exams_list"][0]["course_id"] == "bm314"
    assert saved["exams_list"][0]["exam_grade"] == "85"
    assert any(call[0] == "information" for call in message_calls)


def test_exams_save_unknown_course_blocks_save(exams_page, message_calls):
    exams_page._add_table_row(code="unknown", name="Unknown", is_selected=True)

    exams_page._save_to_db()

    assert exams_page.db_manager.saved_exams == []
    assert any(call[0] == "critical" and "Ders Bulunamadı" in call[1] for call in message_calls)


def test_exams_delete_selected_row(exams_page):
    exams_page._add_table_row(code="bm314")
    exams_page.table.selectRow(0)
    exams_page._delete_selected_row()

    assert exams_page.table.rowCount() == 0


def test_exams_delete_action_calls_db(exams_page, message_calls):
    exams_page._delete_exams_action()

    assert exams_page.db_manager.deleted_exams is True
    assert exams_page.table.rowCount() == 0
    assert any(call[0] == "information" for call in message_calls)
