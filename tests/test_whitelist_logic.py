import os
from types import SimpleNamespace

import pytest

import whitelist_functionality as wf
from whitelist_functionality import (
    MonitorWorker,
    WhitelistLogic,
    build_violation_entry,
    format_seconds,
    get_active_window_info,
    iter_installed_apps,
    normalize_exe_name,
)


class FakeDBManager:
    def __init__(self):
        self.saved_calls = []

    def save_whitelist_session(self, **kwargs):
        self.saved_calls.append(kwargs)
        return True, "Mock whitelist seansı kaydedildi."


# -----------------------------------------------------------------------------
# Basic helper functions
# -----------------------------------------------------------------------------


def test_format_seconds():
    assert format_seconds(0) == "00:00:00"
    assert format_seconds(0.4) == "00:00:00"
    assert format_seconds(0.6) == "00:00:01"
    assert format_seconds(59) == "00:00:59"
    assert format_seconds(60) == "00:01:00"
    assert format_seconds(3661) == "01:01:01"


def test_normalize_exe_name():
    assert normalize_exe_name("chrome.exe") == "chrome.exe"
    assert normalize_exe_name(" C:/Program Files/Google/Chrome/chrome.exe ") == "chrome.exe"
    assert normalize_exe_name('"spotify.exe"') == "spotify.exe"
    assert normalize_exe_name("'Discord.EXE'") == "discord.exe"
    assert normalize_exe_name(None) == ""
    assert normalize_exe_name("") == ""


# -----------------------------------------------------------------------------
# Windows foreground window helpers
# -----------------------------------------------------------------------------


def test_get_active_window_info_returns_empty_when_win32_unavailable(monkeypatch):
    monkeypatch.setattr(wf, "WIN32_AVAILABLE", False)

    assert get_active_window_info() == ("", "")


def test_get_active_window_info_returns_empty_when_no_window(monkeypatch):
    monkeypatch.setattr(wf, "WIN32_AVAILABLE", True)
    monkeypatch.setattr(
        wf,
        "win32gui",
        SimpleNamespace(GetForegroundWindow=lambda: 0),
        raising=False,
    )

    assert get_active_window_info() == ("", "")


def test_get_active_window_info_returns_title_when_pid_missing(monkeypatch):
    monkeypatch.setattr(wf, "WIN32_AVAILABLE", True)
    monkeypatch.setattr(
        wf,
        "win32gui",
        SimpleNamespace(
            GetForegroundWindow=lambda: 123,
            GetWindowText=lambda hwnd: "  Untitled Window  ",
        ),
        raising=False,
    )
    monkeypatch.setattr(
        wf,
        "win32process",
        SimpleNamespace(GetWindowThreadProcessId=lambda hwnd: (1, 0)),
        raising=False,
    )

    assert get_active_window_info() == ("", "Untitled Window")


def test_get_active_window_info_success(monkeypatch):
    class FakeProcess:
        def name(self):
            return "  CHROME.EXE  "

    monkeypatch.setattr(wf, "WIN32_AVAILABLE", True)
    monkeypatch.setattr(
        wf,
        "win32gui",
        SimpleNamespace(
            GetForegroundWindow=lambda: 123,
            GetWindowText=lambda hwnd: "  Google Chrome  ",
        ),
        raising=False,
    )
    monkeypatch.setattr(
        wf,
        "win32process",
        SimpleNamespace(GetWindowThreadProcessId=lambda hwnd: (1, 555)),
        raising=False,
    )
    monkeypatch.setattr(wf, "psutil", SimpleNamespace(Process=lambda pid: FakeProcess()), raising=False)

    assert get_active_window_info() == ("chrome.exe", "Google Chrome")


