from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
import typing as t

from platform_lib.constants import VALID_FILESIZE_UNITS

__all__ = ["ConvertedBytes"]


@dataclass
class ConvertedBytes:
    """Store converted bytes amount & unit."""

    amount: t.Union[Decimal, int] = field(default=0.00)
    unit: str = field(default="B")

    def __post_init__(self):
        if self.unit not in VALID_FILESIZE_UNITS:
            raise ValueError(
                f"Invalid unit: {self.unit}. Must be one of {VALID_FILESIZE_UNITS}"
            )

        round_amount: Decimal = round(self.amount, 2)
        self.amount = round_amount
