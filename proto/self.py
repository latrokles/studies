from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, List


@dataclass
class Slot:
    name: str
    value: Object
    is_parent: bool = False

    def __str__(self):
        prefix = ""
        if self.is_parent:
            prefix = "*"
        val = f"{prefix}{self.name}={self.value}"
        return val

    def __repr__(self):
        return str(self)


@dataclass
class Proto:
    slots: List[Slot]
    code: List[Object]|None = None

    @property
    def parents(self):
        return [slot.value for slot in self.slots if slot.is_parent]

    def clone(self, **kwargs):
        parent = Slot("parent", self, True)
        new_slots = [Slot(name, value) for name, value in kwargs.items()]
        return Object([parent] + new_slots)

    def send(self, message):
        pass

    def inspect(self):
        contents = [slot for slot in self.slots if slot.name != "self"]
        contents = " ".join(f"{slot}" for slot in contents if slot.is_not_executable)
        return f"({self.tag} {contents})"
