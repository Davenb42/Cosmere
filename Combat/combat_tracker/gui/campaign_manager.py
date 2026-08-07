from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from combat_tracker.gui.combat_window import CombatWindow


class CampaignManagerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Campaign Manager")
        self.resize(900, 620)

        self.campaign_root = Path(__file__).resolve().parents[1] / "Campaign"
        self.selected_path = None

        root = QWidget(self)
        self.setCentralWidget(root)

        layout = QVBoxLayout(root)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        title = QLabel("Campaign Manager")
        title.setStyleSheet("font-size: 26px; font-weight: 700;")
        layout.addWidget(title)

        self.tree = QTreeWidget()
        self.tree.setHeaderLabel("Campaign")
        self.tree.itemClicked.connect(self._handle_tree_click)
        self.populate_tree()
        layout.addWidget(self.tree, 1)

        actions = QHBoxLayout()
        actions.addStretch()

        self.load_button = QPushButton("Load Encounter")
        self.load_button.clicked.connect(self.load_selected_encounter)
        self.load_button.setEnabled(False)
        actions.addWidget(self.load_button)

        layout.addLayout(actions)

    def populate_tree(self):
        self.tree.clear()
        root_item = QTreeWidgetItem(["Campaign"])
        root_item.setData(0, Qt.UserRole, str(self.campaign_root))
        self.tree.addTopLevelItem(root_item)
        self._populate_campaign(root_item, self.campaign_root)
        self.tree.expandItem(root_item)

    def _populate_campaign(self, parent_item, folder):
        if not folder.exists() or not folder.is_dir():
            return

        children = sorted(
            p for p in folder.iterdir()
            if p.is_dir() and p.name.lower().startswith("chapter")
        )

        for child in children:
            item = QTreeWidgetItem([child.name])
            item.setData(0, Qt.UserRole, str(child))
            parent_item.addChild(item)
            self._populate_chapter(item, child)

    def _populate_chapter(self, chapter_item, chapter_dir):
        if not chapter_dir.exists() or not chapter_dir.is_dir():
            return

        encounter_dirs = sorted(
            p for p in chapter_dir.iterdir()
            if p.is_dir() and (p / "encounter.json").exists()
        )

        for encounter_dir in encounter_dirs:
            encounter_item = QTreeWidgetItem([encounter_dir.name])
            encounter_item.setData(0, Qt.UserRole, str(encounter_dir))
            chapter_item.addChild(encounter_item)

    def _handle_tree_click(self, item, column):
        path = Path(item.data(0, Qt.UserRole))
        self.selected_path = path
        self.load_button.setEnabled(path.is_dir() and (path / "encounter.json").exists())

    def load_selected_encounter(self):
        if not self.selected_path or not self.selected_path.is_dir():
            QMessageBox.warning(self, "No Encounter", "Select an encounter folder first.")
            return

        encounter_file = self.selected_path / "encounter.json"
        if not encounter_file.exists():
            QMessageBox.warning(self, "No Encounter", "That folder does not contain an encounter.json file.")
            return

        campaign_root = self.campaign_root
        combat_window = CombatWindow(campaign_root, self.selected_path)
        combat_window.closed.connect(self.show)
        combat_window.show()
        self.hide()
