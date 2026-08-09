from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from combat_tracker.engine.defenses import Defenses
from combat_tracker.engine.condition import Condition

from combat_tracker.engine.resources import Resource


class CharacterType(Enum):
    PC = "PC"
    NPC = "NPC"


@dataclass
class Character:

    # ---------- Loaded from JSON ----------

    name: str
    character_type: CharacterType

    strength: int
    speed: int

    intelligence: int
    willpower: int

    awareness: int
    presence: int

    movement: int

    health: Resource
    focus: Resource
    investiture: Resource

    defenses: Defenses
    skills: dict

    talents: list
    actions: list

    # ---------- Runtime ----------

    id: int = -1

    instance_number: int = 0
    display_name: str = ""

    conditions: list[Condition] = field(default_factory=list)

    turn_type: Optional[str] = None

    actions_remaining: int = 0

    reaction_available: bool = False

    acted_this_round: bool = False

    has_recovered: bool = False

    defeated: bool = False

    def start_turn(self):

        self.actions_remaining = 2 if self.turn_type == "fast" else 3
        self.reaction_available = True

    def spend_actions(self, amount):

        if amount > self.actions_remaining:
            return False

        self.actions_remaining -= amount
        return True

    def end_turn(self):

        self.acted_this_round = True

    def new_round(self):

        self.turn_type = None
        self.actions_remaining = 0
        self.reaction_available = False
        self.acted_this_round = False