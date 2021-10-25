#!/usr/bin/env python3

import stat
from pathlib import Path

CLI_NAME = "t"
LOCAL_BIN_PATH = Path("~/.local/bin").expanduser()
WRAPPER_PATH = LOCAL_BIN_PATH / CLI_NAME

TEMPLATE_PATH = Path(__file__).parent / "cli-wrapper-template"

SemanticVersion = str
ContainerImageName = str
Script = str


def get_version() -> SemanticVersion:
    path = Path(__file__).parent.parent / "VERSION"
    return path.read_text().strip()


def get_podman_image_name() -> ContainerImageName:
    path = Path(__file__).parent.parent / "IMAGE_NAME"
    return path.read_text().strip()


def install_container_wrapper() -> None:
    # Collect required values
    template = TEMPLATE_PATH.read_text()
    version = get_version()
    image = get_podman_image_name()
    assert all((template, version, image))

    # Create ~/.local/bin directory if required
    LOCAL_BIN_PATH.mkdir(parents=True, exist_ok=True)

    # Create executable
    script = template.replace("VERSION_PLACEHOLDER", version)
    script = script.replace("IMAGE_PLACEHOLDER", image)
    print(f"Creating wrapper: {WRAPPER_PATH}")
    WRAPPER_PATH.write_text(script)

    # Grant executable permissions: https://stackoverflow.com/a/12792002
    current_permissions = WRAPPER_PATH.stat().st_mode
    executable_permission = current_permissions | stat.S_IEXEC
    print("Assigning execution permissions...")
    WRAPPER_PATH.chmod(executable_permission)

    print("Installation finished")


def main() -> None:
    if WRAPPER_PATH.exists():
        print("Already installed, please update command instead")
        print("Installation aborted")
        exit(1)

    install_container_wrapper()


if __name__ == "__main__":
    main()
