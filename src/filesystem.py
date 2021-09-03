import json
from pathlib import Path

from src.types import JsonDict


def read_json_with_comments(path: Path) -> JsonDict:
    with path.open("r") as f:
        json_str = "".join(line for line in f if "//" not in line)
        content = json.loads(json_str)

    return content
