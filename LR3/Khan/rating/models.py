"""Доменная модель оценок по независимым модулям (0–54 балла)."""
from dataclasses import dataclass
from decimal import Decimal
from enum import Enum, IntEnum


class ModuleNumber(IntEnum):
    FIRST = 1
    SECOND = 2


class GradeCategory(str, Enum):
    EXCELLENT = "отлично"
    GOOD = "хорошо"
    SATISFACTORY = "удовлетворительно"
    FAILED = "не сдал"


def classify_mark(mark: int) -> GradeCategory:
    """Пороговые интервалы, сообщённые студентом (включая границы)."""
    if type(mark) is not int or not 0 <= mark <= 54:
        raise ValueError("Балл должен быть целым числом от 0 до 54")
    if mark >= 45:
        return GradeCategory.EXCELLENT
    if mark >= 35:
        return GradeCategory.GOOD
    if mark >= 25:
        return GradeCategory.SATISFACTORY
    return GradeCategory.FAILED


@dataclass(frozen=True)
class Student:
    student_id: str
    full_name: str

    def __post_init__(self) -> None:
        if not self.student_id.strip() or not self.full_name.strip():
            raise ValueError("Данные студента обязательны")


@dataclass(frozen=True)
class Discipline:
    code: str
    name: str

    def __post_init__(self) -> None:
        if not self.code.strip() or not self.name.strip():
            raise ValueError("Код и название дисциплины обязательны")


@dataclass(frozen=True)
class ModuleGrade:
    """Одна самостоятельная оценка: студент + дисциплина + модуль + год."""
    student_id: str
    discipline_code: str
    academic_year: str
    module: ModuleNumber
    mark: int

    def __post_init__(self) -> None:
        if not self.student_id.strip() or not self.discipline_code.strip() or not self.academic_year.strip():
            raise ValueError("Идентификаторы и учебный год обязательны")
        if type(self.module) is not ModuleNumber:
            raise ValueError("Номер модуля должен быть FIRST или SECOND")
        classify_mark(self.mark)

    @property
    def category(self) -> GradeCategory:
        return classify_mark(self.mark)

    @property
    def not_passed(self) -> bool:
        return self.mark < 25


@dataclass(frozen=True)
class RatingSummary:
    """Описательный аналитический показатель, НЕ официальная оценка по предмету."""
    student_id: str
    academic_year: str
    module: ModuleNumber
    strategy: str
    score: Decimal
    graded_count: int
    not_passed_count: int
