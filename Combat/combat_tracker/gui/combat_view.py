from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from combat_tracker.gui.panel_base import CombatPanel


class NoWheelSpinBox(QSpinBox):
    def wheelEvent(self, event):
        event.ignore()


class CombatView(QWidget):
    def __init__(self, combat_window):
        super().__init__()
        self.combat_window = combat_window
        self.resource_controls = {}
        self.setStyleSheet(
            """
            QWidget {
                background: #141a20;
                color: #edf3f8;
                font-family: 'Segoe UI', sans-serif;
            }
            QLabel {
                color: #edf3f8;
            }
            QPushButton {
                background: #2a313a;
                border: 1px solid #5f6a77;
                border-radius: 6px;
                color: #edf3f8;
                padding: 8px 12px;
                text-align: center;
            }
            QPushButton:hover {
                background: #36414d;
            }
            QPushButton:pressed {
                background: #202932;
            }
            QSpinBox {
                background: #202932;
                color: #edf3f8;
                border: 1px solid #576777;
                border-radius: 4px;
                padding: 4px;
            }
            """
        )

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.root = QVBoxLayout(self)
        self.root.setContentsMargins(18, 12, 18, 18)
        self.root.setSpacing(14)
        self.root.setStretch(0, 0)
        self.root.setStretch(1, 1)

        self.header = QFrame()
        self.header.setStyleSheet(
            "QFrame { background: #1d2229; border: 1px solid #4d5865; border-radius: 10px; }"
        )
        self.header.setFixedHeight(64)
        header_layout = QHBoxLayout(self.header)
        header_layout.setContentsMargins(16, 10, 16, 10)

        self.encounter_label = QLabel("Encounter")
        self.encounter_label.setStyleSheet("font-size: 24px; font-weight: 700; color: #f3f7fb;")
        self.encounter_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.encounter_label.setMaximumWidth(620)
        self.round_label = QLabel("Round 1")
        self.round_label.setStyleSheet("font-size: 18px; font-weight: 700; color: #d9e4f0;")
        self.round_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.round_label.setMinimumWidth(120)

        header_layout.addWidget(self.encounter_label)
        header_layout.addStretch()
        header_layout.addWidget(self.round_label)
        self.root.addWidget(self.header)

        self.body = QGridLayout()
        self.body.setContentsMargins(0, 0, 0, 0)
        self.body.setColumnStretch(0, 1)
        self.body.setColumnStretch(1, 2)
        self.body.setRowStretch(0, 1)
        self.body.setRowStretch(1, 1)
        self.body.setRowStretch(2, 0)
        self.body.setHorizontalSpacing(14)
        self.body.setVerticalSpacing(14)

        self.party_panel = CombatPanel("Party")
        self.turn_panel = CombatPanel("CURRENT TURN")
        self.enemies_panel = CombatPanel("Enemies")
        self.log_panel = CombatPanel("Combat Log")

        for panel in (self.party_panel, self.enemies_panel):
            panel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.turn_panel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.turn_content = QWidget()
        self.turn_layout = QVBoxLayout(self.turn_content)
        self.turn_layout.setContentsMargins(0, 0, 0, 0)
        self.turn_layout.setSpacing(10)
        self.turn_layout.setAlignment(Qt.AlignTop)

        self.turn_top = QWidget()
        self.turn_top_layout = QVBoxLayout(self.turn_top)
        self.turn_top_layout.setContentsMargins(10, 10, 10, 10)
        self.turn_top_layout.setSpacing(10)
        self.turn_top_layout.setAlignment(Qt.AlignTop)

        self.turn_bottom = QWidget()
        self.turn_bottom_layout = QVBoxLayout(self.turn_bottom)
        self.turn_bottom_layout.setContentsMargins(10, 0, 10, 10)
        self.turn_bottom_layout.setSpacing(10)
        self.turn_bottom_layout.setAlignment(Qt.AlignTop)

        self.turn_layout.addWidget(self.turn_top)
        self.turn_layout.addWidget(self.turn_bottom)

        self.turn_split = QWidget()
        self.turn_split_layout = QHBoxLayout(self.turn_split)
        self.turn_split_layout.setContentsMargins(0, 0, 0, 0)
        self.turn_split_layout.setSpacing(12)
        self.turn_split_layout.setAlignment(Qt.AlignTop)
        self.turn_split_layout.addWidget(self.turn_content, 1)

        self.actions_container = QWidget()
        self.actions_container.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.actions_layout = QVBoxLayout(self.actions_container)
        self.actions_layout.setContentsMargins(10, 10, 10, 10)
        self.actions_layout.setSpacing(10)
        self.actions_layout.setAlignment(Qt.AlignTop)
        self.turn_split_layout.addWidget(self.actions_container, 0)

        self.turn_scroll = QScrollArea()
        self.turn_scroll.setWidgetResizable(True)
        self.turn_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.turn_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.turn_scroll.setFrameShape(QFrame.NoFrame)
        self.turn_scroll.setWidget(self.turn_split)

        self.turn_panel.content_layout.addWidget(self.turn_scroll)

        self.party_scroll = QScrollArea()
        self.party_scroll.setWidgetResizable(True)
        self.party_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.party_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.party_scroll.setFrameShape(QFrame.NoFrame)

        self.party_content = QWidget()
        self.party_layout = QVBoxLayout(self.party_content)
        self.party_layout.setSpacing(8)
        self.party_scroll.setWidget(self.party_content)
        self.party_panel.content_layout.addWidget(self.party_scroll)

        self.enemies_scroll = QScrollArea()
        self.enemies_scroll.setWidgetResizable(True)
        self.enemies_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.enemies_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.enemies_scroll.setFrameShape(QFrame.NoFrame)

        self.enemies_content = QWidget()
        self.enemies_layout = QVBoxLayout(self.enemies_content)
        self.enemies_layout.setSpacing(8)
        self.enemies_scroll.setWidget(self.enemies_content)
        self.enemies_panel.content_layout.addWidget(self.enemies_scroll)

        self.log_view = QPlainTextEdit()
        self.log_view.setReadOnly(True)
        self.log_view.setStyleSheet(
            """
            QPlainTextEdit {
                background: #1b232b;
                color: #edf3f8;
                border: 1px solid #4d5865;
                border-radius: 8px;
                padding: 8px;
            }
            """
        )
        # Kept as dead code for future log reintroduction.

        self.body.addWidget(self.party_panel, 0, 0)
        self.body.addWidget(self.turn_panel, 0, 1, 2, 1)
        self.body.addWidget(self.enemies_panel, 1, 0)

        self.root.addLayout(self.body, 1)

        self._build_action_buttons()

    def _build_action_buttons(self):
        self.spend1 = QPushButton("Spend 1")
        self.spend2 = QPushButton("Spend 2")
        self.spend3 = QPushButton("Spend 3")
        self.end_turn = QPushButton("End Turn")
        self.end_combat = QPushButton("End Combat")
        for button in (self.spend1, self.spend2, self.spend3, self.end_turn, self.end_combat):
            self.actions_layout.addWidget(button)
        self.actions_layout.addStretch()
        self.spend1.clicked.connect(lambda: self.combat_window.spend_action(1))
        self.spend2.clicked.connect(lambda: self.combat_window.spend_action(2))
        self.spend3.clicked.connect(lambda: self.combat_window.spend_action(3))
        self.end_turn.clicked.connect(self.combat_window.end_turn)
        self.end_combat.clicked.connect(self.combat_window.end_combat)

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def toggle_log(self):
        # Dead code retained for future restoration of the combat log view.
        return

    @staticmethod
    def _is_blank(value):
        if value is None:
            return True
        if isinstance(value, str):
            return not value.strip()
        if isinstance(value, (list, tuple, dict, set)):
            return len(value) == 0
        return False

    @staticmethod
    def _normalize_action_name(name):
        text = str(name).strip()
        if text.lower().startswith("strike "):
            return text[7:]
        return text

    @staticmethod
    def _get_action_value(action, *keys):
        if not isinstance(action, dict):
            return None

        lowered = {
            str(key).strip().lower(): value
            for key, value in action.items()
        }
        for key in keys:
            value = lowered.get(str(key).strip().lower())
            if value is not None:
                return value
        return None

    def _action_symbol(self, action):
        cost = self._get_action_value(action, "action cost", "action_cost", "cost")
        if self._is_blank(cost):
            return "►"

        value = str(cost).strip().lower()
        if value in {"1", "1 action"}:
            return "►"
        if value in {"2", "2 actions"}:
            return "►►"
        if value in {"3", "3 actions"}:
            return "►►►"
        if "free" in value:
            return "▷"
        if "reaction" in value:
            return "↩"
        if "special" in value:
            return "★"
        if "always" in value:
            return "∞"

        return "►"

    def _format_action_lines(self, action_name, action_data):
        lines = [f"{self._action_symbol(action_data)} {self._normalize_action_name(action_name)}"]

        aoe = self._get_action_value(action_data, "aoe", "target")
        attack = self._get_action_value(action_data, "attack")
        action_range = self._get_action_value(action_data, "range")
        saving_throw = self._get_action_value(action_data, "saving throw")
        damage = self._get_action_value(action_data, "damage")
        graze = self._get_action_value(action_data, "graze")
        hit = self._get_action_value(action_data, "hit")
        duration = self._get_action_value(action_data, "duration")
        description = self._get_action_value(action_data, "description")
        focus_cost = self._get_action_value(action_data, "focus cost")

        summary = []
        if not self._is_blank(aoe):
            summary.append(str(aoe).strip())

        if not self._is_blank(attack):
            attack_text = str(attack).strip()
            if "d20" not in attack_text.lower() and (
                attack_text.startswith("+")
                or attack_text.startswith("-")
                or attack_text.isdigit()
            ):
                attack_text = f"1d20{attack_text}"
            attack_text = f"{attack_text} vs Physical Def."
            summary.append(attack_text)

        if not self._is_blank(action_range):
            summary.append(f"({str(action_range).strip()})")

        if summary:
            lines.append(" ".join(summary))

        if not self._is_blank(saving_throw):
            lines.append(str(saving_throw).strip())

        if not self._is_blank(graze):
            lines.append(f"Graze: {str(graze).strip()}")

        if not self._is_blank(hit):
            lines.append(f"Hit: {str(hit).strip()}")

        if not self._is_blank(damage):
            lines.append(f"Damage: {str(damage).strip()}")

        if not self._is_blank(duration):
            lines.append(f"Duration: {str(duration).strip()}")

        if not self._is_blank(focus_cost):
            focus_text = str(focus_cost).strip()
            if focus_text not in {"0", "0.0"}:
                lines.append(f"Focus Cost: {focus_text}")

        if not self._is_blank(description):
            lines.append(str(description).strip())

        return lines

    def _format_talent_lines(self, talent_name, talent_data):
        lines = [f"{self._action_symbol(talent_data)} {str(talent_name).strip()}"]

        description = self._get_action_value(talent_data, "description")
        if not self._is_blank(description):
            lines.append(str(description).strip())
            return lines

        if isinstance(talent_data, dict):
            ignored_keys = {"action cost", "action_cost", "cost"}
            for key, value in talent_data.items():
                key_text = str(key).strip()
                if key_text.lower() in ignored_keys or self._is_blank(value):
                    continue
                lines.append(str(value).strip())

        return lines

    def _format_feature_lines(self, feature_name, feature_data):
        lines = [str(feature_name).strip()]

        if isinstance(feature_data, dict):
            description = self._get_action_value(feature_data, "description")
            if not self._is_blank(description):
                lines.append(str(description).strip())
            else:
                for value in feature_data.values():
                    if self._is_blank(value):
                        continue
                    lines.append(str(value).strip())
        elif not self._is_blank(feature_data):
            lines.append(str(feature_data).strip())

        return lines

    @staticmethod
    def _make_subtitle_label(text):
        label = QLabel(text)
        label.setStyleSheet("font-size: 18px; font-weight: 700; color: #e6eff8;")
        return label

    @staticmethod
    def _make_detail_label(text):
        label = QLabel(text)
        label.setWordWrap(True)
        label.setAlignment(Qt.AlignTop)
        label.setStyleSheet("font-size: 14px; color: #edf3f8;")
        return label

    @staticmethod
    def _format_remaining_actions(actions_remaining):
        try:
            value = int(actions_remaining)
        except (TypeError, ValueError):
            return "None"

        if value <= 0:
            return "None"

        return "►" * value

    def refresh(self):
        state = self.combat_window.tracker.state
        active = self.combat_window.current_character

        self.encounter_label.setText(state.encounter.name)
        self.round_label.setText(f"Round {state.round_number}")

        self.clear_layout(self.party_layout)
        self.clear_layout(self.turn_top_layout)
        self.clear_layout(self.turn_bottom_layout)
        self.clear_layout(self.enemies_layout)

        for character in state.pcs:
            row = QFrame()
            row.setStyleSheet(
                "QFrame { background: #1f2a35; border: 1px solid #46586a; border-radius: 8px; }"
            )
            h = QHBoxLayout(row)
            h.setContentsMargins(10, 8, 10, 8)
            h.setSpacing(10)

            label = QLabel(f"{character.display_name}")
            label.setStyleSheet("font-weight: 600;")
            h.addWidget(label)

            deflect_label = QLabel(f"Deflect {character.defenses.deflect}")
            deflect_label.setStyleSheet("color: #d5effd; font-weight: 600;")
            h.addWidget(deflect_label)

            for key in ("health", "focus", "investiture"):
                resource = getattr(character, key)
                spin = NoWheelSpinBox()
                spin.setRange(0, resource.maximum if hasattr(resource, "maximum") else 99)
                spin.setValue(resource.current)
                spin.valueChanged.connect(lambda value, res=resource: res.set(value))
                spin.setToolTip(key.title())
                h.addWidget(spin)

            self.party_layout.addWidget(row)

        for character in state.npcs:
            row = QFrame()
            row.setStyleSheet(
                "QFrame { background: #1f2a35; border: 1px solid #46586a; border-radius: 8px; }"
            )
            h = QHBoxLayout(row)
            h.setContentsMargins(10, 8, 10, 8)
            h.setSpacing(10)

            label = QLabel(f"{character.display_name}")
            label.setStyleSheet("font-weight: 600;")
            h.addWidget(label)

            deflect_label = QLabel(f"Deflect {character.defenses.deflect}")
            deflect_label.setStyleSheet("color: #d5effd; font-weight: 600;")
            h.addWidget(deflect_label)

            for key in ("health", "focus", "investiture"):
                resource = getattr(character, key)
                spin = NoWheelSpinBox()
                spin.setRange(0, resource.maximum if hasattr(resource, "maximum") else 99)
                spin.setValue(resource.current)
                spin.valueChanged.connect(lambda value, res=resource: res.set(value))
                spin.setToolTip(key.title())
                h.addWidget(spin)

            self.enemies_layout.addWidget(row)

        if active is not None:
            name = QLabel(f"{active.display_name}")
            name.setStyleSheet("font-size: 24px; font-weight: 700; color: #f7fbff;")
            self.turn_top_layout.addWidget(name)

            group_label = f"{'Fast' if active.turn_type == 'fast' else 'Slow'} {active.character_type.value}s"
            group = QLabel(f"Turn Group: {group_label}")
            group.setStyleSheet("font-size: 14px; color: #dbe5f0;")
            self.turn_top_layout.addWidget(group)

            details = QLabel(
                f"HP {active.health.current}/{active.health.maximum}   "
                f"Focus {active.focus.current}/{active.focus.maximum}   "
                f"Investiture {active.investiture.current}/{active.investiture.maximum}   "
                f"Deflect {active.defenses.deflect}"
            )
            details.setStyleSheet("font-size: 16px; font-weight: 600; color: #edf3f8;")
            self.turn_top_layout.addWidget(details)

            actions = QLabel(f"Actions Remaining: {self._format_remaining_actions(active.actions_remaining)}")
            actions.setStyleSheet("font-size: 15px; font-weight: 600; color: #e6eff8;")
            self.turn_top_layout.addWidget(actions)

            if active.conditions:
                conds = ", ".join(condition.name for condition in active.conditions)
            else:
                conds = "None"
            conditions_label = QLabel(f"Conditions: {conds}")
            conditions_label.setStyleSheet("font-size: 14px; color: #dbe5f0;")
            self.turn_top_layout.addWidget(conditions_label)

            if active.character_type.value == "PC":
                self.turn_bottom_layout.addWidget(self._make_subtitle_label("Talents"))
                if active.talents:
                    for key, value in active.talents.items():
                        self.turn_bottom_layout.addWidget(
                            self._make_detail_label("\n".join(self._format_talent_lines(key, value)))
                        )
                else:
                    self.turn_bottom_layout.addWidget(self._make_detail_label("None"))

                self.turn_bottom_layout.addWidget(self._make_subtitle_label("Actions"))
                if active.actions:
                    for key, value in active.actions.items():
                        self.turn_bottom_layout.addWidget(
                            self._make_detail_label("\n".join(self._format_action_lines(key, value)))
                        )
                else:
                    self.turn_bottom_layout.addWidget(self._make_detail_label("None"))
            else:
                self.turn_bottom_layout.addWidget(self._make_subtitle_label("Features"))
                if active.talents:
                    for key, value in active.talents.items():
                        self.turn_bottom_layout.addWidget(
                            self._make_detail_label("\n".join(self._format_feature_lines(key, value)))
                        )
                else:
                    self.turn_bottom_layout.addWidget(self._make_detail_label("None"))

                self.turn_bottom_layout.addWidget(self._make_subtitle_label("Actions"))
                if active.actions:
                    for key, value in active.actions.items():
                        self.turn_bottom_layout.addWidget(
                            self._make_detail_label("\n".join(self._format_action_lines(key, value)))
                        )
                else:
                    self.turn_bottom_layout.addWidget(self._make_detail_label("None"))

        self.log_view.setPlainText("\n".join(self.combat_window.log_entries))
        self.log_view.verticalScrollBar().setValue(self.log_view.verticalScrollBar().maximum())
        self.enemies_panel.layout.addStretch()

    def set_round_selection(self):
        self.encounter_label.setText(self.combat_window.tracker.state.encounter.name)
