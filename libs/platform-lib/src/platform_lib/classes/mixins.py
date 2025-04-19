from __future__ import annotations

from dataclasses import dataclass
import typing as t

from platform_lib.types import T

__all__ = ["DictMixin"]


@dataclass
class DictMixin:
    """Mixin class to add "as_dict()" method to classes. Equivalent to .__dict__.

    Add a .as_dict() method to classes that inherit from this mixin. For example,
    to add .as_dict() method to a parent class, where all children inherit the .as_dict()
    function, declare parent as:

    @dataclass
    class Parent(DictMixin):
        ...

    and call like:

        p = Parent()
        p_dict = p.as_dict()
    """

    def as_dict(self: t.Generic[T]) -> dict[str, t.Any]:
        """Return dict representation of a dataclass instance."""
        try:
            return self.__dict__.copy()

        except Exception as exc:
            raise Exception(
                f"Unhandled exception converting class instance to dict. Details: {exc}"
            )
