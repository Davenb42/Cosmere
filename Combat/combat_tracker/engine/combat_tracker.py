from combat_tracker.engine.combat_state import CombatState
from combat_tracker.engine.turn_manager import TurnManager


class CombatTracker:

    def __init__(self, encounter):

        self.state = CombatState(encounter)

        self.turn_manager = TurnManager()
