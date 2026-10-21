from __future__ import annotations

from abc import ABC, abstractmethod
from typing import ClassVar

from domain.models import ControlType, Grade


class RatingStrategy(ABC):
    @abstractmethod
    def calculate(self, grades: list[Grade]) -> float:
        ...


class SimpleAverageStrategy(RatingStrategy):
    def calculate(self, grades: list[Grade]) -> float:
        if not grades:
            return 0.0
        return round(sum(g.value for g in grades) / len(grades), 2)


class WeightedGradeStrategy(RatingStrategy):
    def __init__(
        self,
        exam_weight: float = 1.5,
        credit_weight: float = 1.0,
        coursework_weight: float = 1.2,
    ) -> None:
        self._weights: dict[ControlType, float] = {
            ControlType.EXAM: exam_weight,
            ControlType.CREDIT: credit_weight,
            ControlType.COURSEWORK: coursework_weight,
        }

    def calculate(self, grades: list[Grade]) -> float:
        if not grades:
            return 0.0
        total_weight = 0.0
        weighted_sum = 0.0
        for g in grades:
            w = self._weights[g.control_type]
            weighted_sum += g.value * w
            total_weight += w
        return round(weighted_sum / total_weight, 2)


class GpaStrategy(RatingStrategy):
    _MAPPING: ClassVar[dict[int, float]] = {5: 4.0, 4: 3.0, 3: 2.0, 2: 0.0}

    def calculate(self, grades: list[Grade]) -> float:
        if not grades:
            return 0.0
        return round(
            sum(self._MAPPING[g.value] for g in grades) / len(grades), 2
        )