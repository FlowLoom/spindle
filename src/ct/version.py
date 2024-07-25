"""Version information"""

import os
from pathlib import Path
from subprocess import CalledProcessError  # noqa: S404 # nosec B404
from subprocess import check_output  # nosec B404

__all__ = [
    "VERSION",
    "AUTHOR",
    "AUTHOR_EMAIL",
    "get_version",
    "get_git_hash",
]

VERSION = "1.0.0-dev1"
AUTHOR = "Joshua Magady"
AUTHOR_EMAIL = "josh.magady@gmail.com"


def get_git_hash() -> str:
    """Get the :mod:`bohicalog` git hash."""
    with Path(os.devnull).open("w") as devnull:
        try:
            ret = check_output(  # nosec B404, B603, B607
                ["git", "rev-parse", "HEAD"],  # noqa: S603, S607
                cwd=Path(__file__).resolve().parent,  # nosec B607
                stderr=devnull,
            )
        except CalledProcessError:
            return "UNHASHED"
        else:
            return ret.strip().decode("utf-8")[:8]


def get_version(with_git_hash: bool = False) -> str:  # noqa: FBT001, FBT002
    """Get the :mod:`bohicalog` version string, including a git hash."""
    return f"{VERSION}-{get_git_hash()}" if with_git_hash else VERSION


if __name__ == "__main__":
    print(get_version(with_git_hash=True))  # noqa: T201