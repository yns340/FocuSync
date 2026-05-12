import os
import pytest

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMessageBox,
    QFileDialog,
    QPushButton,
)

import ui.whitelist_page as wp
from ui.whitelist_page import (
    WhitelistPage,
    InstalledAppsDialog,
    ViolationAlertDialog,
)


# =============================================================================
# Test helpers
# =============================================================================

class FakeSignal:
    def __init__(self):
        self._callbacks = []

    def connect(self, callback):
        self._callbacks.append(callback)

    def emit(self, *args, **kwargs):
        for callback in list(self._callbacks):
            callback(*args, **kwargs)


class FakeMonitorWorker:
    instances = []

    def __init__(self, get_whitelist_fn, interval_ms=1000, parent=None):
        self.get_whitelist_fn = get_whitelist_fn
        self.interval_ms = interval_ms
        self.parent = parent

        self.violation_found = FakeSignal()
        self.no_violation = FakeSignal()

        self.started = False
        self.stopped = False
        self._running = False

        FakeMonitorWorker.instances.append(self)

    def start(self):
        self.started = True
        self._running = True

    def stop(self):
        self.stopped = True
        self._running = False

    def isRunning(self):
        return self._running


class FakeDBManager:
    def __init__(self):
        self.saved_calls = []

    def save_whitelist_session(self, **kwargs):
        self.saved_calls.append(kwargs)
        return True, "Mock whitelist session saved."


def find_button(widget, text):
    """
    Finds a QPushButton by visible text.
    Useful because some buttons in WhitelistPage are local variables,
    not self attributes.
    """
    for button in widget.findChildren(QPushButton):
        if text in button.text():
            return button

    available = [button.text() for button in widget.findChildren(QPushButton)]
    raise AssertionError(f"Button not found: {text}. Available buttons: {available}")


@pytest.fixture
def message_calls(monkeypatch):
    """
    QMessageBox popups can block tests.
    This fixture captures warning/information calls instead of showing real popups.
    """
    calls = []

    def fake_warning(*args, **kwargs):
        title = args[1] if len(args) > 1 else ""
        text = args[2] if len(args) > 2 else ""
        calls.append(("warning", title, text))
        return QMessageBox.StandardButton.Ok

    def fake_information(*args, **kwargs):
        title = args[1] if len(args) > 1 else ""
        text = args[2] if len(args) > 2 else ""
        calls.append(("information", title, text))
        return QMessageBox.StandardButton.Ok

    monkeypatch.setattr(QMessageBox, "warning", fake_warning)
    monkeypatch.setattr(QMessageBox, "information", fake_information)

    return calls


@pytest.fixture
def page(qtbot, monkeypatch, message_calls):
    """
    Creates WhitelistPage in a safe test mode.
    WIN32_AVAILABLE is forced to True for UI tests unless a specific test overrides it.
    """
    monkeypatch.setattr(wp, "WIN32_AVAILABLE", True)

    widget = WhitelistPage("test_user", None)
    qtbot.addWidget(widget)
    widget.show()

    return widget


# =============================================================================
# Initial UI state
# =============================================================================

def test_initial_ui_state(page):
    assert page._list_widget.count() == 0

    assert page._input.placeholderText() == "Manuel exe adı gir (örn: chrome.exe)"

    assert page._allow_last_btn.isEnabled() is False
    assert page._allow_last_shortcut.isEnabled() is False

    assert page._ihlal_lbl.text() == "İhlal: —"
    assert page._detay_lbl.text() == "Tespit edilen uygulama: —"
    assert page._aktif_lbl.text() == "İzleme: Kapalı"


def test_core_widgets_have_styles(page):
    assert "#111318" in page._list_widget.styleSheet()
    assert "#6b7280" in page._aktif_lbl.styleSheet()


# =============================================================================
# Manual add UI flow
# =============================================================================

def test_manual_exe_add_with_button_updates_list_widget(page, qtbot):
    page._input.setText("chrome.exe")

    add_button = find_button(page, "Elle Ekle")
    qtbot.mouseClick(add_button, Qt.MouseButton.LeftButton)

    assert page._list_widget.count() == 1
    assert page._list_widget.item(0).text() == "chrome.exe"
    assert page._input.text() == ""


