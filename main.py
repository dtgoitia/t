import os
import sys

from prompt_toolkit import prompt
from prompt_toolkit.completion import FuzzyWordCompleter

options = [
    "Break @ Babylon Health",
    "Code review @ Babylon Health",
    "Coding @ Babylon Health",
    "Coding @ Learn and study",
    "Study coding @ Learn and study",
    "Meeting @ Babylon Health",
    "Pairing @ Babylon Health",
    "Support @ Babylon Health",
]
completer = FuzzyWordCompleter(words=options)

selected = prompt("Toggl: ", completer=completer)

print("selected option:", selected)
