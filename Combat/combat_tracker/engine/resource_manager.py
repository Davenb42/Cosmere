from combat_tracker.engine.selectors import Selectors
from combat_tracker.engine.utils import clear_screen, pause


class ResourceManager:

    def __init__(self):
        self.selectors = Selectors()

    def modify(self, state, character=None, choice=None):
        if character is None:
            character = self.selectors.character(state)

        if character is None:
            return {"character": None}

        if choice is None:
            return {
                "character": character.display_name,
                "resources": {
                    "health": str(character.health),
                    "focus": str(character.focus),
                    "investiture": str(character.investiture),
                },
                "options": ["Health", "Focus", "Investiture", "Back"],
            }

        if choice == "0":
            return {"action": "back", "character": character.display_name}

        if choice == "1":
            return self.change(character.health)

        if choice == "2":
            return self.change(character.focus)

        if choice == "3":
            return self.change(character.investiture)

        return {"character": character.display_name, "action": "unknown"}

    def change(self, resource, change=None):
        if change is None:
            return {
                "resource": getattr(resource, "name", resource.__class__.__name__),
                "current": getattr(resource, "current", resource),
                "max": getattr(resource, "maximum", getattr(resource, "current", resource)),
                "examples": ["+3", "-2", "=10"],
            }

        if not change:
            return {"success": False, "message": "No change supplied."}

        if change.startswith("+"):
            resource.current = min(resource.maximum, resource.current + int(change[1:]))
        elif change.startswith("-"):
            resource.current = max(0, resource.current - int(change[1:]))
        elif change.startswith("="):
            value = int(change[1:])
            resource.current = max(0, min(resource.maximum, value))
        else:
            return {"success": False, "message": "Invalid resource change format."}

        return {"success": True, "resource": getattr(resource, "name", resource.__class__.__name__), "current": resource.current}
