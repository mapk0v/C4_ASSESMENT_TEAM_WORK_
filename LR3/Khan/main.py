"""Демонстрация двух независимых модулей на шести дисциплинах ИДБ-23-12."""
from rating import (DISCIPLINES, AverageStrategy, MedianStrategy, MinimumStrategy,
                    ModuleGrade, ModuleNumber, RatingCalculator, Student)


def main() -> None:
    student = Student("S-001", "Иванов Иван (пример)")
    academic_year = "2026/2027"
    first = (48, 35, 22, 39, 30, 45)
    second = (42, 51, 46, 44, 24, 48)
    grades = [
        ModuleGrade(student.student_id, discipline.code, academic_year, module, mark)
        for module, marks in ((ModuleNumber.FIRST, first), (ModuleNumber.SECOND, second))
        for discipline, mark in zip(DISCIPLINES, marks)
    ]
    print("Демонстрационные данные, НЕ реальные оценки студентов МГТУ «СТАНКИН»")
    calculator = RatingCalculator(AverageStrategy())
    for module in ModuleNumber:
        print(f"\nМОДУЛЬ {module.value}")
        for discipline in DISCIPLINES:
            grade = next(g for g in grades if g.module == module and g.discipline_code == discipline.code)
            print(f"  {discipline.name}: {grade.mark}/54 — {grade.category.value}")
        for strategy in (AverageStrategy(), MedianStrategy(), MinimumStrategy()):
            calculator.set_strategy(strategy)
            result = calculator.calculate_rating(student, academic_year, module, grades)
            print(f"  {result.strategy}: {result.score}/54; не сдано: {result.not_passed_count}")
    print("\nСреднее, медиана и минимум — учебные аналитические показатели, не официальные оценки вуза.")


if __name__ == "__main__":
    main()
