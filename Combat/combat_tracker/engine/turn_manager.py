class TurnManager:

    def choose_turn_types(self, state, fast_pcs=None, fast_npcs=None):
        self._choose_fast(state.pcs, "PC", fast_pcs)
        self._choose_fast(state.npcs, "NPC", fast_npcs)
        self.build_turn_order(state)

    def _choose_fast(self, characters, title, selected=None):
        for character in characters:
            character.turn_type = "slow"

        if selected is None:
            return []

        if isinstance(selected, str):
            selected = selected.strip()
            if not selected:
                return []
            selected = {int(x) for x in selected.split()}
        else:
            selected = {int(x) for x in selected}

        # GUI selection passes global character IDs. Older callers may pass
        # 1-based positions within the provided character list.
        id_matches = {
            character.id for character in characters
            if character.id in selected
        }

        if id_matches:
            for character in characters:
                if character.id in selected:
                    character.turn_type = "fast"
        else:
            for i, character in enumerate(characters, start=1):
                if i in selected:
                    character.turn_type = "fast"

        return [character for character in characters if character.turn_type == "fast"]

    def build_turn_order(self, state):
        state.turn_order = (
            [c for c in state.pcs if c.turn_type == "fast"] +
            [c for c in state.npcs if c.turn_type == "fast"] +
            [c for c in state.pcs if c.turn_type == "slow"] +
            [c for c in state.npcs if c.turn_type == "slow"]
        )

    def start_round(self, state):
        state.turn_order.clear()

        for character in state.combatants:
            character.new_round()

        self.choose_turn_types(state)