def test_manual_exe_add_with_enter_key_updates_list_widget(page, qtbot):
    page._input.setText("firefox.exe")
    page._input.setFocus()

    qtbot.keyClick(page._input, Qt.Key.Key_Return)

    assert page._list_widget.count() == 1
    assert page._list_widget.item(0).text() == "firefox.exe"
    assert page._input.text() == ""


def test_manual_add_normalizes_exe_name(page, qtbot):
    page._input.setText("  DISCORD.EXE  ")

    add_button = find_button(page, "Elle Ekle")
    qtbot.mouseClick(add_button, Qt.MouseButton.LeftButton)

    assert page._list_widget.count() == 1
    assert page._list_widget.item(0).text() == "discord.exe"


def test_invalid_exe_does_not_update_list_widget(page, qtbot, message_calls):
    page._input.setText("chrome")

    add_button = find_button(page, "Elle Ekle")
    qtbot.mouseClick(add_button, Qt.MouseButton.LeftButton)

    assert page._list_widget.count() == 0
    assert any(call[0] == "warning" for call in message_calls)
    assert any(".exe" in call[2] for call in message_calls)


def test_empty_manual_add_does_not_update_list_widget(page, qtbot, message_calls):
    page._input.setText("")

    add_button = find_button(page, "Elle Ekle")
    qtbot.mouseClick(add_button, Qt.MouseButton.LeftButton)

    assert page._list_widget.count() == 0
    assert any(call[0] == "warning" for call in message_calls)


def test_duplicate_exe_does_not_create_second_item(page, qtbot, message_calls):
    add_button = find_button(page, "Elle Ekle")

    page._input.setText("spotify.exe")
    qtbot.mouseClick(add_button, Qt.MouseButton.LeftButton)

    page._input.setText("spotify.exe")
    qtbot.mouseClick(add_button, Qt.MouseButton.LeftButton)

    assert page._list_widget.count() == 1
    assert page._list_widget.item(0).text() == "spotify.exe"
    assert any("zaten whitelist" in call[2] for call in message_calls)


def test_list_is_sorted_after_multiple_adds(page, qtbot):
    add_button = find_button(page, "Elle Ekle")

    page._input.setText("spotify.exe")
    qtbot.mouseClick(add_button, Qt.MouseButton.LeftButton)

    page._input.setText("chrome.exe")
    qtbot.mouseClick(add_button, Qt.MouseButton.LeftButton)

    page._input.setText("discord.exe")
    qtbot.mouseClick(add_button, Qt.MouseButton.LeftButton)

    items = [
        page._list_widget.item(i).text()
        for i in range(page._list_widget.count())
    ]

    assert items == ["chrome.exe", "discord.exe", "spotify.exe"]


# =============================================================================
# Remove UI flow
# =============================================================================

def test_remove_selected_exe_from_list_widget(page, qtbot):
    page._input.setText("spotify.exe")
    qtbot.mouseClick(find_button(page, "Elle Ekle"), Qt.MouseButton.LeftButton)

    assert page._list_widget.count() == 1

    page._list_widget.setCurrentRow(0)

    remove_button = find_button(page, "Seçili Girişi Kaldır")
    qtbot.mouseClick(remove_button, Qt.MouseButton.LeftButton)

    assert page._list_widget.count() == 0
    assert "spotify.exe" not in page.logic.get_whitelist()


def test_remove_without_selection_shows_warning(page, qtbot, message_calls):
    remove_button = find_button(page, "Seçili Girişi Kaldır")
    qtbot.mouseClick(remove_button, Qt.MouseButton.LeftButton)

    assert any(call[0] == "warning" for call in message_calls)
    assert any("Lütfen listeden bir giriş seç" in call[2] for call in message_calls)


# =============================================================================
# File picker UI flow
# =============================================================================

