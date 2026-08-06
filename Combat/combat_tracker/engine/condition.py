from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional


class ConditionDuration(Enum):
    PERMANENT = auto()
    TARGET_NEXT_TURN = auto()
    SOURCE_NEXT_TURN = auto()
    ROUNDS = auto()


@dataclass
class Condition:

    name: str

    duration_type: ConditionDuration = ConditionDuration.PERMANENT

    rounds_remaining: int = 0

    source_id: Optional[int] = None