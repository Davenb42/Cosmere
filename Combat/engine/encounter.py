from dataclasses import dataclass
from typing import List

from engine.character import Character


@dataclass
class Encounter:

    name: str

    combatants: List[Character]