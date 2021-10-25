#!/usr/bin/env python3

import re
from pathlib import Path

CLI_NAME = "t"
LOCAL_BIN_PATH = Path("~/.local/bin").expanduser()
WRAPPER_PATH = LOCAL_BIN_PATH / CLI_NAME

VERSION_PATTERN = re.compile(r"^VERSION=([0-9\.]{6,})$")


SemanticVersion = str
ContainerImageName = str


def uninstall_container_wrapper() -> None:
    print(f"Deleting wrapper: {WRAPPER_PATH}")
    WRAPPER_PATH.unlink()

    print("Uninstallation finished")


def main() -> None:
    if not WRAPPER_PATH.exists():
        print("Nothing to uninstall")
        exit(1)

    uninstall_container_wrapper()


if __name__ == "__main__":
    main()
