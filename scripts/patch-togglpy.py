#!/usr/bin/env python3

from pathlib import Path


def apply_current_time_entry_patch():
    repo_path = Path(__file__).parent.parent
    venv_path = repo_path / ".venv"
    path_to_patch = venv_path / "lib/python3.9/site-packages/toggl/TogglPy.py"
    assert path_to_patch.exists(), f"File {path_to_patch} does not exist"

    content = path_to_patch.read_text()
    buggy = " = self.postRequest(Endpoints.CURRENT_RUNNING_TIME)"
    fixed = ' = self.postRequest(Endpoints.CURRENT_RUNNING_TIME, method="GET")'
    patched_content = content.replace(buggy, fixed)
    path_to_patch.write_text(patched_content)


def apply_stop_running_time_entry_patch():
    repo_path = Path(__file__).parent.parent
    venv_path = repo_path / ".venv"
    path_to_patch = venv_path / "lib/python3.9/site-packages/toggl/TogglPy.py"
    assert path_to_patch.exists(), f"File {path_to_patch} does not exist"

    content = path_to_patch.read_text()
    buggy = " = self.postRequest(Endpoints.STOP_TIME(entryid))"
    fixed = ' = self.postRequest(Endpoints.STOP_TIME(entryid), method="PUT")'
    patched_content = content.replace(buggy, fixed)
    path_to_patch.write_text(patched_content)


if __name__ == "__main__":
    apply_current_time_entry_patch()
    apply_stop_running_time_entry_patch()
