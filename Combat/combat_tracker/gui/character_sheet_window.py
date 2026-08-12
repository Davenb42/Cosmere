from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QMainWindow, QScrollArea, QVBoxLayout, QWidget

from combat_tracker.gui.panel_base import CombatPanel


class CharacterSheetWindow(QMainWindow):
    def __init__(self, character, populate_details, parent=None):
        super().__init__(parent)
        self.character = character
        self._populate_details = populate_details

        self.setWindowTitle(f"{self.character.display_name} Sheet")
        self.resize(620, 760)

        root = QWidget()
        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(12, 12, 12, 12)
        root_layout.setSpacing(10)

        panel = CombatPanel("CHARACTER SHEET")

        self.content = QWidget()
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(10)
        self.content_layout.setAlignment(Qt.AlignTop)

        self.top = QWidget()
        self.top_layout = QVBoxLayout(self.top)
        self.top_layout.setContentsMargins(10, 10, 10, 10)
        self.top_layout.setSpacing(10)
        self.top_layout.setAlignment(Qt.AlignTop)

        self.bottom = QWidget()
        self.bottom_layout = QVBoxLayout(self.bottom)
        self.bottom_layout.setContentsMargins(10, 0, 10, 10)
        self.bottom_layout.setSpacing(10)
        self.bottom_layout.setAlignment(Qt.AlignTop)

        self.content_layout.addWidget(self.top)
        self.content_layout.addWidget(self.bottom)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setWidget(self.content)

        panel.content_layout.addWidget(scroll)
        root_layout.addWidget(panel)
        self.setCentralWidget(root)

    def _clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def refresh_sheet(self):
        self.setWindowTitle(f"{self.character.display_name} Sheet")
        self._clear_layout(self.top_layout)
        self._clear_layout(self.bottom_layout)
        self._populate_details(self.character, self.top_layout, self.bottom_layout)