def test_get_active_window_info_handles_exceptions(monkeypatch, capsys):
    def raise_error():
        raise RuntimeError("fake foreground error")

    monkeypatch.setattr(wf, "WIN32_AVAILABLE", True)
    monkeypatch.setattr(wf, "win32gui", SimpleNamespace(GetForegroundWindow=raise_error), raising=False)

    assert get_active_window_info() == ("", "")
    assert "Aktif pencere bilgisi alınamadı" in capsys.readouterr().out


# -----------------------------------------------------------------------------
# Registry / installed app helper functions
# -----------------------------------------------------------------------------


def test_safe_reg_read_returns_default_when_winreg_missing(monkeypatch):
    monkeypatch.setattr(wf, "winreg", None)

    assert wf._safe_reg_read(object(), "DisplayName", "DEFAULT") == "DEFAULT"


def test_safe_reg_read_returns_value_and_handles_oserror(monkeypatch):
    class FakeWinReg:
        def QueryValueEx(self, key, value_name):
            if value_name == "DisplayName":
                return "Cool App", None
            raise OSError("missing value")

    monkeypatch.setattr(wf, "winreg", FakeWinReg())

    assert wf._safe_reg_read(object(), "DisplayName", "DEFAULT") == "Cool App"
    assert wf._safe_reg_read(object(), "MissingValue", "DEFAULT") == "DEFAULT"


def test_extract_exe_path():
    assert wf._extract_exe_path("") == ""
    assert wf._extract_exe_path("C:/Program Files/App/readme.txt") == ""

    extracted = wf._extract_exe_path('"/opt/Discord/Discord.exe",0')
    assert extracted.lower().endswith("discord.exe")
    assert ",0" not in extracted

    extracted = wf._extract_exe_path("'/opt/Spotify/Spotify.exe' ")
    assert extracted.lower().endswith("spotify.exe")


def test_score_exe_candidate_prefers_matching_app_and_rejects_system_exe():
    system_score = wf._score_exe_candidate("C:/Windows/explorer.exe", "Explorer")
    good_score = wf._score_exe_candidate("C:/Apps/discord.exe", "Discord")
    updater_score = wf._score_exe_candidate("C:/Apps/discord_updater.exe", "Discord")
    generic_score = wf._score_exe_candidate("C:/Apps/app.exe", "Cool App")
    short_token_score = wf._score_exe_candidate("C:/Apps/aihelper.exe", "AI")

    assert isinstance(short_token_score, int)
    assert system_score == -999
    assert good_score > updater_score
    assert good_score > generic_score


def test_guess_exe_from_install_location(tmp_path, monkeypatch):
    install_dir = tmp_path / "CoolApp"
    install_dir.mkdir()
    good_exe = install_dir / "coolapp.exe"
    bad_exe = install_dir / "uninstall.exe"
    readme = install_dir / "readme.txt"

    good_exe.write_text("fake exe")
    bad_exe.write_text("fake uninstall")
    readme.write_text("not exe")

    guessed = wf._guess_exe_from_install_location(str(install_dir), "CoolApp")

    assert os.path.basename(guessed).lower() == "coolapp.exe"
    assert wf._guess_exe_from_install_location("", "CoolApp") == ""
    assert wf._guess_exe_from_install_location(str(tmp_path / "missing"), "CoolApp") == ""

    empty_dir = tmp_path / "Empty"
    empty_dir.mkdir()
    assert wf._guess_exe_from_install_location(str(empty_dir), "Empty") == ""

    low_score_dir = tmp_path / "LowScore"
    low_score_dir.mkdir()
    (low_score_dir / "helper.exe").write_text("fake helper")
    assert wf._guess_exe_from_install_location(str(low_score_dir), "UnknownProduct") == ""

    def raise_oserror(folder):
        raise OSError("cannot scan")

    monkeypatch.setattr(wf.os, "scandir", raise_oserror)
    assert wf._guess_exe_from_install_location(str(install_dir), "CoolApp") == ""


