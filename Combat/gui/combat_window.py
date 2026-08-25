from pathlib import Path

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QLabel,
    QMainWindow,
    QMessageBox,
    QVBoxLayout,
)

from engine.character import CharacterType
from engine.combat_tracker import CombatTracker
from engine.encounter_loader import EncounterLoader
from engine.infused_object import InfusedObject
from gui.combat_view import CombatView
from gui.condition_dialogs import (
    ConditionReminderDialog,
    ConditionSelectionDialog,
)
from gui.infused_object_dialogs import (
    AddInfusedObjectDialog,
    InfuseInvestitureDialog,
    InfusedObjectsReminderDialog,
)


class TurnSelectionDialog(QDialog):
    def __init__(self, state, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Round Turn Selection")
        self.resize(500, 420)
        self.checkboxes = []

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Select who is taking a fast turn this round."))

        for character in state.combatants:
            checkbox = QCheckBox(f"{character.display_name} ({character.character_type.value})")
            self.checkboxes.append((character, checkbox))
            layout.addWidget(checkbox)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def selected_fast(self, character_type):
        fast = []
        for character, checkbox in self.checkboxes:
            if checkbox.isChecked() and character.character_type == character_type:
                fast.append(character)
        return fast


class CombatWindow(QMainWindow):
    closed = Signal()

    def __init__(self, campaign_root, encounter_dir):
        super().__init__()
        self.setWindowTitle("Combat Tracker")
        self.resize(1200, 720)
        self.setWindowState(Qt.WindowMaximized)

        self.campaign_root = Path(campaign_root)
        self.encounter_dir = Path(encounter_dir)
        self.loader = EncounterLoader(str(self.campaign_root))
        self.tracker = CombatTracker(self.loader.load(self.encounter_dir))
        self.all_conditions = self.loader.load_conditions()
        self.surges = self.loader.load_surges()
        self.turn_order = []
        self.current_character = None
        self.turn_index = 0

        self.view = CombatView(self)
        self.setCentralWidget(self.view)

        self.begin_round()

    def begin_round(self):
        if self.tracker.state.combat_over:
            return

        for character in self.tracker.state.combatants:
            character.new_round()

        dialog = TurnSelectionDialog(self.tracker.state, self)
        if dialog.exec() != QDialog.Accepted:
            self.close()
            return

        fast_pcs = dialog.selected_fast(CharacterType.PC)
        fast_npcs = dialog.selected_fast(CharacterType.NPC)

        self.tracker.turn_manager.choose_turn_types(
            self.tracker.state,
            fast_pcs=[character.id for character in fast_pcs],
            fast_npcs=[character.id for character in fast_npcs],
        )
        self.turn_order = list(self.tracker.state.turn_order)
        self.turn_index = 0
        self.advance_turn()

    def advance_turn(self):
        if not self.turn_order:
            self.current_character = None
            self.view.refresh()
            return

        while (
            self.turn_index < len(self.turn_order)
            and self.turn_order[self.turn_index].excluded_from_combat
        ):
            self.turn_index += 1

        if self.turn_index >= len(self.turn_order):
            self.process_infused_objects_round_end()
            self.tracker.state.round_number += 1
            self.begin_round()
            return

        self.current_character = self.turn_order[self.turn_index]
        self.tracker.state.active_character = self.current_character
        self.current_character.start_turn()
        self.view.refresh()
        self.show_condition_reminder(self.current_character)

    def toggle_active(self, character):
        if character is None:
            return

        character.excluded_from_combat = not character.excluded_from_combat
        self.view.refresh()

    def open_add_infused_object(self):
        dialog = AddInfusedObjectDialog(self.surges, self)
        if dialog.exec() != QDialog.Accepted:
            return

        name = dialog.object_name()
        if not name:
            return

        self.tracker.state.infused_objects.append(
            InfusedObject(
                name=name,
                surge=dialog.object_surge(),
                investiture=dialog.object_investiture(),
                created_round=self.tracker.state.round_number,
            )
        )
        self.view.refresh()

    def open_infuse_object(self, infused_object):
        dialog = InfuseInvestitureDialog(infused_object, self)
        if dialog.exec() != QDialog.Accepted:
            return

        infused_object.investiture += dialog.amount()
        if infused_object.investiture > 0:
            infused_object.zero_at_round = None
        self.view.refresh()

    def recall_infused_object(self, infused_object):
        if infused_object in self.tracker.state.infused_objects:
            self.tracker.state.infused_objects.remove(infused_object)
        self.view.refresh()

    def process_infused_objects_round_end(self):
        state = self.tracker.state
        ending_round = state.round_number

        state.infused_objects = [
            infused_object
            for infused_object in state.infused_objects
            if infused_object.zero_at_round is None
            or ending_round <= infused_object.zero_at_round
        ]

        for infused_object in state.infused_objects:
            if (
                ending_round >= infused_object.created_round + 1
                and infused_object.investiture > 0
            ):
                infused_object.investiture -= 1
                if infused_object.investiture == 0:
                    infused_object.zero_at_round = ending_round

        depleted = [
            infused_object
            for infused_object in state.infused_objects
            if infused_object.investiture <= 0
        ]
        if depleted:
            InfusedObjectsReminderDialog(depleted, self).exec()

    def show_condition_reminder(self, character):
        if not character.conditions:
            return

        dialog = ConditionReminderDialog(character, self.all_conditions, self)
        dialog.exec()

    def open_condition_editor(self, character):
        if character is None:
            return

        dialog = ConditionSelectionDialog(character, self.all_conditions, self)
        if dialog.exec() == QDialog.Accepted:
            character.conditions = dialog.selected_conditions()
            self.view.refresh()

    def spend_action(self, amount):
        if self.current_character is None:
            return

        self.current_character.spend_actions(amount)
        self.view.refresh_turn_only()

    def spend_reaction(self, character):
        if character is None:
            return

        character.reaction_available = False
        self.view.refresh()

    def regain_reaction(self, character):
        if character is None:
            return

        dialog = QMessageBox(self)
        dialog.setWindowTitle("Regain Reaction")
        dialog.setText("Do you want this character to regain a reaction?")
        accept_button = dialog.addButton("Accept", QMessageBox.AcceptRole)
        dialog.addButton("Cancel", QMessageBox.RejectRole)
        dialog.exec()

        if dialog.clickedButton() == accept_button:
            character.reaction_available = True
            self.view.refresh()

    def end_turn(self):
        if self.current_character is None:
            return

        self.current_character.end_turn()
        self.turn_index += 1
        self.advance_turn()

    def end_combat(self):
        self.tracker.state.combat_over = True
        self.view.refresh()
        self.close()

    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)
