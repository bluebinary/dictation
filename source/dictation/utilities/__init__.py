def has(dictionary: dict, keys: str | list[str], separator: str = ".") -> bool:
    """Helper method to determine if a dictionary contains the key or keys."""

    if not isinstance(variable := dictionary, dict):
        raise TypeError("The 'dictionary' argument must reference a dictionary!")

    if not isinstance(separator, str):
        raise TypeError("The 'separator' argument must have a string value!")
    elif not len(separator) >= 1:
        raise ValueError("The 'separator' argument must reference a non-empty string!")

    if isinstance(keys, str):
        if separator in keys:
            keys = keys.split(separator)
        else:
            keys = [keys]
    elif isinstance(keys, (list, set, tuple)):
        pass
    else:
        raise TypeError(
            "The 'keys' argument must reference a string key or list of string keys!"
        )

    if (count := len(keys)) == 0:
        return False

    for index, key in enumerate(keys, start=1):
        if dict.__contains__(variable, key):  # in variable:
            variable = dict.__getitem__(
                variable, key
            )  # variable[key] # type(variable).__getitem__(variable, key)
        else:
            return False

        if not isinstance(variable, dict):
            if count == index:
                break
            else:
                return False

    return True


def get(
    dictionary: dict,
    keys: str | list[str],
    default: object = None,
    separator: str = ".",
) -> object:
    """Helper method to get an item from a dictionary containing the key or keys."""

    if not isinstance(variable := dictionary, dict):
        raise TypeError("The 'dictionary' argument must reference a dictionary!")

    if not isinstance(separator, str):
        raise TypeError("The 'separator' argument must have a string value!")
    elif not len(separator) >= 1:
        raise ValueError("The 'separator' argument must reference a non-empty string!")

    if isinstance(keys, str):
        if separator in keys:
            keys = keys.split(separator)
        else:
            keys = [keys]
    elif isinstance(keys, (list, set, tuple)):
        pass
    else:
        raise TypeError(
            "The 'keys' argument must reference a string key or list of string keys!"
        )

    for key in keys:
        if dict.__contains__(variable, key):
            variable = dict.__getitem__(variable, key)
        else:
            variable = None

        if not isinstance(variable, dict):
            break

    if variable is None:
        return default

    return variable


def set(
    dictionary: dict,
    keys: str | list[str],
    value: object,
    typed: type = None,
    separator: str = ".",
):
    """Helper method to set an item value in a dictionary at the key or keys."""

    if not isinstance(variable := dictionary, dict):
        raise TypeError("The 'dictionary' argument must reference a dictionary!")

    if not isinstance(separator, str):
        raise TypeError("The 'separator' argument must have a string value!")
    elif not len(separator) >= 1:
        raise ValueError("The 'separator' argument must reference a non-empty string!")

    if typed is None:
        typed = dict
    elif isinstance(typed, type) and issubclass(typed, dict):
        pass
    else:
        raise TypeError(
            "The 'typed' argument, if specified, must reference a dictionary subclass!"
        )

    def put(variable: object, keys: str | list[str], item: object) -> None:
        if isinstance(keys, list):
            keys = separator.join([str(key) for key in keys])

        if separator in keys:
            key, rest = keys.split(separator, maxsplit=1)

            if key not in variable:
                super(type(variable), variable).__setitem__(key, typed())

            put(variable[key], rest, item)
        else:
            super(type(variable), variable).__setitem__(keys, item)

    put(variable, keys, value)


def unset(dictionary: dict, keys: str | list[str], separator: str = "."):
    """Helper method to unset an item from a dictionary at the key or keys."""

    if not isinstance(dictionary, dict):
        raise TypeError("The 'dictionary' argument must reference a dictionary!")

    if not isinstance(separator, str):
        raise TypeError("The 'separator' argument must have a string value!")
    elif not len(separator) >= 1:
        raise ValueError("The 'separator' argument must reference a non-empty string!")

    if isinstance(keys, str):
        if separator in keys:
            keys = keys.split(separator)
        else:
            keys = [keys]

    variable = dictionary

    last = keys.pop()

    for key in keys:
        if key in variable:
            variable = super(type(variable), variable).__getitem__(key)
        else:
            variable = None

        if not isinstance(variable, dict):
            break

    if isinstance(variable, dict) and last in variable:
        super(type(variable), variable).__delitem__(last)
