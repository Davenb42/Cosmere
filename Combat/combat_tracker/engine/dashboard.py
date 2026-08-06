class Dashboard:

    @staticmethod
    def clear():
        return None

    def render(self, state):
        self.clear()

        lines = [
            "=" * 70,
            state.encounter.name,
            f"Round {state.round_number}",
            f"Phase : {state.phase}",
        ]

        if state.active_character:
            lines.append(f"Current Turn : {state.active_character.display_name}")

        lines.append("=" * 70)
        lines.append("")
        lines.append(
            f"{'ID':<4}"
            f"{'Character':<20}"
            f"{'HP':<10}"
            f"{'Focus':<10}"
            f"{'Inv.':<10}"
            f"{'PD':<10}"
            f"{'CD':<10}"
            f"{'SD':<10}"
            f"{'Def':<10}"
            f"Conditions"
        )
        lines.append("-" * 70)

        for c in state.combatants:
            conditions = ", ".join(condition.name for condition in c.conditions)
            if not conditions:
                conditions = "-"

            lines.append(
                f"{c.id:<4}"
                f"{c.display_name:<20}"
                f"{str(c.health):<10}"
                f"{str(c.focus):<10}"
                f"{str(c.investiture):<10}"
                f"{c.defenses.physical:<10}"
                f"{c.defenses.cognitive:<10}"
                f"{c.defenses.spiritual:<10}"
                f"{c.defenses.deflect:<10}"
                f"{conditions}"
            )

        lines.append("")
        lines.append("=" * 70)
        return "\n".join(lines)