def test_iter_installed_apps_returns_empty_outside_windows_or_without_winreg(monkeypatch):
    monkeypatch.setattr(wf.os, "name", "posix", raising=False)
    monkeypatch.setattr(wf, "winreg", object())
    assert iter_installed_apps() == []

    monkeypatch.setattr(wf.os, "name", "nt", raising=False)
    monkeypatch.setattr(wf, "winreg", None)
    assert iter_installed_apps() == []


def test_iter_installed_apps_reads_registry_filters_and_sorts(tmp_path, monkeypatch):
    guessed_dir = tmp_path / "NeedsGuess"
    guessed_dir.mkdir()
    guessed_exe = guessed_dir / "needsguess.exe"
    guessed_exe.write_text("fake exe")

    class FakeRegistryKey:
        def __init__(self, values=None, subkeys=None):
            self.values = values or {}
            self.subkeys = subkeys or []

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

    class FakeWinReg:
        HKEY_LOCAL_MACHINE = "HKLM"
        HKEY_CURRENT_USER = "HKCU"
        KEY_READ = 1
        KEY_WOW64_64KEY = 2
        KEY_WOW64_32KEY = 4

        def __init__(self):
            self.good = FakeRegistryKey({
                "DisplayName": "Cool Browser",
                "DisplayIcon": f'"{tmp_path / "CoolBrowser" / "coolbrowser.exe"}",0',
                "InstallLocation": "",
                "Publisher": "Cool Corp",
            })
            self.no_name = FakeRegistryKey({})
            self.system_component = FakeRegistryKey({
                "DisplayName": "Hidden Driver",
                "SystemComponent": 1,
            })
            self.hotfix = FakeRegistryKey({
                "DisplayName": "Security Patch",
                "ReleaseType": "Hotfix",
            })
            self.invalid_system_component = FakeRegistryKey({
                "DisplayName": "Invalid System Component",
                "SystemComponent": "not-an-int",
                "DisplayIcon": f'"{tmp_path / "InvalidSystem" / "invalidsystem.exe"}",0',
                "Publisher": "Invalid Corp",
            })
            self.needs_guess = FakeRegistryKey({
                "DisplayName": "NeedsGuess",
                "DisplayIcon": "",
                "InstallLocation": str(guessed_dir),
                "Publisher": "Guess Corp",
            })
            self.no_executable = FakeRegistryKey({
                "DisplayName": "No Executable",
                "DisplayIcon": "",
                "InstallLocation": "",
            })
            self.uninstaller = FakeRegistryKey({
                "DisplayName": "Bad App",
                "DisplayIcon": str(tmp_path / "Bad" / "uninstall.exe"),
            })
            self.duplicate_good = FakeRegistryKey(self.good.values.copy())

            self.parent = FakeRegistryKey(subkeys=[
                ("Good", self.good),
                ("NoName", self.no_name),
                ("SystemComponent", self.system_component),
                ("InvalidSystem", self.invalid_system_component),
                ("Hotfix", self.hotfix),
                ("NeedsGuess", self.needs_guess),
                ("NoExecutable", self.no_executable),
                ("Uninstaller", self.uninstaller),
                ("DuplicateGood", self.duplicate_good),
                ("BrokenOpen", FakeRegistryKey()),
            ])

        def OpenKey(self, root, path, reserved=0, access=0):
            if isinstance(root, FakeRegistryKey):
                if path == "BrokenOpen":
                    raise OSError("cannot open subkey")
                for subkey_name, subkey in root.subkeys:
                    if subkey_name == path:
                        return subkey
                raise OSError("subkey not found")
            return self.parent

        def EnumKey(self, parent_key, index):
            try:
                return parent_key.subkeys[index][0]
            except IndexError:
                raise OSError("no more keys")

        def QueryValueEx(self, key, value_name):
            if value_name in key.values:
                return key.values[value_name], None
            raise OSError("missing value")

    monkeypatch.setattr(wf.os, "name", "nt", raising=False)
    monkeypatch.setattr(wf, "winreg", FakeWinReg())

    apps = iter_installed_apps()

    assert [app["display_name"] for app in apps] == [
        "Cool Browser",
        "Invalid System Component",
        "NeedsGuess",
    ]
    assert [app["exe_name"] for app in apps] == [
        "coolbrowser.exe",
        "invalidsystem.exe",
        "needsguess.exe",
    ]
    assert apps[0]["publisher"] == "Cool Corp"
    assert apps[0]["source"] == "registry"
    assert len(apps) == 3


