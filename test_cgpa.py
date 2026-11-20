import unittest
from cgpa import calculate_cgpa


class TestCGPA(unittest.TestCase):
    def test_credit_weighted_cgpa(self):
        courses = [
            {"credit": 3, "grade_point": 4.00},
            {"credit": 3, "grade_point": 3.75},
            {"credit": 3, "grade_point": 3.25},
            {"credit": 2, "grade_point": 3.50},
        ]
        # (12 + 11.25 + 9.75 + 7) / 11 = 3.636..., rounded to 3.64
        self.assertEqual(calculate_cgpa(courses), (3.64, 11.0))

    def test_f_grade_is_included(self):
        courses = [
            {"credit": 3, "grade_point": 4.0},
            {"credit": 3, "grade_point": 0.0},
        ]
        self.assertEqual(calculate_cgpa(courses), (2.00, 6.0))

    def test_invalid_course_results(self):
        invalid_inputs = [
            [],
            [{"credit": 0, "grade_point": 3.0}],
            [{"credit": -1, "grade_point": 3.0}],
            [{"credit": 3, "grade_point": 4.5}],
            [{"credit": float("nan"), "grade_point": 3.0}],
            [{"credit": 3}],
        ]
        for courses in invalid_inputs:
            with self.subTest(courses=courses), self.assertRaises(ValueError):
                calculate_cgpa(courses)


if __name__ == "__main__":
    unittest.main()
