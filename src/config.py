import logging
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List

from src.filesystem import read_json_with_comments
from src.types import JsonDict, Project

CONFIG_PATH = Path("~/.config/t/config.json").expanduser()

logger = logging.getLogger(__name__)


@dataclass
class AppConfig:
    projects: List[Project]


def abort_if_config_file_does_not_exist(path: Path) -> None:
    if path.exists():
        return

    msg = f"Please create config file at: {path}"
    logger.error(msg)
    print(msg)
    sys.exit(1)


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


def parse_config(raw: JsonDict) -> AppConfig:
    projects = list(map(parse_project, raw["projects"]))
    config = AppConfig(projects=projects)
    return config


def get_config() -> AppConfig:
    abort_if_config_file_does_not_exist(path=CONFIG_PATH)

    raw_config = read_json_with_comments(path=CONFIG_PATH)
    config = parse_config(raw_config)

    return config
