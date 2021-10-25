import datetime
import logging
import os
import sys
from typing import List

from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, FuzzyWordCompleter
from toggl.TogglPy import Toggl

from src.config import AppConfig, TogglApiToken, get_config
from src.types import EntryChoice, JsonDict, TogglProjectId, TogglProjectName


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


def get_project_name(project_id: TogglProjectId, config: AppConfig) -> TogglProjectName:
    project = [proj for proj in config.projects if proj.id == project_id][0]

    return project.name


def get_toggl_client(token: TogglApiToken) -> Toggl:
    toggl = Toggl()
    toggl.setAPIKey(token)
    return toggl


def start_timer_in_toggl_cmd() -> None:
    config = get_config()
    toggl = get_toggl_client(token=config.api_token)

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
    _ = toggl.startTimeEntry(selected.name, project_id)


def format_time_entry_response(data: JsonDict, config: AppConfig) -> str:
    project_id = data["pid"]
    project = get_project_name(project_id=project_id, config=config)
    description = data["description"]
    start = datetime.datetime.fromisoformat(data["start"])
    now = datetime.datetime.now(datetime.timezone.utc)
    duration_in_secs = round((now - start).total_seconds())
    duration = datetime.timedelta(seconds=duration_in_secs)
    return f"{description} @ {project}  {duration}"


def show_running_entry():
    config = get_config()
    toggl = get_toggl_client(token=config.api_token)

    data = toggl.currentRunningTimeEntry().get("data")
    if not data:
        print("No time entry running")
        return

    print(format_time_entry_response(data, config))


def stop_running_entry():
    config = get_config()
    toggl = get_toggl_client(token=config.api_token)

    data = toggl.currentRunningTimeEntry().get("data")
    if not data:
        print("No time entry running")
        return

    entry_id = data["id"]
    toggl.stopTimeEntry(entry_id)