def test_browse_exe_adds_selected_file_to_whitelist(page, qtbot, monkeypatch, tmp_path):
    selected_exe = tmp_path / "Discord.exe"

    monkeypatch.setattr(
        QFileDialog,
        "getOpenFileName",
        lambda *args, **kwargs: (str(selected_exe), "Executable Files (*.exe)")
    )

    qtbot.mouseClick(page._browse_exe_btn, Qt.MouseButton.LeftButton)

    assert page._list_widget.count() == 1
    assert page._list_widget.item(0).text() == "discord.exe"
    assert "discord.exe" in page.logic.get_whitelist()


def test_browse_exe_cancel_does_nothing(page, qtbot, monkeypatch):
    monkeypatch.setattr(
        QFileDialog,
        "getOpenFileName",
        lambda *args, **kwargs: ("", "")
    )

    qtbot.mouseClick(page._browse_exe_btn, Qt.MouseButton.LeftButton)

    assert page._list_widget.count() == 0


def test_browse_invalid_file_shows_warning(page, qtbot, monkeypatch, tmp_path, message_calls):
    selected_file = tmp_path / "readme.txt"

    monkeypatch.setattr(
        QFileDialog,
        "getOpenFileName",
        lambda *args, **kwargs: (str(selected_file), "All Files (*)")
    )

    qtbot.mouseClick(page._browse_exe_btn, Qt.MouseButton.LeftButton)

    assert page._list_widget.count() == 0
    assert any(call[0] == "warning" for call in message_calls)


# =============================================================================
# Installed apps button flow
# =============================================================================

def test_installed_apps_button_warns_outside_windows(page, qtbot, monkeypatch, message_calls):
    monkeypatch.setattr(wp.os, "name", "posix", raising=False)

    qtbot.mouseClick(page._installed_apps_btn, Qt.MouseButton.LeftButton)

    assert any(call[0] == "warning" for call in message_calls)
    assert any("yalnızca Windows" in call[2] for call in message_calls)


def test_installed_apps_button_shows_info_when_no_apps_found(
    page,
    qtbot,
    monkeypatch,
    message_calls,
):
    monkeypatch.setattr(wp.os, "name", "nt", raising=False)
    monkeypatch.setattr(wp, "iter_installed_apps", lambda: [])

    qtbot.mouseClick(page._installed_apps_btn, Qt.MouseButton.LeftButton)

    assert page._list_widget.count() == 0
    assert any(call[0] == "information" for call in message_calls)
    assert any("Kurulu uygulama listesi alınamadı" in call[2] for call in message_calls)


def test_installed_apps_button_adds_selected_app(page, qtbot, monkeypatch):
    apps = [
        {
            "display_name": "Spotify",
            "exe_name": "spotify.exe",
            "exe_path": r"C:\Apps\Spotify\spotify.exe",
            "publisher": "Spotify AB",
        }
    ]

    class FakeInstalledAppsDialog:
        def __init__(self, given_apps, parent=None):
            self.given_apps = given_apps
            self.parent = parent

        def exec(self):
            return True

        def selected_app(self):
            return apps[0]

    monkeypatch.setattr(wp.os, "name", "nt", raising=False)
    monkeypatch.setattr(wp, "iter_installed_apps", lambda: apps)
    monkeypatch.setattr(wp, "InstalledAppsDialog", FakeInstalledAppsDialog)

    qtbot.mouseClick(page._installed_apps_btn, Qt.MouseButton.LeftButton)

    assert page._list_widget.count() == 1
    assert page._list_widget.item(0).text() == "spotify.exe"
    assert "spotify.exe" in page.logic.get_whitelist()


def test_installed_apps_button_cancel_does_not_add_app(page, qtbot, monkeypatch):
    apps = [
        {
            "display_name": "Spotify",
            "exe_name": "spotify.exe",
            "exe_path": r"C:\Apps\Spotify\spotify.exe",
            "publisher": "Spotify AB",
        }
    ]

    class FakeInstalledAppsDialog:
        def __init__(self, given_apps, parent=None):
            pass

        def exec(self):
            return False

        def selected_app(self):
            return apps[0]

    monkeypatch.setattr(wp.os, "name", "nt", raising=False)
    monkeypatch.setattr(wp, "iter_installed_apps", lambda: apps)
    monkeypatch.setattr(wp, "InstalledAppsDialog", FakeInstalledAppsDialog)

    qtbot.mouseClick(page._installed_apps_btn, Qt.MouseButton.LeftButton)

    assert page._list_widget.count() == 0
    assert "spotify.exe" not in page.logic.get_whitelist()


