import json
import tempfile
import unittest
from pathlib import Path

from student_manager import StudentResultManager


class TestStudentResultManager(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.data_file = Path(self.temp_dir.name) / "records.json"
        self.manager = StudentResultManager(self.data_file)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_add_student_and_duplicate_id(self):
        self.manager.add_student("101", "Rahim")
        with self.assertRaises(ValueError):
            self.manager.add_student("101", "Karim")

    def test_add_course_and_duplicate_course(self):
        self.manager.add_course("cse401", "Software Engineering", 3)
        with self.assertRaises(ValueError):
            self.manager.add_course("CSE401", "Another title", 3)

    def test_add_course_rejects_invalid_credit(self):
        for credit in (0, -1, float("nan"), float("inf"), "abc"):
            with self.subTest(credit=credit), self.assertRaises(ValueError):
                self.manager.add_course("CSE401", "Software Engineering", credit)

    def test_marks_grade_cgpa_and_result(self):
        self.manager.add_student("101", "Rahim")
        self.manager.add_course("CSE401", "Software Engineering", 3)
        self.manager.enter_marks("101", "CSE401", 85)
        result = self.manager.get_result_sheet("101")
        self.assertEqual(result["courses"][0]["grade"], "A+")
        self.assertEqual(result["cgpa"], 4.00)
        self.assertFalse(result["has_failed"])

    def test_marks_can_be_updated(self):
        self.manager.add_student("101", "Rahim")
        self.manager.add_course("CSE401", "Software Engineering", 3)
        self.manager.enter_marks("101", "CSE401", 65)
        self.manager.enter_marks("101", "CSE401", 85)
        result = self.manager.get_result_sheet("101")
        self.assertEqual(len(result["courses"]), 1)
        self.assertEqual(result["courses"][0]["marks"], 85.0)
        self.assertEqual(result["courses"][0]["grade"], "A+")

    def test_invalid_marks_do_not_save(self):
        self.manager.add_student("101", "Rahim")
        self.manager.add_course("CSE401", "Software Engineering", 3)
        with self.assertRaises(ValueError):
            self.manager.enter_marks("101", "CSE401", 101)
        self.assertEqual(self.manager.marks, {})

    def test_unknown_student_and_course(self):
        with self.assertRaises(KeyError):
            self.manager.enter_marks("999", "CSE401", 50)
        self.manager.add_student("101", "Rahim")
        with self.assertRaises(KeyError):
            self.manager.enter_marks("101", "CSE999", 50)

    def test_data_persists_after_restart(self):
        self.manager.add_student("101", "Rahim")
        self.manager.add_course("CSE401", "Software Engineering", 3)
        self.manager.enter_marks("101", "CSE401", 85)
        reloaded = StudentResultManager(self.data_file)
        self.assertEqual(reloaded.get_result_sheet("101")["cgpa"], 4.0)

    def test_invalid_json_is_reported(self):
        self.data_file.write_text("{invalid json", encoding="utf-8")
        with self.assertRaises(ValueError):
            StudentResultManager(self.data_file)



    def test_sample_style_credit_weighted_result(self):
        self.manager.add_student("101", "Rahim")
        course_data = [
            ("CSE401", "Software Engineering", 3, 85),
            ("CSE402", "Project", 3, 78),
            ("CSE403", "Database", 3, 65),
            ("MAT401", "Mathematics", 2, 90),
        ]
        for code, title, credit, marks in course_data:
            self.manager.add_course(code, title, credit)
            self.manager.enter_marks("101", code, marks)

        result = self.manager.get_result_sheet("101")
        self.assertEqual(result["total_credits"], 11.0)
        self.assertEqual(result["cgpa"], 3.73)
        self.assertEqual(len(result["courses"]), 4)

    def test_non_numeric_marks_are_rejected(self):
        self.manager.add_student("101", "Rahim")
        self.manager.add_course("CSE401", "Software Engineering", 3)
        for mark in ("abc", None, True):
            with self.subTest(mark=mark), self.assertRaises(ValueError):
                self.manager.enter_marks("101", "CSE401", mark)
        self.assertEqual(self.manager.marks, {})


    def test_result_sheet_applies_complete_assignment_grading_scale(self):
        self.manager.add_student("200", "Grade Scale Test")
        cases = [
            ("C001", 3, 100, "A+", 4.00),
            ("C002", 3, 80, "A+", 4.00),
            ("C003", 3, 79, "A", 3.75),
            ("C004", 3, 74, "A-", 3.50),
            ("C005", 3, 69, "B+", 3.25),
            ("C006", 3, 64, "B", 3.00),
            ("C007", 3, 59, "B-", 2.75),
            ("C008", 3, 54, "C+", 2.50),
            ("C009", 3, 49, "C", 2.25),
            ("C010", 3, 40, "D", 2.00),
            ("C011", 3, 39, "F", 0.00),
            ("C012", 3, 0, "F", 0.00),
        ]
        for code, credit, mark, expected_grade, expected_point in cases:
            self.manager.add_course(code, f"Course {code}", credit)
            self.manager.enter_marks("200", code, mark)

        result = self.manager.get_result_sheet("200")
        actual = {
            row["course_code"]: (row["grade"], row["grade_point"])
            for row in result["courses"]
        }
        for code, _, _, expected_grade, expected_point in cases:
            self.assertEqual(actual[code], (expected_grade, expected_point))

    def test_result_sheet_calculates_credit_weighted_cgpa_not_simple_average(self):
        self.manager.add_student("201", "Weighted CGPA Test")
        self.manager.add_course("HIGH", "High Credit Course", 3)
        self.manager.add_course("LOW", "Low Credit Course", 1)
        self.manager.enter_marks("201", "HIGH", 85)  # A+ = 4.00
        self.manager.enter_marks("201", "LOW", 35)   # F = 0.00

        result = self.manager.get_result_sheet("201")
        # (3 * 4.00 + 1 * 0.00) / (3 + 1) = 3.00
        self.assertEqual(result["total_credits"], 4.0)
        self.assertEqual(result["cgpa"], 3.00)
        self.assertTrue(result["has_failed"])


if __name__ == "__main__":
    unittest.main()
