import logging
from pathlib import Path

import click

from src.domain import show_running_entry, start_timer_in_toggl_cmd, stop_running_entry


@click.group(invoke_without_command=True)
@click.pass_context
def t_group(context: click.Context) -> None:
    if not context.invoked_subcommand:
        start_timer_in_toggl_cmd()
        return


@t_group.command(name="status", help="Show current status of the timer")
def show_running_entry_cmd() -> None:
    show_running_entry()


@t_group.command(name="stop", help="Stop timer")
def stop_running_entry_cmd() -> None:
    stop_running_entry()


if __name__ == "__main__":
    log_file = Path(f"{__file__}.log")
    log_format = "%(asctime)s:%(levelname)s:%(filename)s:%(lineno)d:%(message)s"
    logging.basicConfig(filename=log_file, level=logging.DEBUG, format=log_format)

    logging.info("Command started...")
    t_group()
    logging.info("Finished command")
