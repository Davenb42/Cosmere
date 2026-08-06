from pathlib import Path


class CampaignBrowser:

    def __init__(self, campaign_folder):
        self.campaign_folder = Path(campaign_folder)

    def list_folders(self, current=None):
        current = Path(current) if current is not None else self.campaign_folder
        folders = sorted(
            [
                folder
                for folder in current.iterdir()
                if folder.is_dir() and folder.name not in ("PCs", "NPCs", "Conditions", "__pycache__")
            ]
        )
        return {
            "current": current,
            "folders": folders,
            "has_encounter": (current / "encounter.json").exists(),
            "parent": current.parent if current != self.campaign_folder else None,
        }

    def choose_encounter(self, current=None, selection=None):
        current = Path(current) if current is not None else self.campaign_folder

        if selection is None:
            return current if (current / "encounter.json").exists() else None

        if selection == "back" and current != self.campaign_folder:
            return current.parent

        if selection == 0 and (current / "encounter.json").exists():
            return current

        if isinstance(selection, int):
            folders = self.list_folders(current)["folders"]
            if 0 <= selection - 1 < len(folders):
                return folders[selection - 1]

        return current
