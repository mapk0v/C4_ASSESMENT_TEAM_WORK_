from __future__ import annotations

from domain.models import AssessmentResult, Grade, Student
from domain.strategies.rating import RatingStrategy
from domain.strategies.risk import RiskDetectionStrategy


class RatingService:
    def __init__(
        self,
        rating_strategy: RatingStrategy,
        risk_strategy: RiskDetectionStrategy,
    ) -> None:
        self._rating_strategy = rating_strategy
        self._risk_strategy = risk_strategy

    def set_rating_strategy(self, strategy: RatingStrategy) -> None:
        self._rating_strategy = strategy

    def set_risk_strategy(self, strategy: RiskDetectionStrategy) -> None:
        self._risk_strategy = strategy

    def calculate_rating(self, grades: list[Grade]) -> float:
        return self._rating_strategy.calculate(grades)

    def evaluate_risk(self, grades: list[Grade]) -> bool:
        return self._risk_strategy.is_at_risk(grades)

    def build_assessment_result(
        self,
        student: Student,
        period: str,
        grades: list[Grade],
    ) -> AssessmentResult:
        return AssessmentResult(
            student_id=student.id,
            period=period,
            avg_grade=self.calculate_rating(grades),
            debt_count=self._risk_strategy.get_debt_count(grades),
            is_at_risk=self.evaluate_risk(grades),
            risk_reason=self._risk_strategy.get_risk_reason(grades),
        )