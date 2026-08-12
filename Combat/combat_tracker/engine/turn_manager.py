class TurnManager:

    def choose_turn_types(self, state, fast_pcs=None, fast_npcs=None):
        self._choose_fast(state.pcs, fast_pcs)
        self._choose_fast(state.npcs, fast_npcs)
        self.build_turn_order(state)

    def _choose_fast(self, characters, selected=None):
        for character in characters:
            character.turn_type = "slow"

        if selected is None:
            return []

        selected = {int(x) for x in selected}

        for character in characters:
            if character.id in selected:
                character.turn_type = "fast"

        return [character for character in characters if character.turn_type == "fast"]

    def build_turn_order(self, state):
        state.turn_order = (
            [c for c in state.pcs if c.turn_type == "fast"] +
            [c for c in state.npcs if c.turn_type == "fast"] +
            [c for c in state.pcs if c.turn_type == "slow"] +
            [c for c in state.npcs if c.turn_type == "slow"]
        )
