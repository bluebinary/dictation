import sys, os

path = os.path.join(os.path.dirname(__file__), "..", "source")

sys.path.insert(0, path)  # add dictation library path for importing into the tests

import pytest
import dictation


@pytest.fixture(name="sampleA", scope="session")
def dictationSampleA() -> dictation.dictation:
    """Create a dictation sample instance without annotations for the unit tests"""
    return dictation.dictation(a=1, b=2, c=3)


@pytest.fixture(name="sampleB", scope="session")
def dictationSampleB() -> dictation.dictation:
    """Create a dictation sample instance with annotations for the unit tests"""
    return dictation.dictation(a=1, b=2, c=3).annotate(d=4, e=5)