def test_iter_installed_apps_skips_non_exe_path_returned_by_helper(monkeypatch):
    class FakeRegistryKey:
        def __init__(self, values=None, subkeys=None):
            self.values = values or {}
            self.subkeys = subkeys or []

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

    class FakeWinReg:
        HKEY_LOCAL_MACHINE = "HKLM"
        HKEY_CURRENT_USER = "HKCU"
        KEY_READ = 1

        def __init__(self):
            self.app_key = FakeRegistryKey({
                "DisplayName": "Text Only App",
                "DisplayIcon": "fake-icon-value",
            })
            self.parent = FakeRegistryKey(subkeys=[("TextOnly", self.app_key)])

        def OpenKey(self, root, path, reserved=0, access=0):
            if isinstance(root, FakeRegistryKey):
                return self.app_key
            return self.parent

        def EnumKey(self, parent_key, index):
            if index == 0:
                return "TextOnly"
            raise OSError("no more keys")

        def QueryValueEx(self, key, value_name):
            if value_name in key.values:
                return key.values[value_name], None
            raise OSError("missing value")

    monkeypatch.setattr(wf.os, "name", "nt", raising=False)
    monkeypatch.setattr(wf, "winreg", FakeWinReg())
    monkeypatch.setattr(wf, "_extract_exe_path", lambda raw: "C:/Apps/readme.txt")

    assert iter_installed_apps() == []


def test_iter_installed_apps_handles_openkey_oserror(monkeypatch):
    class FakeWinReg:
        HKEY_LOCAL_MACHINE = "HKLM"
        HKEY_CURRENT_USER = "HKCU"
        KEY_READ = 1
        KEY_WOW64_64KEY = 2
        KEY_WOW64_32KEY = 4

        def OpenKey(self, *args, **kwargs):
            raise OSError("registry unavailable")

    monkeypatch.setattr(wf.os, "name", "nt", raising=False)
    monkeypatch.setattr(wf, "winreg", FakeWinReg())

    assert iter_installed_apps() == []


# -----------------------------------------------------------------------------
# MonitorWorker behavior
# -----------------------------------------------------------------------------


def test_monitor_worker_emit_helpers_emit_only_when_state_changes():
    worker = MonitorWorker(lambda: set(), interval_ms=1)
    events = []

    worker.no_violation.connect(lambda: events.append("ok"))
    worker.violation_found.connect(lambda detail: events.append(detail))

    worker._emit_ok_if_changed()
    worker._emit_ok_if_changed()
    worker._emit_violation_if_changed("discord.exe | Discord")
    worker._emit_violation_if_changed("discord.exe | Discord")
    worker._emit_ok_if_changed()

    assert events == ["ok", "discord.exe | Discord", "ok"]


@pytest.mark.parametrize(
    "exe_name, title, whitelist, expected_events",
    [
        ("", "", set(), ["ok"]),
        ("explorer.exe", "Windows Explorer", set(), ["ok"]),
        ("code.exe", "Visual Studio Code", set(), ["ok"]),
        ("chrome.exe", "Chrome", {"chrome.exe"}, ["ok"]),
        ("discord.exe", "Discord", set(), ["discord.exe | Discord"]),
        ("steam.exe", "", set(), ["steam.exe"]),
    ],
)
def test_monitor_worker_run_one_cycle_for_common_states(
    monkeypatch,
    exe_name,
    title,
    whitelist,
    expected_events,
):
    worker = MonitorWorker(lambda: whitelist, interval_ms=1)
    events = []

    worker.no_violation.connect(lambda: events.append("ok"))
    worker.violation_found.connect(lambda detail: events.append(detail))

    monkeypatch.setattr(wf, "get_active_window_info", lambda: (exe_name, title))

    def stop_after_sleep(_ms):
        worker._running = False

    monkeypatch.setattr(worker, "msleep", stop_after_sleep)
    worker.run()

    assert events == expected_events


