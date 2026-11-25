"""Компонент rating_calc: контекст паттерна Strategy."""
from decimal import Decimal, ROUND_HALF_UP
from typing import Sequence

from .models import ModuleGrade, ModuleNumber, RatingSummary, Student
from .strategies import RatingStrategy


class RatingCalculator:
    def __init__(self, strategy: RatingStrategy) -> None:
        self._strategy = strategy

    def set_strategy(self, strategy: RatingStrategy) -> None:
        self._strategy = strategy

    def calculate_rating(
        self,
        student: Student,
        academic_year: str,
        module: ModuleNumber,
        grades: Sequence[ModuleGrade],
    ) -> RatingSummary:
        """Фильтрует оценки строго по одному модулю; данные другого не смешиваются."""
        if not academic_year.strip():
            raise ValueError("Учебный год обязателен")
        if type(module) is not ModuleNumber:
            raise ValueError("Некорректный модуль")
        relevant = [g for g in grades if g.student_id == student.student_id
                    and g.academic_year == academic_year and g.module == module]
        if not relevant:
            raise ValueError("Нет оценок студента за выбранный модуль")
        codes = [g.discipline_code for g in relevant]
        if len(codes) != len(set(codes)):
            raise ValueError("Дублирующиеся оценки за одну дисциплину и модуль")
        raw_score = self._strategy.calculate(relevant)
        if not isinstance(raw_score, Decimal) or not raw_score.is_finite() or not Decimal(0) <= raw_score <= Decimal(54):
            raise ValueError("Стратегия должна вернуть Decimal от 0 до 54")
        return RatingSummary(
            student_id=student.student_id,
            academic_year=academic_year,
            module=module,
            strategy=type(self._strategy).__name__,
            score=raw_score.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
            graded_count=len(relevant),
            not_passed_count=sum(g.not_passed for g in relevant),
        )
