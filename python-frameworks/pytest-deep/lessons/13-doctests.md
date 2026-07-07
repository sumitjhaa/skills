# 📖 Doctests
<!-- ⏱️ 10 min | 🟢 Core -->

**What You'll Learn:** Testing code examples in docstrings with pytest's doctest support.

## Writing Doctests

```python
def add(a, b):
    """Return the sum of a and b.
    
    >>> add(2, 3)
    5
    >>> add(-1, 1)
    0
    """
    return a + b
```

## Running Doctests

```bash
pytest --doctest-modules       # Run doctests in all modules
pytest --doctest-modules -v    # Verbose
pytest --doctest-glob="*.md"   # Run doctests in markdown files
```

## Doctest in Classes

```python
class Calculator:
    def multiply(self, a, b):
        """Multiply two numbers.
        
        >>> Calculator().multiply(3, 4)
        12
        """
        return a * b
```

## Expected Exceptions

```python
def divide(a, b):
    """Divide a by b.
    
    >>> divide(10, 2)
    5.0
    >>> divide(10, 0)
    Traceback (most recent call last):
        ...
    ZeroDivisionError: division by zero
    """
    return a / b
```

## Ellipsis Matching

```python
def complex_output():
    """Returns a complex string.
    
    >>> complex_output()  # doctest: +ELLIPSIS
    Result: ...
    """
    return f"Result: {datetime.now()}"
```

<!-- 🤔 Use `--doctest-modules` to catch stale docstring examples. -->

## Run the Code

```bash
pytest code/13-doctests.py --doctest-modules -v
```
