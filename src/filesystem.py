import json
from pathlib import Path

from src.types import JsonDict


def read_json(path: Path) -> JsonDict:
    with path.open("r") as f:
        content = json.load(f)

    return content
