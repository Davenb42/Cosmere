from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QFrame,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from combat_tracker.engine.condition import Condition


__all__ = ["ConditionSelectionDialog", "ConditionReminderDialog"]


def _make_scrollable_content():
    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    scroll.setFrameShape(QFrame.NoFrame)

    content = QWidget()
    content_layout = QVBoxLayout(content)
    content_layout.setAlignment(Qt.AlignTop)
    content_layout.setSpacing(12)

    scroll.setWidget(content)
    return scroll, content_layout


class ConditionSelectionDialog(QDialog):
    """Lets the user toggle which conditions apply to a character."""

    def __init__(self, character, all_conditions, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Set Conditions - {character.display_name}")
        self.resize(520, 600)

        active_names = {condition.name for condition in character.conditions}
        self.checkboxes = []

        layout = QVBoxLayout(self)

        scroll, content_layout = _make_scrollable_content()

        for name, description in all_conditions.items():
            checkbox = QCheckBox(name)
            checkbox.setChecked(name in active_names)
            checkbox.setStyleSheet("font-weight: 700;")
            content_layout.addWidget(checkbox)

            desc_label = QLabel(description)
            desc_label.setWordWrap(True)
            content_layout.addWidget(desc_label)

            self.checkboxes.append((name, checkbox))

        layout.addWidget(scroll)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def selected_conditions(self):
        return [
            Condition(name=name)
            for name, checkbox in self.checkboxes
            if checkbox.isChecked()
        ]


class ConditionReminderDialog(QDialog):
    """Reminds the user which conditions the active character has."""

    def __init__(self, character, all_conditions, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Active Conditions - {character.display_name}")
        self.resize(480, 400)

        layout = QVBoxLayout(self)
        layout.addWidget(
            QLabel(f"{character.display_name} has the following conditions:")
        )

        scroll, content_layout = _make_scrollable_content()

        for condition in character.conditions:
            name_label = QLabel(condition.name)
            name_label.setStyleSheet("font-weight: 700;")
            content_layout.addWidget(name_label)

            description = all_conditions.get(condition.name, "")
            if description:
                desc_label = QLabel(description)
                desc_label.setWordWrap(True)
                content_layout.addWidget(desc_label)

        layout.addWidget(scroll)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok)
        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)
