"""Reward block abstractions."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:  # pragma: no cover
    from strand.core.sequence import Sequence


@dataclass(slots=True)
class RewardContext:
    iteration: int = 0
    metadata: Mapping[str, int | float | str] = field(default_factory=dict)


@runtime_checkable
class RewardBlockProtocol(Protocol):
    name: str
    weight: float

    def score(self, sequence: Sequence, *, context: RewardContext | None = None) -> float:  # noqa: D401
        """Return the weighted score for the given sequence."""


@dataclass(slots=True)
class BaseRewardBlock:
    name: str
    weight: float = 1.0

    def score(self, sequence: Sequence, *, context: RewardContext | None = None) -> float:
        return self.weight * self._score(sequence, context or RewardContext())

    def _score(self, sequence: Sequence, context: RewardContext) -> float:
        raise NotImplementedError

    def __add__(self, other: BaseRewardBlock | list[BaseRewardBlock]) -> list[BaseRewardBlock]:
        """Compose reward blocks into a list for convenient chaining."""
        if isinstance(other, list):
            return [self] + other
        return [self, other]

    def __radd__(self, other: int | list[BaseRewardBlock]) -> list[BaseRewardBlock]:
        """Support sum() and prepending to lists."""
        if isinstance(other, int):  # sum() starts with 0
            return [self]
        if isinstance(other, list):
            return other + [self]
        return [self, other]
