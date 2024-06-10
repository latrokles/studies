from __future__ import annotations

import importlib
import itertools
import operator
import sys

from dataclasses import dataclass, field
from typing import Callable, List


@dataclass
class Slot:
    name: str
    value: Object
    is_parent: bool = False
    is_executable: bool = False

    @property
    def is_not_executable(self):
        return not self.is_executable

    def __repr__(self):
        return str(self)

    def __str__(self):
        prefix = ""
        if self.is_parent:
            prefix = "*"
        val = f"{prefix}{self.name}={self.value}"
        return val


@dataclass
class Object:
    tag: str
    slots: List[Slot]

    def __post_init__(self):
        self.set_slot("self", self)

    @property
    def parents(self):
        return [slot.value for slot in self.slots if slot.is_parent]

    def clone(self, tag=None, **kwargs):
        tag = (tag or self.tag)
        parent = Slot("parent", self, True) 
        additional_slots = [Slot(name, value) for name, value in kwargs.items()]
        new = Object(tag, [parent] + additional_slots)
        return new

    def get_slot(self, name):
        for objekt in self.slot_resolution_order():
            if (slot := objekt.find_slot(name)):
                return slot.value
        raise RuntimeError(f"{self.tag} does not understand `{name}`!")

    def set_slot(self, name, value):
        return self._set_slot(Slot(name, value))

    def set_parent_slot(self, name, value):
        return self._set_slot(Slot(name, value, True))

    def set_method_slot(self, name, method_object):
        return self._set_slot(Slot(name, method_object, False, True))

    def _set_slot(self, slot):
        if (found_slot := self.find_slot(slot.name)):
            self.slots.remove(found_slot)
        self.slots.append(slot)
        return self

    def find_slot(self, name):
        for slot in self.slots:
            if slot.name == name:
                return slot
        return None

    def slot_resolution_order(self):
        parents_slot_resolution = [
            parent.slot_resolution_order() for parent in self.parents
        ]
        return [self] + list(itertools.chain.from_iterable(parents_slot_resolution))

    def inspect(self):
        contents = [slot for slot in self.slots if slot.name != "self"]
        contents = " ".join(f"{slot}" for slot in contents if slot.is_not_executable)
        return f"({self.tag} {contents})"

    def __str__(self):
        return self.inspect()

    def __repr__(self):
        return str(self)


@dataclass
class PrimitiveMethod(Object):
    code: Callable

    def execute(self, receiver, *args):
        match len(args):
            case 0:  # unary
                return box(self.code(unbox(receiver)))
            case 1:  # binary
                return box(self.code(unbox(receiver), unbox(args[0])))
            case _:  # keyword 
                return box(self.code(unbox(receiver), unbox(args)))

    def __str__(self):
        return super().__str__()

    def __repr__(self):
        return str(self)


@dataclass
class PrimitiveUnaryMethod(PrimitiveMethod):
    def execute(self, receiver):
        return box(self.code(unbox(receiver)))


@dataclass
class PrimitiveBinaryMethod(PrimitiveMethod):
    def execute(self, receiver, argument):
        return box(self.code(unbox(receiver), unbox(argument)))


@dataclass
class PrimitiveKeywordMethod(PrimitiveMethod):
    def execute(self, receiver, keyword):
        pass


OBJECT = Object(tag="Object", slots=[])


# native number ops
def box(native_value):
    match native_value:
        case None:
            return Nil
        case True:
            return true
        case False:
            return false
        case int():
            return Integer.clone(value=native_value)
        case float():
            return Float.clone(value=native_value)
        case str():
            return String.clone(value=native_value)
        case _:
            raise RuntimeError(f"Unable to box {native_value=} with {type(native_value)=}!")


def unbox(obj):
    return obj.get_slot("value")


def add_unary_native_method(receiver, name, fully_qualified_callable):
    """Resolves fully qualified callable and adds it to `receiver` as a unary method."""
    pass


def add_binary_native_method(receiver, name, fully_qualified_callable):
    """Resolves fully qualified callable and adds it to `receiver` as a binary method."""
    pass


PrimitiveModule = OBJECT.clone(tag="PrimitiveModule")
PrimitiveModule.set_method_slot("load", PrimitiveBinaryMethod("load", [], importlib.import_module))
PrimitiveModule.set_method_slot("unload", PrimitiveBinaryMethod("unload", [], sys.modules.pop))
PrimitiveModule.set_method_slot("get-slot", PrimitiveBinaryMethod("get-slot", [], getattr))

Nil = OBJECT.clone(tag="Nil", value=None)
Boolean = OBJECT.clone(tag="Boolean")
true = Boolean.clone(value=True)
false = Boolean.clone(value=False)
String = OBJECT.clone(tag="String")
Number = OBJECT.clone(tag="Number") 
Integer = Number.clone(tag="Integer")
Float = Number.clone(tag="Float")
Number.set_method_slot("+", PrimitiveBinaryMethod("+", [], operator.add))
Number.set_method_slot("-", PrimitiveBinaryMethod("-", [], operator.sub))
Number.set_method_slot("*", PrimitiveBinaryMethod("*", [], operator.mul))
Number.set_method_slot("/", PrimitiveBinaryMethod("/", [], operator.truediv))
Number.set_method_slot("negate", PrimitiveUnaryMethod("negate", [], operator.neg))
