import pytest

from dictation import (
    dictation,
    dottedict,
)


@pytest.fixture(name="sample", scope="function")
def sample_fixture() -> dottedict[object, object]:
    """Create a sample dottedict dictionary."""

    # Define a sample source data set as a regular built-in Python dictionary
    source = {
        "x": 1,
        "y": 2,
        "z": 3,
        "a": {
            "b": {
                "c": {
                    "d": 4,
                    "e": 5,
                    "f": 6,
                }
            }
        },
    }

    # source = {
    #     "a": {
    #         "b": 123,
    #     },
    # }

    # Instantiate a new dictation dictionary with the contents of the source dictionary
    return dottedict(source)


def test_dottedict_instantiation(sample: dottedict):
    """Ensure that a attrs dictionary can be created and accessed as expected"""

    # Confirm that the newly created dictation dictionary conforms to expectations
    assert isinstance(sample, dottedict)
    assert isinstance(sample, dictation)
    assert isinstance(sample, dict)

    # Check that the expected length matches
    assert len(sample) == 4

    assert sample == {
        "x": 1,
        "y": 2,
        "z": 3,
        "a": {"b": {"c": {"d": 4, "e": 5, "f": 6}}},
    }

    assert "a" in sample
    assert isinstance(sample, dottedict)
    assert sample["a"] == {"b": {"c": {"d": 4, "e": 5, "f": 6}}}

    assert "b" in sample["a"]
    assert isinstance(sample["a"]["b"], dottedict)
    assert sample["a"]["b"] == {"c": {"d": 4, "e": 5, "f": 6}}

    assert "c" in sample["a"]["b"]
    assert isinstance(sample["a"]["b"]["c"], dottedict)
    assert sample["a"]["b"]["c"] == {"d": 4, "e": 5, "f": 6}


def test_dottedict_item_exists(sample: dottedict):
    """Ensure that item existence checks works as expected."""

    assert isinstance(sample, dottedict)

    assert "x" in sample
    assert isinstance(sample["x"], int)
    assert sample["x"] == 1

    assert "y" in sample
    assert isinstance(sample["y"], int)
    assert sample["y"] == 2

    assert "z" in sample
    assert isinstance(sample["z"], int)
    assert sample["z"] == 3

    assert not "r" in sample
    assert not "s" in sample
    assert not "t" in sample

    assert "a" in sample
    assert isinstance(sample["a"], dottedict)

    assert "a.b" in sample
    assert isinstance(sample["a.b"], dottedict)

    assert "a.b.c" in sample
    assert isinstance(sample["a.b.c"], dottedict)

    assert "a.b.c.d" in sample
    assert isinstance(sample["a.b.c.d"], int)
    assert sample["a.b.c.d"] == 4

    assert "a.b.c.e" in sample
    assert isinstance(sample["a.b.c.e"], int)
    assert sample["a.b.c.e"] == 5

    assert "a.b.c.f" in sample
    assert isinstance(sample["a.b.c.f"], int)
    assert sample["a.b.c.f"] == 6


def test_dottedict_item_access(sample: dottedict):
    """Ensure that item retrieval works as expected."""

    assert sample["x"] == 1
    assert sample["y"] == 2
    assert sample["z"] == 3


def test_dottedict_item_setting(sample: dottedict):
    """Ensure that item retrieval works as expected."""

    assert sample["z"] == 3

    sample["z"] = 4

    assert sample["z"] == 4


def test_dottedict_item_deleting(sample: dottedict):
    """Ensure that attribute deletion works as expected."""

    sample["i.j.k"] = 3

    del sample["i.j.k"]

    assert not "i.j.k" in sample


def test_dottedict_item_nested_access(sample: dottedict):
    """Ensure that attribute access works as expected."""

    assert sample["a.b.c.d"] == 4
    assert sample["a.b.c.e"] == 5
    assert sample["a.b.c.f"] == 6


def test_dottedict_custom_separator():
    """Ensure that attribute access with a custom separator works as expected."""

    sample: dottedict = dottedict({"a": {"b": {"c": 123}}}, separator="/")

    assert sample["a/b/c"] == 123
