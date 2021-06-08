import logging
import os
import sys
from pathlib import Path
from typing import List

from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, FuzzyWordCompleter
from toggl.TogglPy import Toggl

from src.config import AppConfig, get_config
from src.types import EntryChoice, TogglProjectId


def get_entry_choices(config: AppConfig) -> List[EntryChoice]:
    choices: List[EntryChoice] = []
    for project in config.projects:
        for name in project.entries:
            choice = EntryChoice(name=name, project=project.name)
            choices.append(choice)

    return choices


def configure_completer(choices: List[EntryChoice]) -> Completer:
    words = [choice.to_prompt() for choice in choices]
    completer = FuzzyWordCompleter(words=words)
    return completer


def parse_selected(raw: str) -> EntryChoice:
    name, project = raw.split(" @ ")
    selected = EntryChoice(name=name, project=project)
    return selected


def get_toggl_api_token() -> str:
    # Get API token at https://track.toggl.com/profile
    try:
        token = os.environ["TOGGL_API_TOKEN"]
    except KeyError:
        msg = "TOGGL_API_TOKEN environment variable not found, please set it"
        logging.error(msg)
        print(msg)
        sys.exit(1)

    return token


def get_toggl_project_id(selected: EntryChoice, config: AppConfig) -> TogglProjectId:
    project = [proj for proj in config.projects if proj.name == selected.project][0]

    return project.id


def start_timer_in_toggl_cmd() -> None:
    config = get_config()
    token = get_toggl_api_token()

    logging.info("Reading toggl entry choices from config file...")
    entry_choices = get_entry_choices(config=config)
    completer = configure_completer(choices=entry_choices)

    logging.info("Prompting user to choose a toggl entry...")
    raw_selected_choice = prompt("Toggl: ", completer=completer)
    selected = parse_selected(raw_selected_choice)
    logging.info(f"User selected {selected}")

    logging.info("Finding corresponding project ID...")
    project_id = get_toggl_project_id(selected, config=config)
    logging.info(f"Project ID: {project_id}")

    logging.info(f"Starting a toggl timer with {selected}...")
    toggl = Toggl()
    toggl.setAPIKey(token)
    _ = toggl.startTimeEntry(selected.name, project_id)


if __name__ == "__main__":
    log_file = Path(f"{__file__}.log")
    log_format = "%(asctime)s:%(levelname)s:%(filename)s:%(lineno)d:%(message)s"
    logging.basicConfig(filename=log_file, level=logging.DEBUG, format=log_format)

    logging.info("Command started...")
    start_timer_in_toggl_cmd()
    logging.info("Finished command")
