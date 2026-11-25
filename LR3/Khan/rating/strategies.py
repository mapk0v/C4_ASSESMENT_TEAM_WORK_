"""Strategy: взаимозаменяемые способы анализа баллов одного модуля."""
from abc import ABC, abstractmethod
from decimal import Decimal
from statistics import median
from typing import Sequence

from .models import ModuleGrade


class RatingStrategy(ABC):
    @abstractmethod
    def calculate(self, grades: Sequence[ModuleGrade]) -> Decimal:
        """Вычислить аналитический показатель по непустому набору оценок."""


class AverageStrategy(RatingStrategy):
    """Средний балл по дисциплинам в выбранном модуле."""
    def calculate(self, grades: Sequence[ModuleGrade]) -> Decimal:
        if not grades:
            raise ValueError("Нет оценок для расчёта")
        return sum((Decimal(g.mark) for g in grades), Decimal(0)) / Decimal(len(grades))


class MedianStrategy(RatingStrategy):
    """Медианный балл по дисциплинам в выбранном модуле."""
    def calculate(self, grades: Sequence[ModuleGrade]) -> Decimal:
        if not grades:
            raise ValueError("Нет оценок для расчёта")
        return Decimal(str(median([g.mark for g in grades])))


class MinimumStrategy(RatingStrategy):
    """Наименьший балл среди дисциплин выбранного модуля."""
    def calculate(self, grades: Sequence[ModuleGrade]) -> Decimal:
        if not grades:
            raise ValueError("Нет оценок для расчёта")
        return Decimal(min(g.mark for g in grades))