def test_monitor_worker_run_allows_python_focusync_when_python_removed_from_self_exes(monkeypatch):
    worker = MonitorWorker(lambda: set(), interval_ms=1)
    events = []

    worker.no_violation.connect(lambda: events.append("ok"))
    worker.violation_found.connect(lambda detail: events.append(detail))

    monkeypatch.setattr(wf, "SELF_EXES", {"focusync.exe", "code.exe", "pycharm64.exe"})
    monkeypatch.setattr(wf, "get_active_window_info", lambda: ("python.exe", "FocuSync Main Window"))

    def stop_after_sleep(_ms):
        worker._running = False

    monkeypatch.setattr(worker, "msleep", stop_after_sleep)
    worker.run()

    assert events == ["ok"]


def test_monitor_worker_stop_sets_running_false_and_waits(monkeypatch):
    worker = MonitorWorker(lambda: set(), interval_ms=1)
    calls = []

    monkeypatch.setattr(MonitorWorker, "quit", lambda self: calls.append("quit"))
    monkeypatch.setattr(MonitorWorker, "wait", lambda self, timeout=None: calls.append(("wait", timeout)))

    worker._running = True

    worker.stop()

    assert worker._running is False
    assert calls == ["quit", ("wait", 1000)]

# -----------------------------------------------------------------------------
# WhitelistLogic behavior
# -----------------------------------------------------------------------------


def test_get_whitelist_returns_copy_and_whitelist_items_are_sorted():
    logic = WhitelistLogic("test_user", None)
    logic.add_exe_to_whitelist("spotify.exe")
    logic.add_exe_to_whitelist("chrome.exe")

    returned_copy = logic.get_whitelist()
    returned_copy.add("external.exe")

    assert logic.whitelist_items() == ["chrome.exe", "spotify.exe"]
    assert "external.exe" not in logic.get_whitelist()


def test_current_violation_exe_and_clear_last_violation():
    logic = WhitelistLogic("test_user", None)

    assert logic.current_violation_exe() == ""
    assert logic.has_last_violation() is False

    logic.process_violation("Discord.EXE | Discord")

    assert logic.current_violation_exe() == "discord.exe"
    assert logic.has_last_violation() is True

    logic.clear_last_violation()

    assert logic.has_last_violation() is False


def test_start_monitoring_resets_runtime_state(monkeypatch):
    logic = WhitelistLogic("test_user", None)
    logic._whitelist.add("chrome.exe")
    logic.ihlal = True
    logic._son_ihlal = "discord.exe | Discord"
    logic._last_violation_exe = "discord.exe"
    logic._violation_log.append({"app_name": "discord.exe"})
    logic._active_violation_exe = "discord.exe"
    logic._active_violation_start = 999.0
    logic._total_monitoring_seconds = 50.0
    logic._total_violation_seconds = 20.0

    monkeypatch.setattr(wf.time, "time", lambda: 1000.0)

    logic.start_monitoring()

    assert logic._monitoring_start_time == 1000.0
    assert logic._whitelist == {"chrome.exe"}
    assert logic.ihlal is False
    assert logic._son_ihlal == ""
    assert logic.has_last_violation() is False
    assert logic._violation_log == []
    assert logic._active_violation_exe == ""
    assert logic._active_violation_start is None
    assert logic._total_monitoring_seconds == 0.0
    assert logic._total_violation_seconds == 0.0


