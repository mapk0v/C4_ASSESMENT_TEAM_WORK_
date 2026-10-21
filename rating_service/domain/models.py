from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ControlType(Enum):
    EXAM = "экзамен"
    CREDIT = "зачёт"
    COURSEWORK = "курсовая"


@dataclass(frozen=True)
class Student:
    id: str
    full_name: str
    group_id: str


@dataclass(frozen=True)
class Grade:
    student_id: str
    discipline_id: str
    value: int
    control_type: ControlType

    def __post_init__(self) -> None:
        if not 2 <= self.value <= 5:
            raise ValueError(f"Недопустимая оценка: {self.value}")


@dataclass(frozen=True)
class AssessmentResult:
    student_id: str
    period: str
    avg_grade: float
    debt_count: int
    is_at_risk: bool
    risk_reason: str