import pytest

from dictation import (
    dictation,
    attrs,
    lazydict,
)


@pytest.fixture(name="sample", scope="function")
def sample_fixture():
    """Create a sample lazydict sample dictionary."""

    # Define a sample source data set as a regular built-in Python dictionary
    source = {
        "x": 1,
        "y": 2,
        "z": 3,
    }

    # Instantiate a new dictation dictionary with the contents of the source dictionary
    sample = lazydict(source)

    # Confirm that the newly created dictation dictionary conforms to expectations
    assert isinstance(sample, dict)
    assert isinstance(sample, dictation)
    assert isinstance(sample, attrs)
    assert isinstance(sample, lazydict)

    return sample


def test_lazydict_instantiation(sample: lazydict):
    """Ensure that a lazydict dictionary can be created and accessed as expected"""

    # Confirm that the newly created dictation dictionary conforms to expectations
    assert isinstance(sample, lazydict)

    # Check that the expected length matches
    assert len(sample) == 3


def test_lazydict_item_exists(sample: lazydict):
    """Ensure that item existence checks works as expected."""

    assert "x" in sample
    assert "y" in sample
    assert "z" in sample

    assert not "a" in sample
    assert not "b" in sample
    assert not "c" in sample


def test_lazydict_item_access(sample: lazydict):
    """Ensure that item retrieval works as expected."""

    assert sample["x"] == 1
    assert sample["y"] == 2
    assert sample["z"] == 3


def test_lazydict_item_setting(sample: lazydict):
    """Ensure that item value setting works as expected."""

    assert sample["z"] == 3

    sample["z"] = 4

    assert sample["z"] == 4


def test_lazydict_attribute_exists(sample: lazydict):
    """Ensure that attribute existence checks work as expected."""

    assert hasattr(sample, "x")
    assert hasattr(sample, "y")
    assert hasattr(sample, "z")

    assert not hasattr(sample, "a")
    assert not hasattr(sample, "b")
    assert not hasattr(sample, "c")


def test_lazydict_attribute_access(sample: lazydict):
    """Ensure that attribute access works as expected."""

    assert sample.x == 1
    assert sample.y == 2
    assert sample.z == 3


def test_lazydict_attribute_setting(sample: lazydict):
    """Ensure that attribute setting works as expected."""

    assert sample.z == 3

    sample.z = 4

    assert sample.z == 4


def test_lazydict_attribute_deleting(sample: lazydict):
    """Ensure that attribute deletion works as expected."""

    assert sample.z == 3

    del sample.z

    assert not hasattr(sample, "z")


def test_lazydict_attribute_lazy_loading(sample: lazydict):
    """Ensure that attribute lazy loading works as expected."""

    def callback(key: object, parent: lazydict, calltype: str) -> dict:
        """Simple lazy loader that returns a dictionary for the key specified and for
        the value also uses the key. The lazy loader callback must always return a dictionary, but do not need to just return a dictionary for the current key, instead they can run any operations needed to source, build, format, and return a dictionary value consisting of one or more keys and associated values.
        """

        return {key: key}

    sample.callback = callback

    assert not "d" in sample
    assert sample.d == "d"
    assert "d" in sample

    assert not "e" in sample
    assert sample.e == "e"
    assert "e" in sample

    assert not "f" in sample
    assert sample.f == "f"
    assert "f" in sample
