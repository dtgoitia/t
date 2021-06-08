from dataclasses import dataclass
from typing import Any, Dict, List

JsonDict = Dict[str, Any]
TogglProjectId = int
TogglProjectName = str
ToggleEntryName = str


@dataclass
class EntryChoice:
    name: ToggleEntryName
    project: TogglProjectName

    def to_prompt(self) -> str:
        return f"{self.name} @ {self.project}"


@dataclass
class Project:
    id: TogglProjectId
    name: TogglProjectName
    entries: List[ToggleEntryName]