def test_installed_apps_button_selected_app_none_does_not_add(page, qtbot, monkeypatch):
    apps = [
        {
            "display_name": "Spotify",
            "exe_name": "spotify.exe",
            "exe_path": r"C:\Apps\Spotify\spotify.exe",
            "publisher": "Spotify AB",
        }
    ]

    class FakeInstalledAppsDialog:
        def __init__(self, given_apps, parent=None):
            pass

        def exec(self):
            return True

        def selected_app(self):
            return None

    monkeypatch.setattr(wp.os, "name", "nt", raising=False)
    monkeypatch.setattr(wp, "iter_installed_apps", lambda: apps)
    monkeypatch.setattr(wp, "InstalledAppsDialog", FakeInstalledAppsDialog)

    qtbot.mouseClick(page._installed_apps_btn, Qt.MouseButton.LeftButton)

    assert page._list_widget.count() == 0


# =============================================================================
# InstalledAppsDialog direct UI tests
# =============================================================================

def test_installed_apps_dialog_filters_apps(qtbot, message_calls):
    apps = [
        {
            "display_name": "Cool Browser",
            "exe_name": "coolbrowser.exe",
            "exe_path": r"C:\Apps\CoolBrowser\coolbrowser.exe",
            "publisher": "Cool Corp",
        },
        {
            "display_name": "Music Player",
            "exe_name": "musicplayer.exe",
            "exe_path": r"C:\Apps\MusicPlayer\musicplayer.exe",
            "publisher": "Music Corp",
        },
    ]

    dialog = InstalledAppsDialog(apps)
    qtbot.addWidget(dialog)
    dialog.show()

    assert dialog._list.count() == 2

    dialog._search.setText("cool browser")

    assert dialog._list.count() == 1
    assert dialog._list.item(0).text() == "Cool Browser  •  coolbrowser.exe"
    assert "Cool Corp" in dialog._list.item(0).toolTip()
    assert "Gösterilen uygulama sayısı: 1" in dialog._count_lbl.text()


def test_installed_apps_dialog_select_current_returns_selected_app(qtbot):
    apps = [
        {
            "display_name": "Cool Browser",
            "exe_name": "coolbrowser.exe",
            "exe_path": r"C:\Apps\CoolBrowser\coolbrowser.exe",
            "publisher": "Cool Corp",
        }
    ]

    dialog = InstalledAppsDialog(apps)
    qtbot.addWidget(dialog)
    dialog.show()

    dialog._list.setCurrentRow(0)
    dialog._select_current()

    assert dialog.selected_app()["exe_name"] == "coolbrowser.exe"


def test_installed_apps_dialog_double_click_sets_selected_app(qtbot):
    apps = [
        {
            "display_name": "Cool Browser",
            "exe_name": "coolbrowser.exe",
            "exe_path": r"C:\Apps\CoolBrowser\coolbrowser.exe",
            "publisher": "Cool Corp",
        }
    ]

    dialog = InstalledAppsDialog(apps)
    qtbot.addWidget(dialog)
    dialog.show()

    item = dialog._list.item(0)
    dialog._handle_double_click(item)

    assert dialog.selected_app()["exe_name"] == "coolbrowser.exe"


def test_installed_apps_dialog_select_without_item_shows_warning(
    qtbot,
    message_calls,
):
    apps = []

    dialog = InstalledAppsDialog(apps)
    qtbot.addWidget(dialog)
    dialog.show()

    dialog._select_current()

    assert dialog.selected_app() is None
    assert any(call[0] == "warning" for call in message_calls)
    assert any("Lütfen listeden bir uygulama seç" in call[2] for call in message_calls)


# =============================================================================
# Violation UI state
# =============================================================================

