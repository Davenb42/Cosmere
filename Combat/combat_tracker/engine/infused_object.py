from dataclasses import dataclass
from typing import Optional


@dataclass
class InfusedObject:

    name: str

    surge: str

    investiture: int

    created_round: int

    zero_at_round: Optional[int] = None
