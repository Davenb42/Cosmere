from pathlib import Path
import json

from combat_tracker.engine.condition import Condition
from combat_tracker.engine.selectors import Selectors
from combat_tracker.engine.utils import clear_screen, pause


class ConditionManager:

    def __init__(self, conditions_file=None):

        self.selectors = Selectors()

        if conditions_file is None:
            project_root = Path(__file__).resolve().parent.parent
            conditions_file = project_root / "Campaign" / "Conditions" / "conditions.json"

        with open(conditions_file, "r", encoding="utf-8") as f:
            self.conditions = json.load(f)

    def manage(self, state, character=None, choice=None):
        if character is None:
            character = self.selectors.character(state)

        if character is None:
            return {"character": None}

        if choice is None:
            return {
                "character": character.display_name,
                "conditions": [condition.name for condition in character.conditions],
                "options": ["Add", "Remove", "Back"],
            }

        if choice == "0":
            return {"action": "back", "character": character.display_name}

        if choice == "a":
            return self.add_condition(character)

        if choice == "r":
            return self.remove_condition(character)

        return {"character": character.display_name, "action": "unknown"}

    def add_condition(self, character, choice=None):
        names = sorted(self.conditions.keys())
        if choice is None:
            return {
                "character": character.display_name,
                "available_conditions": names,
                "prompt": "Choose a condition to add",
            }

        if not str(choice).strip().isdigit():
            return {"success": False, "message": "Invalid condition selection."}

        index = int(str(choice).strip())
        if not (1 <= index <= len(names)):
            return {"success": False, "message": "Condition index out of range."}

        character.conditions.append(Condition(name=names[index - 1]))
        return {"success": True, "message": "Condition added.", "condition": names[index - 1]}

    def remove_condition(self, character, choice=None):
        if not character.conditions:
            return {"success": False, "message": "Character has no conditions."}

        if choice is None:
            return {
                "character": character.display_name,
                "conditions": [condition.name for condition in character.conditions],
                "prompt": "Choose a condition to remove",
            }

        if not str(choice).strip().isdigit():
            return {"success": False, "message": "Invalid condition selection."}

        index = int(str(choice).strip())
        if not (1 <= index <= len(character.conditions)):
            return {"success": False, "message": "Condition index out of range."}

        removed = character.conditions.pop(index - 1)
        return {"success": True, "message": "Condition removed.", "condition": removed.name}
