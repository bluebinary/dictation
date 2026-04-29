import pytest

from dictation import (
    dictation,
    attrdict,
    attrs,
)


@pytest.fixture(name="sample", scope="function")
def sample_fixture() -> attrs[object, object]:
    """Create a sample attrs sample dictionary."""

    # Define a sample source data set as a regular built-in Python dictionary
    source = {
        "x": 1,
        "y": 2,
        "z": 3,
    }

    # Instantiate a new dictation dictionary with the contents of the source dictionary
    sample = attrs(source)

    # Confirm that the newly created dictation dictionary conforms to expectations
    assert isinstance(sample, attrs)
    assert isinstance(sample, attrdict)
    assert isinstance(sample, dictation)
    assert isinstance(sample, dict)

    return sample


def test_attrdict_instantiation(sample: attrs):
    """Ensure that a attrs dictionary can be created and accessed as expected"""

    # Confirm that the newly created dictation dictionary conforms to expectations
    assert isinstance(sample, attrs)

    # Check that the expected length matches
    assert len(sample) == 3


def test_attrdict_item_exists(sample: attrs):
    """Ensure that item existence checks works as expected."""

    assert "x" in sample
    assert "y" in sample
    assert "z" in sample

    assert not "a" in sample
    assert not "b" in sample
    assert not "c" in sample


def test_attrdict_item_access(sample: attrs):
    """Ensure that item retrieval works as expected."""

    assert sample["x"] == 1
    assert sample["y"] == 2
    assert sample["z"] == 3


def test_attrdict_item_setting(sample: attrs):
    """Ensure that item retrieval works as expected."""

    assert sample["z"] == 3

    sample["z"] = 4

    assert sample["z"] == 4


def test_attrdict_attribute_exists(sample: attrs):
    """Ensure that attribute existence checks work as expected."""

    assert hasattr(sample, "x")
    assert hasattr(sample, "y")
    assert hasattr(sample, "z")

    assert not hasattr(sample, "a")
    assert not hasattr(sample, "b")
    assert not hasattr(sample, "c")


def test_attrdict_attribute_access(sample: attrs):
    """Ensure that attribute access works as expected."""

    assert sample.x == 1
    assert sample.y == 2
    assert sample.z == 3


def test_attrdict_attribute_setting(sample: attrs):
    """Ensure that attribute setting works as expected."""

    assert sample.z == 3

    sample.z = 4

    assert sample.z == 4


def test_attrdict_attribute_deleting(sample: attrs):
    """Ensure that attribute deletion works as expected."""

    assert sample.z == 3

    del sample.z

    assert not hasattr(sample, "z")
