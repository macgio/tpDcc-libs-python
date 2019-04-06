def is_center(side, patterns=None):
    """
    Returns whether given side is a valid center side or not
    :param side: str
    :param patterns: list<str>
    :return: bool
    """

    if not patterns:
        patterns = ['C', 'c', 'Center', 'ct', 'center', 'middle', 'm']

    if str(side) in patterns:
        return True

    return False


def is_left(side, patterns=None):
    """
    Returns whether given side is a valid left side or not
    :param side: str
    :param patterns: list<str>
    :return: bool
    """

    if not patterns:
        patterns = ['L', 'l', 'Left', 'left', 'lf']

    if str(side) in patterns:
        return True

    return False


def is_right(side, patterns=None):
    """
    Returns whether given side is a valid right side or not
    :param side: str
    :param patterns: list<str>
    :return: bool
    """

    if not patterns:
        patterns = ['R', 'r', 'Right', 'right', 'rt']

    if str(side) in patterns:
        return True

    return False