#!/usr/bin/env python3

import site
from pathlib import Path


def get_python_site_packages_path() -> Path:
    repo_path = Path(__file__).parent.parent
    venv_path = repo_path / ".venv"
    if venv_path.exists():
        path = venv_path / "lib/python3.9/site-packages"
        return path

    # global installation happened, not venv
    site_packages_dir = site.getsitepackages()[0]
    return Path(site_packages_dir)


def apply_current_time_entry_patch(site_packages_path: Path) -> None:
    path_to_patch = site_packages_path / "toggl/TogglPy.py"
    assert path_to_patch.exists(), f"File {path_to_patch} does not exist"

    content = path_to_patch.read_text()
    buggy = " = self.postRequest(Endpoints.CURRENT_RUNNING_TIME)"
    fixed = ' = self.postRequest(Endpoints.CURRENT_RUNNING_TIME, method="GET")'
    patched_content = content.replace(buggy, fixed)
    path_to_patch.write_text(patched_content)


def apply_stop_running_time_entry_patch(site_packages_path: Path) -> None:
    path_to_patch = site_packages_path / "toggl/TogglPy.py"
    assert path_to_patch.exists(), f"File {path_to_patch} does not exist"

    content = path_to_patch.read_text()
    buggy = " = self.postRequest(Endpoints.STOP_TIME(entryid))"
    fixed = ' = self.postRequest(Endpoints.STOP_TIME(entryid), method="PUT")'
    patched_content = content.replace(buggy, fixed)
    path_to_patch.write_text(patched_content)


if __name__ == "__main__":
    site_packages_path = get_python_site_packages_path()
    apply_current_time_entry_patch(site_packages_path)
    apply_stop_running_time_entry_patch(site_packages_path)