def test_violation_state_updates_labels_button_and_popup(page, monkeypatch):
    popup_calls = []

    monkeypatch.setattr(
        page,
        "_show_alert_popup",
        lambda detay, play_sound=False: popup_calls.append((detay, play_sound))
    )

    page._ihlal_isle("discord.exe | Discord")

    assert "EVET" in page._ihlal_lbl.text()
    assert "discord.exe | Discord" in page._detay_lbl.text()

    assert page._allow_last_btn.isEnabled() is True
    assert page._allow_last_shortcut.isEnabled() is True
    assert "discord.exe" in page._allow_last_btn.text()

    assert popup_calls == [("discord.exe | Discord", True)]


def test_same_violation_does_not_request_sound_again(page, monkeypatch):
    popup_calls = []

    monkeypatch.setattr(
        page,
        "_show_alert_popup",
        lambda detay, play_sound=False: popup_calls.append((detay, play_sound))
    )

    page._ihlal_isle("discord.exe | Discord")
    page._ihlal_isle("discord.exe | Discord")

    assert popup_calls[0] == ("discord.exe | Discord", True)
    assert popup_calls[1] == ("discord.exe | Discord", False)


def test_no_violation_state_closes_popup_and_updates_labels(page, monkeypatch):
    closed = []

    monkeypatch.setattr(page, "_show_alert_popup", lambda *args, **kwargs: None)
    monkeypatch.setattr(page, "_close_alert_popup", lambda: closed.append(True))

    page._ihlal_isle("discord.exe | Discord")
    page._ihlal_yok()

    assert closed == [True]
    assert "Yok" in page._ihlal_lbl.text()
    assert page._detay_lbl.text() == "Tespit edilen uygulama: —"
    assert page.logic.ihlal is False


def test_manual_add_matching_current_violation_closes_violation_state(
    page,
    qtbot,
    monkeypatch,
):
    closed = []

    monkeypatch.setattr(page, "_show_alert_popup", lambda *args, **kwargs: None)
    monkeypatch.setattr(page, "_close_alert_popup", lambda: closed.append(True))

    page._ihlal_isle("discord.exe | Discord")

    page._input.setText("discord.exe")
    qtbot.mouseClick(find_button(page, "Elle Ekle"), Qt.MouseButton.LeftButton)

    assert "discord.exe" in page.logic.get_whitelist()
    assert page._allow_last_btn.isEnabled() is False
    assert "Yok" in page._ihlal_lbl.text()
    assert closed == [True]


# =============================================================================
# Allow last violation UI flow
# =============================================================================

def test_allow_last_violation_button_initially_disabled(page):
    assert page._allow_last_btn.isEnabled() is False
    assert page._allow_last_shortcut.isEnabled() is False


def test_allow_last_violation_button_click_adds_last_violation(
    page,
    qtbot,
    monkeypatch,
):
    monkeypatch.setattr(page, "_show_alert_popup", lambda *args, **kwargs: None)

    page._ihlal_isle("discord.exe | Discord")

    assert page._allow_last_btn.isEnabled() is True

    qtbot.mouseClick(page._allow_last_btn, Qt.MouseButton.LeftButton)

    assert "discord.exe" in page.logic.get_whitelist()
    assert page._list_widget.count() == 1
    assert page._list_widget.item(0).text() == "discord.exe"
    assert page._allow_last_btn.isEnabled() is False


def test_allow_last_shortcut_signal_adds_last_violation(page, monkeypatch):
    monkeypatch.setattr(page, "_show_alert_popup", lambda *args, **kwargs: None)

    page._ihlal_isle("steam.exe | Steam")

    assert page._allow_last_shortcut.isEnabled() is True

    page._allow_last_shortcut.activated.emit()

    assert "steam.exe" in page.logic.get_whitelist()
    assert page._allow_last_btn.isEnabled() is False


def test_allow_last_without_violation_shows_information(page, qtbot, message_calls):
    assert page._allow_last_btn.isEnabled() is False

    # Direct method call is used because disabled QPushButton will not emit clicked.
    page._son_ihlale_izin_ver()

    assert page._list_widget.count() == 0
    assert any(call[0] == "information" for call in message_calls)
    assert any("son ihlal" in call[2].lower() for call in message_calls)


