import pytest

from proto import * 


def test_clones_object_without_additional_slots():
    new_object = OBJECT.clone(1)
    assert id(new_object) != id(OBJECT)
    assert new_object.get_slot("parent") == OBJECT


def test_clones_object_with_additional_slots():
    new_object = OBJECT.clone(1, title="smalltalk")
    assert new_object.get_slot("title") == "smalltalk"


def test_gets_inherited_slot():
    parent = OBJECT.clone(tag="person")
    child = parent.clone(name="bob")
    assert child.tag == "person"
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
    assert str(point) == "(1 *parent=(Object ) x=1 y=1)"
    assert repr(point) == "(1 *parent=(Object ) x=1 y=1)"


def test_integer_methods():
    number1 = Integer.clone(value=1)
    number2 = Integer.clone(value=2)
    result = Integer.get_slot("+").execute(number1, number2)
    assert result.tag == Integer.tag
    assert unbox(result) == 3
    assert unbox(Integer.get_slot("negate").execute(number1)) == -1


def test_float_methods():
    number1 = Float.clone(value=2.5)
    number2 = Float.clone(value=2.5)
    result = Integer.get_slot("+").execute(number1, number2)
    assert result.tag == Float.tag
    assert unbox(result) == 5.0
    assert unbox(Integer.get_slot("negate").execute(result)) == -5.0

