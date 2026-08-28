from dataclasses import dataclass
from typing import Optional


@dataclass
class Infusion:

    name: str

    surge: str

    investiture: int

    created_round: int

    creator_id: Optional[int] = None

    recipient_id: Optional[int] = None

    pending_removal: bool = False
