from __future__ import annotations

from abc import ABC, abstractmethod

from domain.models import Grade


class RiskDetectionStrategy(ABC):
    @abstractmethod
    def is_at_risk(self, grades: list[Grade]) -> bool:
        ...

    @abstractmethod
    def get_risk_reason(self, grades: list[Grade]) -> str:
        ...

    @abstractmethod
    def get_debt_count(self, grades: list[Grade]) -> int:
        ...


class DebtCountStrategy(RiskDetectionStrategy):
    def __init__(self, max_debts: int = 1) -> None:
        self._max_debts = max_debts

    def get_debt_count(self, grades: list[Grade]) -> int:
        return sum(1 for g in grades if g.value == 2)

    def is_at_risk(self, grades: list[Grade]) -> bool:
        return self.get_debt_count(grades) >= self._max_debts

    def get_risk_reason(self, grades: list[Grade]) -> str:
        count = self.get_debt_count(grades)
        return f"Задолженностей: {count}" if count else ""


class LowGradeStrategy(RiskDetectionStrategy):
    def __init__(self, avg_threshold: float = 3.0) -> None:
        self._avg_threshold = avg_threshold

    def get_debt_count(self, grades: list[Grade]) -> int:
        return sum(1 for g in grades if g.value == 2)

    def is_at_risk(self, grades: list[Grade]) -> bool:
        if not grades:
            return False
        avg = sum(g.value for g in grades) / len(grades)
        return avg < self._avg_threshold

    def get_risk_reason(self, grades: list[Grade]) -> str:
        if not grades:
            return ""
        avg = round(sum(g.value for g in grades) / len(grades), 2)
        return f"Средний балл ниже {self._avg_threshold}: {avg}"