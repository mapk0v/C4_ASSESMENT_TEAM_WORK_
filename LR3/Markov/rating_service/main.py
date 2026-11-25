from domain.models import ControlType, Grade, Student
from domain.services.rating_service import RatingService
from domain.strategies.rating import (
    GpaStrategy,
    SimpleAverageStrategy,
    WeightedGradeStrategy,
)
from domain.strategies.risk import DebtCountStrategy, LowGradeStrategy


def main() -> None:
    student = Student(id="S-001", full_name="Иванов И.И.", group_id="ИДБ-23-12")
    grades = [
        Grade(student.id, "D1", 5, ControlType.EXAM),
        Grade(student.id, "D2", 3, ControlType.CREDIT),
        Grade(student.id, "D3", 2, ControlType.EXAM),
    ]

    service = RatingService(
        rating_strategy=SimpleAverageStrategy(),
        risk_strategy=DebtCountStrategy(max_debts=1),
    )

    print("Сценарий 1 — простое среднее, риск по долгам:")
    print(service.build_assessment_result(student, "2025-1", grades))

    service.set_rating_strategy(WeightedGradeStrategy())
    service.set_risk_strategy(LowGradeStrategy(avg_threshold=3.5))
    print("\nСценарий 2 — взвешенный балл, риск по среднему < 3.5:")
    print(service.build_assessment_result(student, "2025-1", grades))

    service.set_rating_strategy(GpaStrategy())
    print("\nСценарий 3 — рейтинг в формате GPA:")
    print(f"GPA = {service.calculate_rating(grades)}")


if __name__ == "__main__":
    main()