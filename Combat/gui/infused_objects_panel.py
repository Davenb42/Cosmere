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


__all__ = ["InfusedObjectsPanel"]


class InfusedObjectsPanel(CombatPanel):
    """Panel listing infused objects, kept separate from combat_view.py."""

    def __init__(self, combat_window, parent=None):
        super().__init__("Infused Objects", parent)
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

        self.add_button = QPushButton("Add Infused Object")
        self.add_button.clicked.connect(self.combat_window.open_add_infused_object)
        self.content_layout.addWidget(self.add_button)

    def _clear_list(self):
        while self.list_layout.count():
            item = self.list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def _build_object_row(self, infused_object):
        row = QFrame()
        row.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        row.setMinimumHeight(52)
        depleted = infused_object.investiture <= 0
        row.setStyleSheet(
            "QFrame { background: #14181d; border: 1px solid #333a42; border-radius: 8px; }"
            if depleted
            else "QFrame { background: #1f2a35; border: 1px solid #46586a; border-radius: 8px; }"
        )

        h = QHBoxLayout(row)
        h.setContentsMargins(10, 8, 10, 8)
        h.setSpacing(10)

        label = QLabel(f"{infused_object.name} ({infused_object.surge})")
        label.setStyleSheet("font-weight: 600;")
        h.addWidget(label)

        investiture_label = QLabel(f"Investiture {infused_object.investiture}")
        investiture_label.setStyleSheet("color: #d5effd; font-weight: 600;")
        h.addWidget(investiture_label)

        infuse_button = QPushButton("Infuse")
        infuse_button.clicked.connect(
            lambda _, target=infused_object: self.combat_window.open_infuse_object(target)
        )
        h.addWidget(infuse_button)

        recall_button = QPushButton("Recall")
        recall_button.clicked.connect(
            lambda _, target=infused_object: self.combat_window.recall_infused_object(target)
        )
        h.addWidget(recall_button)

        return row

    def refresh(self, infused_objects):
        self._clear_list()
        for infused_object in infused_objects:
            self.list_layout.addWidget(self._build_object_row(infused_object))
        self.list_layout.addStretch()
