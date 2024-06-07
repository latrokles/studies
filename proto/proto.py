from __future__ import annotations

import itertools

import pytest

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
    uid: str
    # tag: str
    slots: List[Slot]

    def __post_init__(self):
        self.set_slot("self", self)

    @property
    def parents(self):
        return [slot.value for slot in self.slots if slot.is_parent]

    def clone(self, uid, **kwargs):
        parent = Slot("parent", self, True) 
        additional_slots = [Slot(name, value) for name, value in kwargs.items()]
        new = Object(uid, [parent] + additional_slots)
        return new

    def get_slot(self, name):
        for objekt in self.slot_resolution_order():
            if (slot := objekt.find_slot(name)):
                return slot.value
        raise RuntimeError(f"{self.uid} does not understand `{name}`!")

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

    def __str__(self):
        self_slot = f"{self.get_slot('self').uid}"
        contents = [slot for slot in self.slots if slot.name != "self"]
        contents = " ".join(f"{slot}" for slot in contents if slot.is_not_executable)
        return f"({self.uid} SELF={self_slot} {contents})"
    
    def __repr__(self):
        return str(self)



@dataclass
class NativeBinaryMethod(Object):
    code: Callable

    def execute(self, receiver, argument):
        # TODO clarify how `code` has to unwrap the object values
        # perform the operation and return the appropriate object
        return self.code(receiver, argument)

    def __str__(self):
        return super().__str__()

    def __repr__(self):
        return str(self)



OBJECT = Object(uid="0", slots=[])

Integer = OBJECT.clone("1")
Integer.set_method_slot("+", NativeBinaryMethod("+", [], lambda x, y: x.get_slot("value") + y))
Integer.set_method_slot("-", NativeBinaryMethod("-", [], lambda x, y: x.get_slot("value") - y))
Integer.set_method_slot("*", NativeBinaryMethod("*", [], lambda x, y: x.get_slot("value") * y))
Integer.set_method_slot("/", NativeBinaryMethod("/", [], lambda x, y: x.get_slot("value") / y))


def test_clones_object_without_additional_slots():
    new_object = OBJECT.clone(1)
    assert id(new_object) != id(OBJECT)
    assert new_object.get_slot("parent") == OBJECT


def test_clones_object_with_additional_slots():
    new_object = OBJECT.clone(1, title="smalltalk")
    assert new_object.get_slot("title") == "smalltalk"


def test_gets_inherited_slot():
    parent = OBJECT.clone(1, tag="person")
    child = parent.clone(2, name="bob")
    assert child.get_slot("tag") == "person"
    assert child.get_slot("name") == "bob"


def test_get_slot_raises_error_if_slot_is_not_found():
    new_object = OBJECT.clone(1)
    with pytest.raises(RuntimeError):
        new_object.get_slot("foo")


def test_set_slot():
    new_object = OBJECT.clone(1)
    new_object.set_slot("name", "bob")
    assert new_object.get_slot("name") == "bob"


def test_set_slot_replaces_existing_slot():
    new_object = OBJECT.clone(1, name="bob")
    new_object.set_slot("name", "bob")
    assert new_object.get_slot("name") == "bob"


def test_set_parent():
    point = OBJECT.clone(1)
    point1 = OBJECT.clone(2)
    point1.set_parent_slot("trait-point", point)
    assert point1.get_slot("trait-point") == point


def test_slot_str_representation():
    s = Slot("name", "bob")
    assert str(s) == "name=bob"
    assert repr(s) == "name=bob"


def test_str_representation():
    point = OBJECT.clone(1, x=1, y=1)
    assert str(point) == "(1 SELF=1 *parent=(0 SELF=0 ) x=1 y=1)"
    assert repr(point) == "(1 SELF=1 *parent=(0 SELF=0 ) x=1 y=1)"
