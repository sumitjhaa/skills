"""Virtual environments & dependencies — demo script for the lesson.

This script prints information about the current Python environment.
It should be run from within an activated virtual environment.

Usage:
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    python 09-08-virtual-envs.py
"""

import sys
import os
import site


def get_env_info() -> dict[str, str | bool]:
    """Return information about the current Python environment."""
    in_venv = sys.prefix != sys.base_prefix
    venv_path = sys.prefix if in_venv else None
    site_packages = site.getusersitepackages()
    python_version = sys.version
    return {
        "in_virtualenv": in_venv,
        "venv_path": venv_path,
        "python_version": python_version,
        "site_packages": site_packages,
        "executable": sys.executable,
    }


def main() -> None:
    info = get_env_info()

    print("=" * 50)
    print("Python Environment Info")
    print("=" * 50)
    print(f"In virtualenv:      {info['in_virtualenv']}")
    print(f"Python version:     {info['python_version']}")
    print(f"Executable:         {info['executable']}")
    print(f"Site packages:      {info['site_packages']}")

    if info["venv_path"]:
        print(f"Virtualenv path:    {info['venv_path']}")

    # Show installed packages
    try:
        import pkg_resources
        installed = sorted(
            f"{d.project_name}=={d.version}"
            for d in pkg_resources.working_set
        )
        print(f"Installed packages: {len(installed)}")
        for pkg in installed[:10]:
            print(f"  - {pkg}")
        if len(installed) > 10:
            print(f"  ... and {len(installed) - 10} more")
    except ImportError:
        print("pkg_resources not available")


if __name__ == "__main__":
    main()
