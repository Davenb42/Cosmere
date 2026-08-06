from combat_tracker.engine.combat_state import CombatState
from combat_tracker.engine.dashboard import Dashboard
from combat_tracker.engine.turn_manager import TurnManager
from combat_tracker.engine.utils import clear_screen, pause
from combat_tracker.engine.selectors import Selectors
from combat_tracker.engine.resource_manager import ResourceManager
from combat_tracker.engine.condition_manager import ConditionManager

class CombatTracker:

    def __init__(self, encounter):

        self.state = CombatState(encounter)

        self.dashboard = Dashboard()

        self.turn_manager = TurnManager()

        self.selectors = Selectors()

        self.resource_manager = ResourceManager()

        self.condition_manager = ConditionManager()

    def run(self):

        while not self.state.combat_over:

            self.turn_manager.start_round(self.state)

            self.run_round()

            self.state.round_number += 1

    def run_round(self):

        for character in self.state.turn_order:

            self.run_turn(character)

        clear_screen()

    def get_turn_state(self, character):
        return {
            "character": character.display_name,
            "actions_remaining": character.actions_remaining,
            "reaction_available": character.reaction_available,
            "options": [
                "Spend Action",
                "Resources",
                "Conditions",
                "Select Character",
                "End Turn",
            ],
        }

    def run_turn(self, character, choice=None):
        self.state.active_character = character
        character.start_turn()

        if choice is None:
            return self.get_turn_state(character)

        if choice == "1":
            return self.spend_actions(character)

        if choice == "2":
            return self.resource_manager.modify(self.state, character=character)

        if choice == "3":
            return self.condition_manager.manage(self.state, character=character)

        if choice == "4":
            return self.inspect_character(character)

        if choice == "5":
            character.end_turn()
            return {"ended_turn": True, "character": character.display_name}

        return self.get_turn_state(character)

    def spend_actions(self, character, amount=None):
        if amount is None:
            return {
                "action": "spend_actions",
                "character": character.display_name,
                "prompt": "Actions to spend",
            }

        amount_text = str(amount).strip()
        if not amount_text.isdigit():
            return {"success": False, "message": "Invalid action amount."}

        amount = int(amount_text)
        if character.spend_actions(amount):
            return {"success": True, "message": "Actions spent.", "amount": amount}

        return {"success": False, "message": "Not enough actions.", "amount": amount}

    def inspect_character(self, character=None):
        if character is None:
            character = self.selectors.character(self.state)

        if character is None:
            return {"character": None}

        return {
            "display_name": character.display_name,
            "health": character.health,
            "focus": character.focus,
            "investiture": character.investiture,
            "defenses": {
                "physical": character.defenses.physical,
                "cognitive": character.defenses.cognitive,
                "spiritual": character.defenses.spiritual,
                "deflect": character.defenses.deflect,
            },
            "conditions": [str(condition) for condition in character.conditions],
        }