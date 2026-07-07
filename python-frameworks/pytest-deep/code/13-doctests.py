"""Doctests — examples in docstrings."""


def add(a, b):
    """Return a + b.

    >>> add(2, 3)
    5
    >>> add(-1, 1)
    0
    >>> add(0, 0)
    0
    """
    return a + b


def multiply(a, b):
    """Return a * b.

    >>> multiply(3, 4)
    12
    >>> multiply(0, 5)
    0
    >>> multiply(-2, 3)
    -6
    """
    return a * b


def divide(a, b):
    """Divide a by b.

    >>> divide(10, 2)
    5.0
    >>> divide(3, 2)
    1.5
    """
    return a / b


class Calculator:
    """A simple calculator.

    >>> Calculator().add(2, 3)
    5
    >>> Calculator().multiply(3, 4)
    12
    """

    def add(self, a, b):
        return a + b

    def multiply(self, a, b):
        return a * b
