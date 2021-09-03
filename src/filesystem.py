import json
import logging
import sys
from pathlib import Path

from src.types import JsonDict

logger = logging.getLogger(__name__)


def read_json_with_comments(path: Path) -> JsonDict:
    with path.open("r") as f:
        json_str = "".join(line for line in f if "//" not in line)
        content = json.loads(json_str)

    return content


def abort_if_file_does_not_exist(path: Path, message: str) -> None:
    if path.exists():
        return

    logger.error(message)
    print(message)
    sys.exit(1)
