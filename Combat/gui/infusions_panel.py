from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from gui.panel_base import CombatPanel


__all__ = ["InfusionsPanel"]


class InfusionsPanel(CombatPanel):
    """Panel listing infusions, kept separate from combat_view.py."""

    def __init__(self, combat_window, parent=None):
        super().__init__("Infusions", parent)
        self.combat_window = combat_window
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll.setFrameShape(QFrame.NoFrame)

        self.list_content = QWidget()
        self.list_layout = QVBoxLayout(self.list_content)
        self.list_layout.setSpacing(8)
        self.list_layout.setAlignment(Qt.AlignTop)
        self.scroll.setWidget(self.list_content)

        self.content_layout.addWidget(self.scroll)

        self.add_button = QPushButton("Add Infusion")
        self.add_button.clicked.connect(self.combat_window.open_add_infusion)
        self.content_layout.addWidget(self.add_button)

    def _clear_list(self):
        while self.list_layout.count():
            item = self.list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def _build_infusion_row(self, infusion):
        row = QFrame()
        row.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        row.setMinimumHeight(52)
        depleted = infusion.investiture <= 0
        row.setStyleSheet(
            "QFrame { background: #14181d; border: 1px solid #333a42; border-radius: 8px; }"
            if depleted
            else "QFrame { background: #1f2a35; border: 1px solid #46586a; border-radius: 8px; }"
        )

        h = QHBoxLayout(row)
        h.setContentsMargins(10, 8, 10, 8)
        h.setSpacing(10)

        label = QLabel(f"{infusion.name} ({infusion.surge})")
        label.setStyleSheet("font-weight: 600;")
        h.addWidget(label)

        investiture_label = QLabel(f"Investiture {infusion.investiture}")
        investiture_label.setStyleSheet("color: #d5effd; font-weight: 600;")
        h.addWidget(investiture_label)

        infuse_button = QPushButton("Infuse")
        infuse_button.clicked.connect(
            lambda _, target=infusion: self.combat_window.open_infusion(target)
        )
        h.addWidget(infuse_button)

        recall_button = QPushButton("Recall")
        recall_button.clicked.connect(
            lambda _, target=infusion: self.combat_window.recall_infusion(target)
        )
        h.addWidget(recall_button)

        return row

    def refresh(self, infusions):
        self._clear_list()
        for infusion in infusions:
            self.list_layout.addWidget(self._build_infusion_row(infusion))
        self.list_layout.addStretch()