def test_add_exe_to_whitelist_branch_coverage():
    logic = WhitelistLogic("test_user", None)

    result = logic.add_exe_to_whitelist("")
    assert result["ok"] is False
    assert result["level"] == "warning"

    result = logic.add_exe_to_whitelist("chrome")
    assert result["ok"] is False
    assert result["level"] == "warning"
    assert result["exe_name"] == "chrome"

    result = logic.add_exe_to_whitelist("chrome.exe")
    assert result["ok"] is True
    assert result["exe_name"] == "chrome.exe"
    assert "chrome.exe" in logic.get_whitelist()

    result = logic.add_exe_to_whitelist("chrome.exe")
    assert result["ok"] is False
    assert result["level"] == "info"


def test_add_exe_to_whitelist_clears_matching_active_violation(monkeypatch):
    logic = WhitelistLogic("test_user", None)
    times = iter([
        1000.0,  # process_violation active start
        1000.0,  # process_violation general violation start
        1005.0,  # process_no_violation total violation duration
        1005.0,  # finish_current_episode end time
    ])
    monkeypatch.setattr(wf.time, "time", lambda: next(times))

    logic.process_violation("discord.exe | Discord")
    result = logic.add_exe_to_whitelist("discord.exe")

    assert result["ok"] is True
    assert result["clear_info"]["ended"] is True
    assert logic.ihlal is False
    assert logic.has_last_violation() is False
    assert logic._total_violation_seconds == 5
    assert logic._violation_log[0]["app_name"] == "discord.exe"


def test_remove_exe_from_whitelist():
    logic = WhitelistLogic("test_user", None)

    assert logic.remove_exe_from_whitelist("") == (False, "")

    logic.add_exe_to_whitelist("spotify.exe")
    assert "spotify.exe" in logic.get_whitelist()

    ok, exe_name = logic.remove_exe_from_whitelist("spotify.exe")

    assert ok is True
    assert exe_name == "spotify.exe"
    assert "spotify.exe" not in logic.get_whitelist()

    ok, exe_name = logic.remove_exe_from_whitelist("missing.exe")
    assert ok is True
    assert exe_name == "missing.exe"


def test_allow_last_violation_when_no_violation_exists():
    logic = WhitelistLogic("test_user", None)

    result = logic.allow_last_violation()

    assert result["ok"] is False
    assert result["level"] == "info"


def test_allow_last_violation_adds_normal_exe_to_whitelist():
    logic = WhitelistLogic("test_user", None)

    logic.process_violation("discord.exe | Discord")
    result = logic.allow_last_violation()

    assert result["ok"] is True
    assert result["exe_name"] == "discord.exe"
    assert "discord.exe" in logic.get_whitelist()
    assert logic.has_last_violation() is False


def test_allow_last_violation_does_not_add_system_exe():
    logic = WhitelistLogic("test_user", None)

    logic.process_violation("explorer.exe | Windows Explorer")
    result = logic.allow_last_violation()

    assert result["ok"] is False
    assert "explorer.exe" not in logic.get_whitelist()
    assert logic.has_last_violation() is False


def test_allow_last_violation_does_not_add_self_exe():
    logic = WhitelistLogic("test_user", None)

    logic.process_violation("code.exe | Visual Studio Code")
    result = logic.allow_last_violation()

    assert result["ok"] is False
    assert "code.exe" not in logic.get_whitelist()
    assert logic.has_last_violation() is False


def test_allow_last_violation_when_exe_already_whitelisted():
    logic = WhitelistLogic("test_user", None)

    logic.add_exe_to_whitelist("discord.exe")
    logic.process_violation("discord.exe | Discord")
    result = logic.allow_last_violation()

    assert result["ok"] is False
    assert result["level"] == "info"
    assert result["exe_name"] == "discord.exe"
    assert logic.has_last_violation() is False
    assert logic.whitelist_items() == ["discord.exe"]


