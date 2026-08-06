class Selectors:

    @staticmethod
    def character(state, choice=None):
        if choice is None:
            return state.combatants[0] if state.combatants else None

        if isinstance(choice, str):
            choice = choice.strip()
            if not choice:
                return None
            try:
                choice = int(choice)
            except ValueError:
                return None

        if choice == 0:
            return None

        for character in state.combatants:
            if character.id == choice:
                return character

        return None
