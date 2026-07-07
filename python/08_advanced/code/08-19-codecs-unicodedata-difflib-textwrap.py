"""08-19-codecs-unicodedata-difflib-textwrap.py — Unicode, diffs, text formatting."""

import codecs
import unicodedata
import difflib
import textwrap


def unicode_normalize_example():
    composed = "café"
    decomposed = unicodedata.normalize("NFD", composed)
    print(f"Composed: {composed!r}, Decomposed: {decomposed!r}")
    assert len(decomposed) > len(composed)
    nfc = unicodedata.normalize("NFC", decomposed)
    assert nfc == composed
    print(f"char 'é': name={unicodedata.name('é')}, category={unicodedata.category('é')}")


def spellcheck_suggestions(word: str, candidates: list[str]) -> list[str]:
    return difflib.get_close_matches(word, candidates, n=3, cutoff=0.6)


def text_diff_view():
    before = ["def hello():", '    print("world")']
    after = ["def greet():", '    print("hello")', '    print("world")']
    diff = list(difflib.unified_diff(before, after, lineterm=""))
    print("\n".join(diff))


def text_wrap_demo():
    text = "This is a very long line that needs to be wrapped to fit within a specific width for display purposes."
    wrapped = textwrap.fill(text, width=40)
    dedented = textwrap.dedent("    indented line\n    another")
    print(f"Wrapped:\n{wrapped}")
    print(f"Shortened: {textwrap.shorten(text, width=30)}")


if __name__ == "__main__":
    unicode_normalize_example()
    print(f"Did you mean? {spellcheck_suggestions('helo', ['hello', 'help', 'hero', 'held'])}")
    text_diff_view()
    text_wrap_demo()
