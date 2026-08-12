from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from combat_tracker.engine.character import CharacterType
from combat_tracker.gui import action_text
from combat_tracker.gui.panel_base import CombatPanel


__all__ = ["CombatView", "NoWheelSpinBox"]


class NoWheelSpinBox(QSpinBox):
    def wheelEvent(self, event):
        event.ignore()


class CombatView(QWidget):
    def __init__(self, combat_window):
        super().__init__()
        self.combat_window = combat_window
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
        self.party_layout.setAlignment(Qt.AlignTop)
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
        self.enemies_layout.setAlignment(Qt.AlignTop)
        self.enemies_scroll.setWidget(self.enemies_content)
        self.enemies_panel.content_layout.addWidget(self.enemies_scroll)

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
        for button in (
            self.spend1,
            self.spend2,
            self.spend3,
            self.end_turn,
            self.end_combat,
        ):
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

    def _build_combatant_row(self, character):
        row = QFrame()
        row.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        row.setMinimumHeight(52)
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

        spend_reaction = QPushButton("Spend Reaction")
        spend_reaction.setEnabled(character.reaction_available)
        if not character.reaction_available:
            spend_reaction.setText("Reaction Spent")
        spend_reaction.clicked.connect(
            lambda _, target=character: self.combat_window.spend_reaction(target)
        )
        h.addWidget(spend_reaction)

        for key in ("health", "focus", "investiture"):
            resource = getattr(character, key)
            spin = NoWheelSpinBox()
            spin.setRange(0, resource.maximum if hasattr(resource, "maximum") else 99)
            spin.setValue(resource.current)
            spin.valueChanged.connect(lambda value, res=resource: res.set(value))
            spin.setToolTip(key.title())
            h.addWidget(spin)

        return row

    def _build_ability_section(self, title, items, formatter):
        self.turn_bottom_layout.addWidget(self._make_subtitle_label(title))
        if items:
            for key, value in items.items():
                self.turn_bottom_layout.addWidget(
                    self._make_detail_label("\n".join(formatter(key, value)))
                )
        else:
            self.turn_bottom_layout.addWidget(self._make_detail_label("None"))

    def _refresh_header(self, state):
        self.encounter_label.setText(state.encounter.name)
        self.round_label.setText(f"Round {state.round_number}")

    def _refresh_rosters(self, state):
        self.clear_layout(self.party_layout)
        self.clear_layout(self.enemies_layout)

        for character in state.pcs:
            self.party_layout.addWidget(self._build_combatant_row(character))

        for character in state.npcs:
            self.enemies_layout.addWidget(self._build_combatant_row(character))

        self.party_layout.addStretch()
        self.enemies_layout.addStretch()

    def refresh_turn_only(self):
        state = self.combat_window.tracker.state
        active = self.combat_window.current_character

        self._refresh_header(state)

        self.clear_layout(self.turn_top_layout)
        self.clear_layout(self.turn_bottom_layout)

        if active is not None:
            name = QLabel(f"{active.display_name}")
            name.setStyleSheet("font-size: 24px; font-weight: 700; color: #f7fbff;")
            self.turn_top_layout.addWidget(name)

            group_label = f"{'Fast' if active.turn_type == 'fast' else 'Slow'} {active.character_type.value}s"
            group = QLabel(f"Turn Group: {group_label}")
            group.setStyleSheet("font-size: 14px; color: #dbe5f0;")
            self.turn_top_layout.addWidget(group)

            attributes = QLabel(
                "\n".join(
                    [
                        action_text.format_attribute_with_defense(
                            "Strength",
                            active.strength,
                            "Physical Def",
                            active.defenses.physical,
                            "Speed",
                            active.speed,
                        ),
                        action_text.format_attribute_with_defense(
                            "Intelligence",
                            active.intelligence,
                            "Cognitive Def",
                            active.defenses.cognitive,
                            "Willpower",
                            active.willpower,
                        ),
                        action_text.format_attribute_with_defense(
                            "Awareness",
                            active.awareness,
                            "Spiritual Def",
                            active.defenses.spiritual,
                            "Presence",
                            active.presence,
                        ),
                    ]
                )
            )
            attributes.setStyleSheet("font-size: 15px; font-weight: 600; color: #e6eff8;")
            self.turn_top_layout.addWidget(attributes)

            details = QLabel(
                f"HP {active.health.current}/{active.health.maximum}   "
                f"Focus {active.focus.current}/{active.focus.maximum}   "
                f"Investiture {active.investiture.current}/{active.investiture.maximum}   "
                f"Deflect {active.defenses.deflect}"
            )
            details.setStyleSheet("font-size: 16px; font-weight: 600; color: #edf3f8;")
            self.turn_top_layout.addWidget(details)

            actions = QLabel(
                "Actions Remaining: "
                f"{action_text.format_remaining_actions(active.actions_remaining)}"
            )
            actions.setStyleSheet("font-size: 15px; font-weight: 600; color: #e6eff8;")
            self.turn_top_layout.addWidget(actions)

            if active.conditions:
                conds = ", ".join(condition.name for condition in active.conditions)
            else:
                conds = "None"
            conditions_label = QLabel(f"Conditions: {conds}")
            conditions_label.setStyleSheet("font-size: 14px; color: #dbe5f0;")
            self.turn_top_layout.addWidget(conditions_label)

            if active.character_type == CharacterType.PC:
                self._build_ability_section("Talents", active.talents, action_text.format_talent_lines)
            else:
                self._build_ability_section("Features", active.talents, action_text.format_feature_lines)

            self._build_ability_section("Actions", active.actions, action_text.format_action_lines)

    def refresh(self):
        state = self.combat_window.tracker.state
        self._refresh_header(state)
        self._refresh_rosters(state)
        self.refresh_turn_only()
