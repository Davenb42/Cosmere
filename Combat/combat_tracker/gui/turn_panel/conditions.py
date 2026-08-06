from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class TurnConditions(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.label = QLabel()
        self.label.setWordWrap(True)
        self.label.setStyleSheet("color: #edf3f8;")
        self.layout.addWidget(self.label)

    def set_character(self, character):
        if character is None:
            self.label.setText("")
            return

        if character.conditions:
            conds = ", ".join(condition.name for condition in character.conditions)
        else:
            conds = "None"
        self.label.setText(f"Conditions: {conds}")
