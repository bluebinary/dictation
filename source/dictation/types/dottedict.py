from __future__ import annotations

from dictation.types.dictation import dictation
from dictation.logging import logger
from dictation.utilities import (
    has as _has,
    get as _get,
    set as _set,
    unset as _unset,
)

logger = logger.getChild(__name__)


class dottedict(dictation):
    """Extended dictionary type supporting dotted access to nested properties."""

    _separator: str = "."
    _reserved: list[str] = ["recursive", "separator"]

    def __init__(self, *args, separator: str = ".", **kwargs):
        """Supports initialising the dotted dictionary subclass."""

        super().__init__(*args, **kwargs)

        if isinstance(separator, str):
            self._separator = separator
        elif not len(separator) >= 1:
            raise ValueError(
                "The 'separator' argument must reference a non-empty string!"
            )
        else:
            raise TypeError("The 'separator' argument must have a string value!")

    def __contains__(self, key: str) -> bool:
        """Supports determining if the dictionary has the specified key or not."""

        return self.has(key=key)

    def __getitem__(self, key: str) -> object:
        """Supports getting the dictionary item from the specified key."""

        return self.get(key=key)

    def __setitem__(self, key: str, value: object):
        """Supports setting the dictionary item value at the specified key."""

        return self.set(key=key, value=value)

    def __delitem__(self, key: str):
        """Supports deleting the dictionary item at the specified key."""

        return self.unset(key=key)

    def has(self, key: object) -> bool:
        """Supports determining if the dictionary has the specified key or not."""

        return _has(self, key, separator=self._separator)

    def get(self, key: object, default: object = None) -> object | None:
        """Overrides the `dict` class' `get` method to support specifying the default
        value positionally as well as via its keyword argument to improve documentation
        of the code at the call site, e.g. x.get("y", 0) vs x.get("y", default=0)."""

        return _get(self, key, default, separator=self._separator)

    def set(self, key: object, value: object) -> dottedict:
        """Provides a `set` method to compliment the built-in `dict` class' `get` method
        which takes the usual key and value as keyword arguments, and assigns the value
        to the current dictionary instance at the provided key. As this method returns
        `self`, calls to `set()` can be chained with calls to other class methods."""

        _set(self, key, value, typed=dottedict, separator=self._separator)

        return self

    def unset(self, key: object) -> dottedict:
        """Provides an `unset` method to compliment the built-in `dict` class' `set`. As
        this method returns `self`, calls to `set()` can be chained with calls to other
        class methods."""

        _unset(self, key, separator=self._separator)

        return self
