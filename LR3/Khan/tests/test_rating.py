import unittest
from decimal import Decimal

from rating import (DISCIPLINES, AverageStrategy, GradeCategory, MedianStrategy,
                    MinimumStrategy, ModuleGrade, ModuleNumber, RatingCalculator,
                    RatingStrategy, Student, classify_mark)


class TestRatingCalculator(unittest.TestCase):
    def setUp(self) -> None:
        self.student = Student("S1", "Тестовый студент")
        self.year = "2026/2027"
        self.grades = [
            ModuleGrade("S1", d.code, self.year, ModuleNumber.FIRST, x)
            for d, x in zip(DISCIPLINES, [48, 35, 22, 39, 30, 45])
        ] + [
            ModuleGrade("S1", d.code, self.year, ModuleNumber.SECOND, x)
            for d, x in zip(DISCIPLINES, [42, 51, 46, 44, 24, 48])
        ]

    def test_boundaries(self) -> None:
        expected = {0: GradeCategory.FAILED, 24: GradeCategory.FAILED,
                    25: GradeCategory.SATISFACTORY, 34: GradeCategory.SATISFACTORY,
                    35: GradeCategory.GOOD, 44: GradeCategory.GOOD,
                    45: GradeCategory.EXCELLENT, 54: GradeCategory.EXCELLENT}
        for score, category in expected.items():
            with self.subTest(score=score):
                self.assertEqual(classify_mark(score), category)

    def test_reject_invalid_marks(self) -> None:
        for mark in [-1, 55, 2.5, True, "45"]:
            with self.subTest(mark=mark), self.assertRaises(ValueError):
                ModuleGrade("S1", "IB", self.year, ModuleNumber.FIRST, mark)

    def test_six_disciplines(self) -> None:
        self.assertEqual(len(DISCIPLINES), 6)
        self.assertEqual(len({d.code for d in DISCIPLINES}), 6)

    def test_modules_are_independent(self) -> None:
        c = RatingCalculator(AverageStrategy())
        one = c.calculate_rating(self.student, self.year, ModuleNumber.FIRST, self.grades)
        two = c.calculate_rating(self.student, self.year, ModuleNumber.SECOND, self.grades)
        self.assertEqual(one.score, Decimal("36.50"))
        self.assertEqual(two.score, Decimal("42.50"))
        self.assertEqual(one.not_passed_count, 1)
        self.assertEqual(two.not_passed_count, 1)

    def test_change_second_does_not_affect_first(self) -> None:
        c = RatingCalculator(AverageStrategy())
        before = c.calculate_rating(self.student, self.year, ModuleNumber.FIRST, self.grades)
        changed = [g for g in self.grades if g.module == ModuleNumber.FIRST]
        changed += [ModuleGrade("S1", d.code, self.year, ModuleNumber.SECOND, 54) for d in DISCIPLINES]
        after = c.calculate_rating(self.student, self.year, ModuleNumber.FIRST, changed)
        self.assertEqual(before, after)

    def test_strategy_median(self) -> None:
        c = RatingCalculator(MedianStrategy())
        self.assertEqual(c.calculate_rating(self.student, self.year, ModuleNumber.FIRST, self.grades).score, Decimal("37.00"))

    def test_strategy_minimum(self) -> None:
        c = RatingCalculator(MinimumStrategy())
        self.assertEqual(c.calculate_rating(self.student, self.year, ModuleNumber.FIRST, self.grades).score, Decimal("22.00"))

    def test_strategy_switch(self) -> None:
        c = RatingCalculator(AverageStrategy())
        a = c.calculate_rating(self.student, self.year, ModuleNumber.FIRST, self.grades)
        c.set_strategy(MinimumStrategy())
        b = c.calculate_rating(self.student, self.year, ModuleNumber.FIRST, self.grades)
        self.assertNotEqual(a.score, b.score)
        self.assertEqual(a.not_passed_count, b.not_passed_count)

    def test_one_module_can_be_unsuccessful_independently(self) -> None:
        rows = [ModuleGrade("S1", "IB", self.year, ModuleNumber.FIRST, 24),
                ModuleGrade("S1", "IB", self.year, ModuleNumber.SECOND, 54)]
        c = RatingCalculator(AverageStrategy())
        self.assertEqual(c.calculate_rating(self.student, self.year, ModuleNumber.FIRST, rows).not_passed_count, 1)
        self.assertEqual(c.calculate_rating(self.student, self.year, ModuleNumber.SECOND, rows).not_passed_count, 0)

    def test_reject_duplicate_subject(self) -> None:
        c = RatingCalculator(AverageStrategy())
        with self.assertRaises(ValueError):
            c.calculate_rating(self.student, self.year, ModuleNumber.FIRST, self.grades + [self.grades[0]])

    def test_reject_missing_module(self) -> None:
        c = RatingCalculator(AverageStrategy())
        with self.assertRaises(ValueError):
            c.calculate_rating(self.student, "2025/2026", ModuleNumber.FIRST, self.grades)

    def test_other_student_is_ignored(self) -> None:
        c = RatingCalculator(AverageStrategy())
        extra = ModuleGrade("OTHER", "IB", self.year, ModuleNumber.FIRST, 0)
        a = c.calculate_rating(self.student, self.year, ModuleNumber.FIRST, self.grades)
        b = c.calculate_rating(self.student, self.year, ModuleNumber.FIRST, self.grades + [extra])
        self.assertEqual(a, b)

    def test_no_grade_assumed_for_missing_subject(self) -> None:
        c = RatingCalculator(AverageStrategy())
        first_row = self.grades[:1]
        result = c.calculate_rating(self.student, self.year, ModuleNumber.FIRST, first_row)
        self.assertEqual(result.graded_count, 1)
        self.assertEqual(result.score, Decimal("48.00"))

    def test_incorrect_module_type(self) -> None:
        with self.assertRaises(ValueError):
            ModuleGrade("S1", "IB", self.year, 1, 25)

    def test_strategy_bounds_enforced(self) -> None:
        class BadStrategy(RatingStrategy):
            def calculate(self, grades):
                return Decimal("55")
        with self.assertRaises(ValueError):
            RatingCalculator(BadStrategy()).calculate_rating(self.student, self.year, ModuleNumber.FIRST, self.grades)


if __name__ == "__main__":
    unittest.main()
