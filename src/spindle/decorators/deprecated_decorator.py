import functools
import warnings
from typing import Callable

__all__ = ["Deprecated"]


class Deprecated:
    """
    This is a decorator class which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used.
    """

    def __init__(self, reason: str) -> None:
        self.reason = reason

    def __call__(self, func1: Callable) -> Callable:
        message = "Call to deprecated function {name} ({reason})."

        @functools.wraps(func1)
        def new_func1(*args, **kwargs):
            warnings.simplefilter("always", DeprecationWarning)
            warnings.warn(
                message.format(name=func1.__name__, reason=self.reason),
                category=DeprecationWarning,
                stacklevel=2,
            )
            warnings.simplefilter("default", DeprecationWarning)
            return func1(*args, **kwargs)

        return new_func1


if __name__ == "__main__":
    # Usage example:
    @Deprecated("This function will be removed in future versions.")
    def some_old_function():
        print("This function is deprecated.")

    some_old_function()
