import sys, os

path = os.path.join(os.path.dirname(__file__), "..", "source")

sys.path.insert(0, path)  # add dictation library path for importing into the tests

import pytest
import dictation

# Override the default alphabetic sort of the test modules, into the order we wish to test
TEST_MODULE_ORDER = [
    "test_dictation_library",
    "test_dictation_attribute_access",
    "test_dictation_lazy_loading",
    "test_dictation_pickling",
]


def pytest_collection_modifyitems(items):
    """Modifies test items in place to ensure test modules run in the given order."""

    module_mapping = {item: item.module.__name__ for item in items}

    sorted_items = items.copy()

    # Iteratively move tests of each module to the end of the test queue
    for module in TEST_MODULE_ORDER:
        sorted_items = [it for it in sorted_items if module_mapping[it] != module] + [
            it for it in sorted_items if module_mapping[it] == module
        ]

    items[:] = sorted_items


@pytest.fixture(name="sampleA", scope="session")
def dictationSampleA() -> dictation.dictation:
    """Create a dictation sample instance without annotations for the unit tests"""
    return dictation.dictation(a=1, b=2, c=3)


@pytest.fixture(name="sampleB", scope="session")
def dictationSampleB() -> dictation.dictation:
    """Create a dictation sample instance with annotations for the unit tests"""
    return dictation.dictation(a=1, b=2, c=3).annotate(d=4, e=5)
