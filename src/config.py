import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import List

from src.filesystem import abort_if_file_does_not_exist, read_json_with_comments
from src.types import JsonDict, Project

DOTFILES_DIR = Path(os.environ.get("CONFIG_DIR_PATH") or "~/.config/t").expanduser()
CONFIG_PATH = DOTFILES_DIR / "config.jsonc"
CREDENTIALS_PATH = DOTFILES_DIR / "credentials.jsonc"

logger = logging.getLogger(__name__)

TogglApiToken = str


@dataclass
class AppConfig:
    projects: List[Project]
    api_token: TogglApiToken


def abort_if_config_file_does_not_exist(path: Path) -> None:
    msg = f"Please create config file at: {path}"
    abort_if_file_does_not_exist(path=path, message=msg)


def abort_if_credentials_file_does_not_exist(path: Path) -> None:
    msg = f"Please create credentials file at: {path}"
    abort_if_file_does_not_exist(path=path, message=msg)


def parse_project(raw: JsonDict) -> Project:
    """
    {
      "id": 1234,
      "name": "project name",
      "entries": ["timer entry A name", "timer entry B name"]
    }
    """
    project = Project(
        id=raw["id"],
        name=raw["name"],
        entries=raw["entries"],
    )
    return project


def parse_credentials(credentials: JsonDict) -> TogglApiToken:
    return credentials["toggle_api_token"]


def parse_config(config_path: Path, credentials_path: Path) -> AppConfig:
    raw_config = read_json_with_comments(path=CONFIG_PATH)
    projects = list(map(parse_project, raw_config["projects"]))

    credentials = read_json_with_comments(path=credentials_path)
    api_token = parse_credentials(credentials)

    config = AppConfig(projects=projects, api_token=api_token)
    return config


def get_config() -> AppConfig:
    abort_if_config_file_does_not_exist(path=CONFIG_PATH)
    abort_if_credentials_file_does_not_exist(path=CREDENTIALS_PATH)

    config = parse_config(config_path=CONFIG_PATH, credentials_path=CREDENTIALS_PATH)

    return config
