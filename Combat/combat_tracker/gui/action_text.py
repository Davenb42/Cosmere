"""Pure text-formatting helpers for rendering actions/talents/features as label text."""


def is_blank(value):
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    if isinstance(value, (list, tuple, dict, set)):
        return len(value) == 0
    return False


def normalize_action_name(name):
    text = str(name).strip()
    if text.lower().startswith("strike "):
        return text[7:]
    return text


def get_action_value(action, *keys):
    if not isinstance(action, dict):
        return None

    lowered = {
        str(key).strip().lower(): value
        for key, value in action.items()
    }
    for key in keys:
        value = lowered.get(str(key).strip().lower())
        if value is not None:
            return value
    return None


def action_symbol(action):
    cost = get_action_value(action, "action cost", "action_cost", "cost")
    if is_blank(cost):
        return "►"

    value = str(cost).strip().lower()
    if value in {"1", "1 action"}:
        return "►"
    if value in {"2", "2 actions"}:
        return "►►"
    if value in {"3", "3 actions"}:
        return "►►►"
    if "free" in value:
        return "▷"
    if "reaction" in value:
        return "↩"
    if "special" in value:
        return "★"
    if "always" in value:
        return "∞"

    return "►"


def format_action_lines(action_name, action_data):
    lines = [f"{action_symbol(action_data)} {normalize_action_name(action_name)}"]

    aoe = get_action_value(action_data, "aoe", "target")
    attack = get_action_value(action_data, "attack")
    action_range = get_action_value(action_data, "range")
    saving_throw = get_action_value(action_data, "saving throw")
    damage = get_action_value(action_data, "damage")
    graze = get_action_value(action_data, "graze")
    hit = get_action_value(action_data, "hit")
    duration = get_action_value(action_data, "duration")
    description = get_action_value(action_data, "description")
    focus_cost = get_action_value(action_data, "focus cost")

    summary = []
    if not is_blank(aoe):
        summary.append(str(aoe).strip())

    if not is_blank(attack):
        attack_text = str(attack).strip()
        if "d20" not in attack_text.lower() and (
            attack_text.startswith("+")
            or attack_text.startswith("-")
            or attack_text.isdigit()
        ):
            attack_text = f"1d20{attack_text}"
        attack_text = f"{attack_text} vs Physical Def."
        summary.append(attack_text)

    if not is_blank(action_range):
        summary.append(f"({str(action_range).strip()})")

    if summary:
        lines.append(" ".join(summary))

    if not is_blank(saving_throw):
        lines.append(str(saving_throw).strip())

    if not is_blank(graze):
        lines.append(f"Graze: {str(graze).strip()}")

    if not is_blank(hit):
        lines.append(f"Hit: {str(hit).strip()}")

    if not is_blank(damage):
        lines.append(f"Damage: {str(damage).strip()}")

    if not is_blank(duration):
        lines.append(f"Duration: {str(duration).strip()}")

    if not is_blank(focus_cost):
        focus_text = str(focus_cost).strip()
        if focus_text not in {"0", "0.0"}:
            lines.append(f"Focus Cost: {focus_text}")

    if not is_blank(description):
        lines.append(str(description).strip())

    return lines


def format_talent_lines(talent_name, talent_data):
    lines = [f"{action_symbol(talent_data)} {str(talent_name).strip()}"]

    description = get_action_value(talent_data, "description")
    if not is_blank(description):
        lines.append(str(description).strip())
        return lines

    if isinstance(talent_data, dict):
        ignored_keys = {"action cost", "action_cost", "cost"}
        for key, value in talent_data.items():
            key_text = str(key).strip()
            if key_text.lower() in ignored_keys or is_blank(value):
                continue
            lines.append(str(value).strip())

    return lines


def format_feature_lines(feature_name, feature_data):
    lines = [str(feature_name).strip()]

    if isinstance(feature_data, dict):
        description = get_action_value(feature_data, "description")
        if not is_blank(description):
            lines.append(str(description).strip())
        else:
            for value in feature_data.values():
                if is_blank(value):
                    continue
                lines.append(str(value).strip())
    elif not is_blank(feature_data):
        lines.append(str(feature_data).strip())

    return lines


def format_remaining_actions(actions_remaining):
    try:
        value = int(actions_remaining)
    except (TypeError, ValueError):
        return "None"

    if value <= 0:
        return "None"

    return "►" * value


def format_attribute_with_defense(attribute_name, attribute_value, defense_name, defense_value, paired_name, paired_value):
    return (
        f"{attribute_name} {attribute_value}   "
        f"{defense_name} {defense_value}   "
        f"{paired_name} {paired_value}"
    )