def test_process_violation_state_transition():
    logic = WhitelistLogic("test_user", None)

    result = logic.process_violation("discord.exe | Discord")

    assert result["started_new"] is True
    assert result["exe_name"] == "discord.exe"
    assert logic.ihlal is True
    assert logic._son_ihlal == "discord.exe | Discord"
    assert logic._last_violation_exe == "discord.exe"
    assert logic._active_violation_exe == "discord.exe"
    assert logic._active_violation_start is not None


def test_process_violation_with_empty_detail_does_not_set_last_exe():
    logic = WhitelistLogic("test_user", None)

    result = logic.process_violation("")

    assert result["exe_name"] == ""
    assert result["started_new"] is True
    assert logic._last_violation_exe is None
    assert logic._active_violation_exe == ""
    assert logic.ihlal is True


def test_same_violation_does_not_start_new_episode():
    logic = WhitelistLogic("test_user", None)

    first = logic.process_violation("discord.exe | Discord")
    second = logic.process_violation("discord.exe | Discord")

    assert first["started_new"] is True
    assert second["started_new"] is False
    assert logic.ihlal is True


def test_different_violation_finishes_previous_episode(monkeypatch):
    logic = WhitelistLogic("test_user", None)

    times = iter([
        1000.0,  # first violation active start
        1000.0,  # first violation general start
        1005.0,  # finish discord episode
        1005.0,  # steam active start
    ])

    monkeypatch.setattr(wf.time, "time", lambda: next(times))

    logic.process_violation("discord.exe | Discord")
    logic.process_violation("steam.exe | Steam")

    assert len(logic._violation_log) == 1
    assert logic._violation_log[0]["app_name"] == "discord.exe"
    assert logic._violation_log[0]["duration_seconds"] == 5
    assert logic._active_violation_exe == "steam.exe"


def test_process_no_violation_when_no_active_violation():
    logic = WhitelistLogic("test_user", None)

    result = logic.process_no_violation()

    assert result == {"ended": False, "last_violation": ""}
    assert logic.ihlal is False
    assert logic._son_ihlal == ""


def test_process_no_violation_closes_active_episode(monkeypatch):
    logic = WhitelistLogic("test_user", None)

    times = iter([
        1000.0,  # active violation start
        1000.0,  # general violation start
        1005.0,  # total violation duration calculation
        1005.0,  # finish episode end time
    ])

    monkeypatch.setattr(wf.time, "time", lambda: next(times))

    logic.process_violation("discord.exe | Discord")
    result = logic.process_no_violation()

    assert result["ended"] is True
    assert result["last_violation"] == "discord.exe | Discord"
    assert logic.ihlal is False
    assert logic._son_ihlal == ""
    assert int(round(logic._total_violation_seconds)) == 5
    assert len(logic._violation_log) == 1
    assert logic._violation_log[0]["app_name"] == "discord.exe"


def test_build_violation_entry_returns_none_for_missing_inputs():
    assert build_violation_entry("", 1000.0) is None
    assert build_violation_entry("discord.exe", None) is None


def test_build_violation_entry_ignores_short_violations(monkeypatch):
    monkeypatch.setattr(wf.time, "time", lambda: 1000.5)

    entry = build_violation_entry("discord.exe", 1000.0)

    assert entry is None


def test_build_violation_entry_creates_valid_log(monkeypatch):
    monkeypatch.setattr(wf.time, "time", lambda: 1002.0)

    entry = build_violation_entry("discord.exe", 1000.0)

    assert entry is not None
    assert entry["app_name"] == "discord.exe"
    assert entry["duration_seconds"] == 2
    assert entry["duration_hms"] == "00:00:02"
    assert entry["started_at"].tzinfo is not None
    assert entry["ended_at"].tzinfo is not None


