from dataclasses import dataclass, field
from typing import Any, Dict, Tuple


@dataclass
class Cell:
    value: Any
    formula: Any|None = None


@dataclass
class SpreadSheet:
    cells: Dict[Tuple[int, int]] = field(default_factory=list)


@c
class Entity:
    uid: str

