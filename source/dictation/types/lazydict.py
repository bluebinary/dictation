from __future__ import annotations

from dictation.logging import logger
from dictation.types.attrs import attrs
from types import MappingProxyType

logger = logger.getChild(__name__)


class lazydict(attrs):
    """A dictionary subclass that supports lazily loading further data via callback."""

    _reserved: list[str] = ["recursive", "callback"]
    _keys: list[object] = None
    _callback: callable = None
    _calltype: tuple[str] = None
    _calltypes: tuple[str] = ["has", "get"]

    def __init__(
        self,
        *args,
        callback: callable = None,
        calltype: list[str] = ["get"],
        **kwargs,
    ):
        """Supports initialising the dictionary's data, its optional lazy loader callback method, and optional list of origins that trigger the callback."""

        self._keys: list[object] = []

        super().__init__(*args, **kwargs)

        self._keys.extend(list(self.keys()))

        if callback is None:
            pass
        elif callable(callback):
            self._callback = callback
        else:
            raise TypeError("The 'callback' argument must reference a callable!")

        if calltype is None:
            pass
        elif isinstance(calltype, (list, tuple, set)):
            for type in calltype:
                if not isinstance(type, str):
                    raise TypeError(
                        "The 'calltype' argument must reference a list of strings!"
                    )
                elif not type in self.__class__._calltypes:
                    raise ValueError(
                        "The 'calltype' argument list can only contain the following type values: '%s'!"
                        % ("', '".join(self.__class__._calltypes))
                    )

            self._calltype = tuple(set(calltype))
        else:
            raise TypeError("The 'calltype' argument must reference a list of strings!")

    def __contains__(self, key: object) -> bool:
        """Supports checking if an item exists in the dictionary, or attempt to lazily load it, if absent."""

        if key in self._keys:
            return True
        elif self._callback and "has" in self._calltype:
            if isinstance(loaded := self._load(key=key, calltype="has"), dict):
                if dict.__contains__(loaded, key) is True:
                    return True

        return False

    def __getitem__(self, key: object) -> object:
        """Supports getting an item from the dictionary, or attempt to lazily load it, if absent."""

        logger.debug("%s.__getitem__(key: %s)", self.__class__.__name__, key)

        if key in self._keys:
            return super().__getitem__(key)
        elif self._callback and "get" in self._calltype:
            if isinstance(loaded := self._load(key=key, calltype="get"), dict):
                if dict.__contains__(loaded, key) is True:
                    return dict.__getitem__(loaded, key)

        raise KeyError(f"No '{key}' key can be found in the dictionary!")

    def __setitem__(self, key: object, value: object):
        """Supports setting an item in the dictionary and updating the known keys."""

        super().__setitem__(key, value)

        self._keys += list(key)

    def __delitem__(self, key: object):
        """Supports deleting an item from the dictionary and updating the known keys."""

        super().__delitem__(key)

        if (index := self._keys.index(key)) >= 0:
            del self._keys[index]

    def _load(self, key: object, calltype: str) -> lazydict:
        """Supports lazily loading the value for the specified key via the callback."""

        if not callable(self._callback):
            logger.warning(
                "%s._load(key: %s) No valid callback has been specified!",
                self.__class__.__name__,
                key,
            )

            return self

        loaded = self._callback(
            key=key,
            parent=MappingProxyType(self),
            calltype=calltype,
        )

        if loaded is None:
            logger.warning(
                "%s._load(key: %s) The callback returned no data!",
                self.__class__.__name__,
                key,
            )

            return self

        if not isinstance(loaded, dict):
            raise TypeError("The lazy loader callback method must return a dictionary!")

        super().update(loaded)

        self._keys += list(loaded.keys())

        def patch(dictionary: dict):
            """Ensure the dictionary and any nested nodes reference the callback."""

            if isinstance(dictionary, dict):
                if not isinstance(dictionary, lazydict):
                    dictionary = lazydict(dictionary, callback=self.callback)
                else:
                    dictionary.callback = self.callback

                for key, value in dictionary.items():
                    if isinstance(value, dict):
                        dictionary[key] = patch(value)
                    elif isinstance(value, (list, tuple, set)):
                        for index, item in enumerate(value):
                            if isinstance(item, dict):
                                value[index] = patch(item)

            return dictionary

        patch(self)

        return self

    def has(self, key: object) -> bool:
        """Supports checking if an item exists in the dictionary, or attempt to lazily
        load it, if absent."""

        logger.debug("%s.has(key: %s)", self.__class__.__name__, key)

        return self.__contains__(key)

    def get(self, key: object, default: object = None) -> object:
        """Supports getting an item from the dictionary, or attempt to lazily load it,
        if absent, and if the key is still not available, return the default value."""

        logger.debug(
            "%s.get(key: %s, default: %s)", self.__class__.__name__, key, default
        )

        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def set(self, key: object, value: object) -> lazydict:
        """Supports setting an item in the dictionary and updating the known keys."""

        logger.debug("%s.set(key: %s, value: %s)", self.__class__.__name__, key, value)

        self.__setitem__(key, value)

        return self

    def unset(self, key: object) -> lazydict:
        """Supports unsetting/deleting an item from the dictionary and updating the known keys."""

        # logger.debug("%s.unset(key: %s)", self.__class__.__name__, key)

        self.__delitem__(key)

        return self

    @property
    def callback(self) -> callable | None:
        """Returns the callback method that has been associated with the dictionary."""

        return self._callback

    @callback.setter
    def callback(self, callback: callable):
        """Supports setting the callback method for the dictionary."""

        if callback is None:
            pass
        elif not callable(callback):
            raise TypeError("The 'callback' argument must reference a callable!")

        self._callback = callback
