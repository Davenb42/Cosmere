import json
from pathlib import Path

from combat_tracker.engine.character import Character
from combat_tracker.engine.character import CharacterType
from combat_tracker.engine.encounter import Encounter
from combat_tracker.engine.resources import Resource
from combat_tracker.engine.defenses import Defenses


class EncounterLoader:

    def __init__(self, campaign_folder):
        self.campaign_folder = self._resolve_campaign_root(Path(campaign_folder))

    def _resolve_campaign_root(self, path):
        current = path if path.is_dir() else path.parent

        while True:
            if (
                (current / "party.json").exists()
                and (current / "PCS").exists()
                and (current / "NPCS").exists()
            ):
                return current

            if current == current.parent:
                return path if path.is_dir() else path.parent

            current = current.parent

    def load(self, encounter_folder):

        encounter_folder = Path(encounter_folder)
        encounter_data = self._load_json(
            encounter_folder / "encounter.json"
        )

        party = self._load_party()

        combatants = []

        for pc in party:

            combatants.append(
                self.load_character(pc, CharacterType.PC)
            )

        for npc_name, amount in encounter_data["npcs"].items():

            for _ in range(amount):

                combatants.append(
                    self.load_character(
                        npc_name,
                        CharacterType.NPC
                    )
                )

        self.number_duplicates(combatants)

        self.assign_ids(combatants)

        return Encounter(
            name=encounter_data["name"],
            combatants=combatants
        )

    def _load_party(self):

        data = self._load_json(
            self.campaign_folder / "party.json"
        )

        return data["parties"][data["active_party"]]

    def load_character(self, name, character_type):

        folder = (
            "PCS"
            if character_type == CharacterType.PC
            else "NPCS"
        )

        data = self._load_json(
            self.campaign_folder / folder / f"{name}.json"
        )

        defenses = data.get("defenses") or {
            "physical": data.get("physical defense", 0),
            "cognitive": data.get("cognitive defense", 0),
            "spiritual": data.get("spiritual defense", 0),
        }

        skills = data.get("skills") or {
            "physical": data.get("physical_skills", {}),
            "cognitive": data.get("cognitive_skills", {}),
            "spiritual": data.get("spiritual_skills", {}),
        }

        talents = data.get("Talents", data.get("talents", data.get("features", {})))
        actions = data.get("Actions", data.get("actions", {}))

        return Character(
            name=data["name"],
            character_type=character_type,

            strength=data.get("strength", 0),
            speed=data["speed"],

            intelligence=data.get("intelligence", 0),
            willpower=data.get("willpower", 0),

            awareness=data.get("awareness", 0),
            presence=data.get("presence", 0),

            movement=data["movement"],

            health=Resource(**data["health"]),
            focus=Resource(**data["focus"]),
            investiture=Resource(**data["investiture"]),

            defenses=Defenses(
                physical=defenses["physical"],
                cognitive=defenses["cognitive"],
                spiritual=defenses["spiritual"],
                deflect=data["deflect"]
            ),
            skills=skills,

            talents=talents,
            actions=actions
        )

    def assign_ids(self, combatants):

        for i, character in enumerate(combatants, start=1):

            character.id = i

    def number_duplicates(self, combatants):

        counts = {}

        for character in combatants:

            counts.setdefault(character.name, 0)
            counts[character.name] += 1

        current = {}

        for character in combatants:

            if counts[character.name] == 1:

                character.display_name = character.name
                continue

            current.setdefault(character.name, 0)
            current[character.name] += 1

            character.display_name = (
                f"{character.name} #{current[character.name]}"
            )

    @staticmethod
    def _load_json(path):

        with open(path, encoding="utf-8") as file:

            return json.load(file)