from __future__ import annotations

from dictation.logging import logger
from dictation.types.dictation import dictation
from classicist import alias

logger = logger.getChild(__name__)


@alias("attrs")
class attrdict(dictation):
    """Extended dictionary type supporting attribute access to dictionary items."""

    def __getattr__(self, name: str) -> object:
        """Support getting an item from the dictionary via an attribute access."""

        if name.startswith("_") or name in dir(self):
            return super().__getattr__(name)
        else:
            try:
                return self.__getitem__(name)
            except KeyError:
                raise AttributeError(f"No '{name}' attribute exists on the dictionary!")

    def __setattr__(self, name: str, value: object):
        """Support setting an item in the dictionary via an attribute access."""

        if name.startswith("_") or name in dir(self):
            super().__setattr__(name, value)
        else:
            self.__setitem__(name, value)

    def __delattr__(self, name: str):
        """Support deleting an item from the dictionary via an attribute access."""

        if name.startswith("_") or name in dir(self):
            super().__delattr__(name)
        else:
            self.__delitem__(name)
