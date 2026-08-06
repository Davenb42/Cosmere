from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class TurnResources(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(6)

        self.label = QLabel()
        self.label.setWordWrap(True)
        self.label.setStyleSheet("color: #edf3f8;")
        self.layout.addWidget(self.label)

    def set_character(self, character):
        if character is None:
            self.label.setText("")
            return

        self.label.setText(
            f"HP {character.health.current}/{character.health.maximum}   "
            f"Focus {character.focus.current}/{character.focus.maximum}   "
            f"Investiture {character.investiture.current}/{character.investiture.maximum}   "
            f"Deflect {character.defenses.deflect}   "
            f"Actions Remaining: {character.actions_remaining}"
        )
