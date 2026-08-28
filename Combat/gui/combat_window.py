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
from engine.infusion import Infusion
from gui.combat_view import CombatView
from gui.condition_dialogs import (
    ConditionReminderDialog,
    ConditionSelectionDialog,
)
from gui.infusion_dialogs import (
    AddInfusionDialog,
    InfuseInvestitureDialog,
    InfusionsReminderDialog,
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
            self.tracker.state.round_number += 1
            self.begin_round()
            return

        self.current_character = self.turn_order[self.turn_index]
        self.tracker.state.active_character = self.current_character
        self.current_character.start_turn()
        self.process_infusions_turn(self.current_character)
        self.view.refresh()
        self.show_condition_reminder(self.current_character)

    def toggle_active(self, character):
        if character is None:
            return

        character.excluded_from_combat = not character.excluded_from_combat
        self.view.refresh()

    def open_add_infusion(self):
        dialog = AddInfusionDialog(self.surges, self.tracker.state.combatants, self)
        if dialog.exec() != QDialog.Accepted:
            return

        name = dialog.infusion_name()
        if not name:
            return

        self.tracker.state.infusions.append(
            Infusion(
                name=name,
                surge=dialog.infusion_surge(),
                investiture=dialog.infusion_investiture(),
                created_round=self.tracker.state.round_number,
                creator_id=self.current_character.id if self.current_character else None,
                recipient_id=dialog.recipient_id(),
            )
        )
        self.view.refresh()

    def open_infusion(self, infusion):
        dialog = InfuseInvestitureDialog(infusion, self)
        if dialog.exec() != QDialog.Accepted:
            return

        infusion.investiture += dialog.amount()
        if infusion.investiture > 0:
            infusion.pending_removal = False
        self.view.refresh()

    def recall_infusion(self, infusion):
        if infusion in self.tracker.state.infusions:
            self.tracker.state.infusions.remove(infusion)
        self.view.refresh()

    def process_infusions_turn(self, character):
        state = self.tracker.state

        # Infusions that reached 0 last turn have stayed visible until now; clear them.
        state.infusions = [
            infusion
            for infusion in state.infusions
            if not infusion.pending_removal
        ]

        newly_depleted = []
        for infusion in state.infusions:
            if (
                infusion.creator_id == character.id
                and state.round_number > infusion.created_round
                and infusion.investiture > 0
            ):
                infusion.investiture -= 1
                if infusion.investiture <= 0:
                    infusion.pending_removal = True
                    newly_depleted.append(infusion)

        if newly_depleted:
            InfusionsReminderDialog(newly_depleted, self).exec()

    def show_condition_reminder(self, character):
        applied_infusions = [
            infusion
            for infusion in self.tracker.state.infusions
            if (
                infusion.recipient_id == character.id
                and infusion.investiture > 0
                and not infusion.pending_removal
            )
        ]
        if not character.conditions and not applied_infusions:
            return

        dialog = ConditionReminderDialog(
            character,
            self.all_conditions,
            applied_infusions,
            self,
        )
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
