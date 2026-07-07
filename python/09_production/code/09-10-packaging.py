"""Packaging & distribution — demo script covering pyproject.toml, build, twine, entry_points.

This script demonstrates the structure of a publishable Python package.
Run: python 09-10-packaging.py
"""

import sys
import textwrap


def show_pyproject_toml() -> str:
    """Return an example pyproject.toml content."""
    return textwrap.dedent("""\
        [build-system]
        requires = ["setuptools>=64"]
        build-backend = "setuptools.backends._legacy:_Backend"

        [project]
        name = "movie-cli"
        version = "0.1.0"
        description = "A CLI tool to manage movie databases"
        requires-python = ">=3.10"
        license = {text = "MIT"}
        dependencies = [
            "requests>=2.31",
        ]

        [project.scripts]
        movie-cli = "movie_cli:main"
    """)


def show_setup_py() -> str:
    """Return an example setup.py content (legacy)."""
    return textwrap.dedent("""\
        from setuptools import setup, find_packages

        setup(
            name="movie-cli",
            version="0.1.0",
            packages=find_packages(),
            install_requires=["requests>=2.31"],
            entry_points={
                "console_scripts": [
                    "movie-cli=movie_cli:main",
                ],
            },
        )
    """)


def main() -> None:
    print("=" * 50)
    print("Packaging & Distribution Demo")
    print("=" * 50)

    print("\n1. Modern approach: pyproject.toml")
    print("-" * 30)
    print(show_pyproject_toml())

    print("\n2. Legacy approach: setup.py")
    print("-" * 30)
    print(show_setup_py())

    print("\n3. Build & publish commands")
    print("-" * 30)
    commands = textwrap.dedent("""\
        # Build source distribution and wheel
        python -m build

        # Upload to TestPyPI
        twine upload --repository-url https://test.pypi.org/legacy/ dist/*

        # Upload to PyPI
        twine upload dist/*

        # Version bump (semver)
        # MAJOR.MINOR.PATCH — 0.1.0 → 0.1.1 (bugfix), 0.2.0 (feature), 1.0.0 (breaking)
    """)
    print(commands)

    print("\n4. Semantic versioning")
    print("-" * 30)
    print("  Given version MAJOR.MINOR.PATCH:")
    print("  - MAJOR: incompatible API changes")
    print("  - MINOR: backward-compatible new features")
    print("  - PATCH: backward-compatible bug fixes")


if __name__ == "__main__":
    main()
