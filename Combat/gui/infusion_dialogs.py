from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFrame,
    QLabel,
    QLineEdit,
    QScrollArea,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)


__all__ = [
    "AddInfusionDialog",
    "InfuseInvestitureDialog",
    "InfusionsReminderDialog",
]


class AddInfusionDialog(QDialog):
    """Prompts for a new infusion's name, surge, and starting investiture."""

    def __init__(self, surges, characters, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Infusion")
        self.resize(360, 260)

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Infusion Name"))
        self.name_edit = QLineEdit()
        layout.addWidget(self.name_edit)

        layout.addWidget(QLabel("Surge"))
        self.surge_combo = QComboBox()
        self.surge_combo.addItems(surges)
        layout.addWidget(self.surge_combo)

        layout.addWidget(QLabel("Investiture"))
        self.investiture_spin = QSpinBox()
        self.investiture_spin.setRange(1, 99)
        self.investiture_spin.setValue(1)
        layout.addWidget(self.investiture_spin)

        layout.addWidget(QLabel("Apply to Character"))
        self.character_combo = QComboBox()
        self.character_combo.addItem("No Character", None)
        for character in characters:
            self.character_combo.addItem(character.display_name, character.id)
        layout.addWidget(self.character_combo)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def infusion_name(self):
        return self.name_edit.text().strip()

    def infusion_surge(self):
        return self.surge_combo.currentText()

    def infusion_investiture(self):
        return self.investiture_spin.value()

    def recipient_id(self):
        return self.character_combo.currentData()


class InfuseInvestitureDialog(QDialog):
    """Prompts for an amount of investiture to add to an existing infusion."""

    def __init__(self, infusion, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Infuse {infusion.name}")
        self.resize(320, 160)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(f"Add investiture to {infusion.name}"))

        self.amount_spin = QSpinBox()
        self.amount_spin.setRange(1, 99)
        self.amount_spin.setValue(1)
        layout.addWidget(self.amount_spin)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def amount(self):
        return self.amount_spin.value()


class InfusionsReminderDialog(QDialog):
    """Reminds the user which infusions ran out of investiture this round."""

    def __init__(self, depleted_infusions, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Depleted Infusions")
        self.resize(420, 320)

        layout = QVBoxLayout(self)
        layout.addWidget(
            QLabel("The following infusions have run out of investiture:")
        )

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setAlignment(Qt.AlignTop)
        content_layout.setSpacing(8)

        for infusion in depleted_infusions:
            label = QLabel(f"{infusion.name} ({infusion.surge})")
            label.setStyleSheet("font-weight: 700;")
            content_layout.addWidget(label)

        scroll.setWidget(content)
        layout.addWidget(scroll)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok)
        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)