def test_finish_current_episode_appends_valid_entry_and_resets_state(monkeypatch):
    logic = WhitelistLogic("test_user", None)
    logic._active_violation_exe = "discord.exe"
    logic._active_violation_start = 1000.0
    monkeypatch.setattr(wf.time, "time", lambda: 1003.0)

    entry = logic.finish_current_episode()

    assert entry["duration_seconds"] == 3
    assert logic._violation_log == [entry]
    assert logic._active_violation_exe == ""
    assert logic._active_violation_start is None


def test_finish_current_episode_ignores_invalid_or_short_entry(monkeypatch):
    logic = WhitelistLogic("test_user", None)
    logic._active_violation_exe = "discord.exe"
    logic._active_violation_start = 1000.0
    monkeypatch.setattr(wf.time, "time", lambda: 1000.2)

    entry = logic.finish_current_episode()

    assert entry is None
    assert logic._violation_log == []
    assert logic._active_violation_exe == ""
    assert logic._active_violation_start is None


def test_stop_monitoring_without_start_returns_none():
    logic = WhitelistLogic("test_user", None)

    assert logic.stop_monitoring_and_save() is None


def test_stop_monitoring_without_db_manager(monkeypatch):
    logic = WhitelistLogic("test_user", None)

    times = iter([
        1000.0,  # monitoring start
        1010.0,  # monitoring stop
    ])

    monkeypatch.setattr(wf.time, "time", lambda: next(times))

    logic.start_monitoring()
    summary = logic.stop_monitoring_and_save()

    assert summary["db_ok"] is None
    assert summary["db_msg"] == "[DB] db_manager yok, kayıt atlandı."
    assert summary["total_hms"] == "00:00:10"
    assert summary["violation_hms"] == "00:00:00"
    assert summary["record_count"] == 0


def test_stop_monitoring_saves_to_mock_database(monkeypatch):
    fake_db = FakeDBManager()
    logic = WhitelistLogic("test_user", fake_db)
    logic.set_focus_session_id("focus_123")

    times = iter([
        1000.0,  # monitoring start
        1015.0,  # monitoring stop
    ])

    monkeypatch.setattr(wf.time, "time", lambda: next(times))

    logic.start_monitoring()
    summary = logic.stop_monitoring_and_save()

    assert summary["db_ok"] is True
    assert len(fake_db.saved_calls) == 1

    saved_data = fake_db.saved_calls[0]

    assert saved_data["user_id"] == "test_user"
    assert saved_data["focus_session_id"] == "focus_123"
    assert saved_data["total_duration"] == 15
    assert saved_data["violation_duration"] == 0
    assert saved_data["total_duration_hms"] == "00:00:15"
    assert saved_data["violation_duration_hms"] == "00:00:00"
    assert saved_data["violations"] == []
    assert saved_data["session_started_at"].tzinfo is not None
    assert saved_data["session_ended_at"].tzinfo is not None


def test_stop_monitoring_saves_active_violation_and_clears_runtime_state(monkeypatch):
    fake_db = FakeDBManager()
    logic = WhitelistLogic("test_user", fake_db)
    times = iter([
        1000.0,  # start_monitoring
        1001.0,  # process_violation active start
        1001.0,  # process_violation general violation start
        1010.0,  # stop total monitoring duration
        1010.0,  # active violation total duration
        1010.0,  # finish_current_episode end time
    ])
    monkeypatch.setattr(wf.time, "time", lambda: next(times))

    logic.start_monitoring()
    logic.process_violation("discord.exe | Discord")
    summary = logic.stop_monitoring_and_save()

    saved_data = fake_db.saved_calls[0]

    assert summary["db_ok"] is True
    assert summary["total_hms"] == "00:00:10"
    assert summary["violation_hms"] == "00:00:09"
    assert summary["record_count"] == 1
    assert saved_data["violation_duration"] == 9
    assert saved_data["violations"][0]["app_name"] == "discord.exe"
    assert saved_data["violations"][0]["duration_seconds"] == 9

    assert logic._monitoring_start_time is None
    assert logic._violation_log == []
    assert logic._active_violation_exe == ""
    assert logic._active_violation_start is None
