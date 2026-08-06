import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from Prototype.engine.campaign_browser import CampaignBrowser
from Prototype.engine.encounter_loader import EncounterLoader
from Prototype.engine.combat_tracker import CombatTracker

browser = CampaignBrowser("Campaign")

encounter_path = browser.choose_encounter()

loader = EncounterLoader("Campaign")

encounter = loader.load(encounter_path)

tracker = CombatTracker(encounter)

tracker.run()