import json
import logging
import sys
from pathlib import Path
from typing import List

from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, FuzzyWordCompleter

from src.types import EntryChoice, JsonDict

CONFIG_PATH = Path("~/.config/t/entries.json").expanduser()


def read_json(path: Path) -> JsonDict:
    with path.open("r") as f:
        content = json.load(f)

    return content


def read_entry_choices(path: Path) -> List[EntryChoice]:
    content = read_json(path=path)

    choices: List[EntryChoice] = []
    for project, names in content["entries_per_project"].items():
        for name in names:
            choice = EntryChoice(name=name, project=project)
            choices.append(choice)

    return choices


def abort_if_config_file_does_not_exist(path: Path) -> None:
    if path.exists():
        return

    msg = f"Please create config file at: {path}"
    logging.error(msg)
    print(msg)
    sys.exit(1)


def configure_completer(choices: List[EntryChoice]) -> Completer:
    words = [choice.to_prompt() for choice in choices]
    completer = FuzzyWordCompleter(words=words)
    return completer


def parse_selected(raw: str) -> EntryChoice:
    name, project = raw.split(" @ ")
    selected = EntryChoice(name=name, project=project)
    return selected


def start_timer_in_toggl_cmd() -> None:
    abort_if_config_file_does_not_exist(path=CONFIG_PATH)

    logging.info("Reading toggl entry choices from config file...")
    entry_choices = read_entry_choices(path=CONFIG_PATH)
    completer = configure_completer(choices=entry_choices)

    logging.info("Prompting user to choose a toggl entry...")
    raw_selected_choice = prompt("Toggl: ", completer=completer)
    selected = parse_selected(raw_selected_choice)
    print(selected)


if __name__ == "__main__":
    log_file = Path(f"{__file__}.log")
    log_format = "%(asctime)s:%(levelname)s:%(filename)s:%(lineno)d:%(message)s"
    logging.basicConfig(filename=log_file, level=logging.DEBUG, format=log_format)

    logging.info("Command started...")
    start_timer_in_toggl_cmd()
    logging.info("Finished command")
