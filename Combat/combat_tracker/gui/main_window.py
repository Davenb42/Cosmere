from PySide6.QtWidgets import QMainWindow

from combat_tracker.gui.combat_view import CombatView


class CombatMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Combat Tracker")
        self.resize(1200, 720)
        self.setCentralWidget(CombatView())
