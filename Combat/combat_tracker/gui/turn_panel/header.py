from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class TurnHeader(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(6)

        self.name_label = QLabel()
        self.name_label.setStyleSheet("font-size: 17px; font-weight: 700; color: #f7fbff;")

        self.turn_label = QLabel()
        self.turn_label.setStyleSheet("color: #dfeaf6;")

        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.turn_label)

    def set_character(self, character):
        if character is None:
            self.name_label.setText("")
            self.turn_label.setText("")
            return

        self.name_label.setText(character.display_name)
        self.turn_label.setText(
            f"{'Fast' if character.turn_type == 'fast' else 'Slow'} {character.character_type.value}s"
        )
