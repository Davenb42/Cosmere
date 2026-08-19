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
    "AddInfusedObjectDialog",
    "InfuseInvestitureDialog",
    "InfusedObjectsReminderDialog",
]


class AddInfusedObjectDialog(QDialog):
    """Prompts for a new infused object's name, surge, and starting investiture."""

    def __init__(self, surges, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Infused Object")
        self.resize(360, 260)

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Object Name"))
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

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def object_name(self):
        return self.name_edit.text().strip()

    def object_surge(self):
        return self.surge_combo.currentText()

    def object_investiture(self):
        return self.investiture_spin.value()


class InfuseInvestitureDialog(QDialog):
    """Prompts for an amount of investiture to add to an existing infused object."""

    def __init__(self, infused_object, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Infuse {infused_object.name}")
        self.resize(320, 160)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(f"Add investiture to {infused_object.name}"))

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


class InfusedObjectsReminderDialog(QDialog):
    """Reminds the user which infused objects ran out of investiture this round."""

    def __init__(self, depleted_objects, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Depleted Infused Objects")
        self.resize(420, 320)

        layout = QVBoxLayout(self)
        layout.addWidget(
            QLabel("The following infused objects have run out of investiture:")
        )

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setAlignment(Qt.AlignTop)
        content_layout.setSpacing(8)

        for infused_object in depleted_objects:
            label = QLabel(f"{infused_object.name} ({infused_object.surge})")
            label.setStyleSheet("font-weight: 700;")
            content_layout.addWidget(label)

        scroll.setWidget(content)
        layout.addWidget(scroll)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok)
        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)