# =============================================================================
# Alert popup UI
# =============================================================================

def test_violation_alert_dialog_text_updates(qtbot):
    dialog = ViolationAlertDialog()
    qtbot.addWidget(dialog)

    dialog.set_violation_text("discord.exe | Discord")

    assert "discord.exe | Discord" in dialog._detail_lbl.text()


def test_show_and_close_alert_popup(page, qtbot):
    page._show_alert_popup("discord.exe | Discord", play_sound=False)

    assert page._alert_dialog is not None
    assert page._alert_dialog.isVisible() is True
    assert "discord.exe | Discord" in page._alert_dialog._detail_lbl.text()

    page._close_alert_popup()

    assert page._alert_dialog.isVisible() is False


def test_play_alert_sound_uses_sound_file_when_exists(page, monkeypatch):
    class FakeWinSound:
        SND_FILENAME = 1
        SND_ASYNC = 2
        SND_NODEFAULT = 4
        MB_ICONEXCLAMATION = 8

        def __init__(self):
            self.calls = []

        def PlaySound(self, sound, flags):
            self.calls.append(("PlaySound", sound, flags))

        def MessageBeep(self, icon):
            self.calls.append(("MessageBeep", icon))

    fake_sound = FakeWinSound()

    monkeypatch.setattr(wp, "winsound", fake_sound)
    monkeypatch.setattr(wp.os.path, "exists", lambda path: True)

    page._play_alert_sound_once()

    assert fake_sound.calls
    assert fake_sound.calls[0][0] == "PlaySound"


def test_play_alert_sound_uses_message_beep_when_file_missing(page, monkeypatch):
    class FakeWinSound:
        SND_FILENAME = 1
        SND_ASYNC = 2
        SND_NODEFAULT = 4
        MB_ICONEXCLAMATION = 8

        def __init__(self):
            self.calls = []

        def PlaySound(self, sound, flags):
            self.calls.append(("PlaySound", sound, flags))

        def MessageBeep(self, icon):
            self.calls.append(("MessageBeep", icon))

    fake_sound = FakeWinSound()

    monkeypatch.setattr(wp, "winsound", fake_sound)
    monkeypatch.setattr(wp.os.path, "exists", lambda path: False)

    page._play_alert_sound_once()

    assert fake_sound.calls
    assert fake_sound.calls[0][0] == "MessageBeep"


# =============================================================================
# Monitoring start / stop UI flow
# =============================================================================

def test_start_monitoring_when_win32_unavailable_shows_warning(
    page,
    monkeypatch,
    message_calls,
):
    monkeypatch.setattr(wp, "WIN32_AVAILABLE", False)

    result = page.start_monitoring()

    assert result is False
    assert page._worker is None
    assert page._aktif_lbl.text() == "İzleme: Kapalı"

    assert any(call[0] == "warning" for call in message_calls)
    assert any("pywin32" in call[2] for call in message_calls)


def test_start_monitoring_creates_worker_and_updates_ui(page, monkeypatch):
    FakeMonitorWorker.instances.clear()

    monkeypatch.setattr(wp, "WIN32_AVAILABLE", True)
    monkeypatch.setattr(wp, "MonitorWorker", FakeMonitorWorker)
    monkeypatch.setattr(page, "_show_alert_popup", lambda *args, **kwargs: None)

    result = page.start_monitoring()

    assert result is True
    assert page._worker is not None
    assert len(FakeMonitorWorker.instances) == 1

    worker = FakeMonitorWorker.instances[0]

    assert worker.started is True
    assert worker.interval_ms == 1000
    assert page._aktif_lbl.text() == "İzleme: Açık"
    assert page._ihlal_lbl.text() == "İhlal: —"


def test_start_monitoring_does_not_create_second_worker_if_already_running(
    page,
    monkeypatch,
):
    FakeMonitorWorker.instances.clear()

    monkeypatch.setattr(wp, "WIN32_AVAILABLE", True)
    monkeypatch.setattr(wp, "MonitorWorker", FakeMonitorWorker)

    assert page.start_monitoring() is True
    assert page.start_monitoring() is True

    assert len(FakeMonitorWorker.instances) == 1


