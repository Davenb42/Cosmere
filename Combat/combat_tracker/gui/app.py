import sys

from PySide6.QtWidgets import QApplication

from combat_tracker.gui.campaign_manager import CampaignManagerWindow


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = CampaignManagerWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
