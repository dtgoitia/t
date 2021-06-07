from dataclasses import dataclass
from typing import Any, Dict

JsonDict = Dict[str, Any]


@dataclass
class EntryChoice:
    name: str
    project: str

    def to_prompt(self) -> str:
        return f"{self.name} @ {self.project}"