def test_worker_violation_signal_updates_ui(page, monkeypatch):
    FakeMonitorWorker.instances.clear()

    monkeypatch.setattr(wp, "WIN32_AVAILABLE", True)
    monkeypatch.setattr(wp, "MonitorWorker", FakeMonitorWorker)
    monkeypatch.setattr(page, "_show_alert_popup", lambda *args, **kwargs: None)

    page.start_monitoring()

    worker = FakeMonitorWorker.instances[0]
    worker.violation_found.emit("discord.exe | Discord")

    assert "EVET" in page._ihlal_lbl.text()
    assert "discord.exe | Discord" in page._detay_lbl.text()
    assert page._allow_last_btn.isEnabled() is True


def test_worker_no_violation_signal_updates_ui(page, monkeypatch):
    FakeMonitorWorker.instances.clear()

    monkeypatch.setattr(wp, "WIN32_AVAILABLE", True)
    monkeypatch.setattr(wp, "MonitorWorker", FakeMonitorWorker)
    monkeypatch.setattr(page, "_show_alert_popup", lambda *args, **kwargs: None)

    page.start_monitoring()

    worker = FakeMonitorWorker.instances[0]
    worker.violation_found.emit("discord.exe | Discord")
    worker.no_violation.emit()

    assert "Yok" in page._ihlal_lbl.text()
    assert page._detay_lbl.text() == "Tespit edilen uygulama: —"


def test_stop_monitoring_stops_worker_and_updates_ui(page, monkeypatch):
    FakeMonitorWorker.instances.clear()

    monkeypatch.setattr(wp, "WIN32_AVAILABLE", True)
    monkeypatch.setattr(wp, "MonitorWorker", FakeMonitorWorker)

    page.start_monitoring()
    worker = FakeMonitorWorker.instances[0]

    page.stop_monitoring()

    assert worker.stopped is True
    assert page._worker is None
    assert page._aktif_lbl.text() == "İzleme: Kapalı"


def test_stop_monitoring_without_worker_is_safe(page):
    page.stop_monitoring()

    assert page._worker is None
    assert page._aktif_lbl.text() == "İzleme: Kapalı"


def test_focus_session_id_is_passed_to_logic_and_db(qtbot, monkeypatch, message_calls):
    FakeMonitorWorker.instances.clear()

    fake_db = FakeDBManager()

    monkeypatch.setattr(wp, "WIN32_AVAILABLE", True)
    monkeypatch.setattr(wp, "MonitorWorker", FakeMonitorWorker)

    widget = WhitelistPage("test_user", fake_db)
    qtbot.addWidget(widget)
    widget.show()

    widget.set_focus_session_id("focus_123")

    widget.start_monitoring()
    widget.stop_monitoring()

    assert len(fake_db.saved_calls) == 1
    assert fake_db.saved_calls[0]["user_id"] == "test_user"
    assert fake_db.saved_calls[0]["focus_session_id"] == "focus_123"


# =============================================================================
# Cleanup / close behavior
# =============================================================================

def test_cleanup_stops_worker_and_closes_popup(page, monkeypatch):
    FakeMonitorWorker.instances.clear()
    closed = []

    monkeypatch.setattr(wp, "WIN32_AVAILABLE", True)
    monkeypatch.setattr(wp, "MonitorWorker", FakeMonitorWorker)
    monkeypatch.setattr(page, "_close_alert_popup", lambda: closed.append(True))

    page.start_monitoring()
    worker = FakeMonitorWorker.instances[0]

    page._cleanup()

    assert worker.stopped is True
    assert page._worker is None

    # _cleanup may close the popup directly and also through _monitoring_bitisini_isle.
    # The important behavior is that cleanup safely attempts to close it.
    assert len(closed) >= 1


def test_close_event_calls_cleanup(page, monkeypatch):
    called = []

    def fake_cleanup():
        called.append(True)

    monkeypatch.setattr(page, "_cleanup", fake_cleanup)

    page.close()

    assert called == [True]