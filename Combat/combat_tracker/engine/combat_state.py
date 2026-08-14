from dataclasses import dataclass, field
from typing import Optional

from combat_tracker.engine.character import Character, CharacterType
from combat_tracker.engine.encounter import Encounter
from combat_tracker.engine.infused_object import InfusedObject


@dataclass
class CombatState:

    encounter: Encounter

    round_number: int = 1

    phase: str = "Fast Turn Selection"

    active_character: Optional[Character] = None

    combat_over: bool = False

    turn_order: list[Character] = field(default_factory=list)

    infused_objects: list[InfusedObject] = field(default_factory=list)

    @property
    def combatants(self):
        return self.encounter.combatants

    @property
    def pcs(self):
        return [
            c for c in self.combatants
            if c.character_type == CharacterType.PC
        ]

    @property
    def npcs(self):
        return [
            c for c in self.combatants
            if c.character_type == CharacterType.NPC
        ]