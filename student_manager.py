"""Business logic and JSON persistence for Student Result Manager."""

import json
import math
import os
import tempfile
from pathlib import Path

from cgpa import calculate_cgpa
from grading import calculate_grade


class StudentResultManager:
    """Manage student records, courses, marks and result sheets."""

    def __init__(self, data_file=None):
        # Keep the data folder beside this source file, regardless of the
        # terminal's current working directory.
        project_dir = Path(__file__).resolve().parent
        self.data_file = Path(data_file) if data_file is not None else project_dir / "data" / "records.json"
        self.data_file.parent.mkdir(parents=True, exist_ok=True)

        self.students = {}
        self.courses = {}
        self.marks = {}
        self._load()

    def _load(self):
        """Load saved data and reject malformed JSON structures clearly."""
        if not self.data_file.exists():
            return

        try:
            data = json.loads(self.data_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            raise ValueError(f"Could not read saved data file: {exc}") from exc

        if not isinstance(data, dict):
            raise ValueError("Saved data is invalid: the root must be a JSON object.")

        for key in ("students", "courses", "marks"):
            if key not in data or not isinstance(data[key], dict):
                raise ValueError(f"Saved data is invalid: '{key}' must be an object.")

        self.students = data["students"]
        self.courses = data["courses"]
        self.marks = data["marks"]

    def _save(self):
        """Write JSON safely so an interrupted write does not corrupt the file."""
        data = {
            "students": self.students,
            "courses": self.courses,
            "marks": self.marks,
        }
        temp_path = None

        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=self.data_file.parent,
                prefix=f".{self.data_file.name}.",
                suffix=".tmp",
                delete=False,
            ) as temp_file:
                json.dump(data, temp_file, indent=4, ensure_ascii=False)
                temp_file.write("\n")
                temp_path = Path(temp_file.name)

            os.replace(temp_path, self.data_file)
        except OSError as exc:
            if temp_path is not None:
                temp_path.unlink(missing_ok=True)
            raise ValueError(f"Could not save data: {exc}") from exc

    @staticmethod
    def _normalise_text(value, field_name):
        text = str(value).strip()
        if not text:
            raise ValueError(f"{field_name} cannot be empty.")
        return text

    @staticmethod
    def _positive_credit(value):
        if isinstance(value, bool):
            raise ValueError("Course credit must be a positive number.")
        try:
            credit = float(value)
        except (TypeError, ValueError) as exc:
            raise ValueError("Course credit must be a valid number.") from exc

        if not math.isfinite(credit) or credit <= 0:
            raise ValueError("Course credit must be a finite number greater than zero.")
        return credit

    def add_student(self, student_id, name):
        student_id = self._normalise_text(student_id, "Student ID")
        name = self._normalise_text(name, "Student name")

        if student_id in self.students:
            raise ValueError(f"Student ID '{student_id}' already exists.")

        self.students[student_id] = {
            "student_id": student_id,
            "name": name,
        }
        self._save()

    def add_course(self, course_code, title, credit):
        course_code = self._normalise_text(course_code, "Course code").upper()
        title = self._normalise_text(title, "Course title")
        credit = self._positive_credit(credit)

        if course_code in self.courses:
            raise ValueError(f"Course '{course_code}' already exists.")

        self.courses[course_code] = {
            "course_code": course_code,
            "title": title,
            "credit": credit,
        }
        self._save()

    def enter_marks(self, student_id, course_code, mark):
        student_id = self._normalise_text(student_id, "Student ID")
        course_code = self._normalise_text(course_code, "Course code").upper()

        if student_id not in self.students:
            raise KeyError(f"Student ID '{student_id}' was not found.")
        if course_code not in self.courses:
            raise KeyError(f"Course '{course_code}' was not found.")

        if isinstance(mark, bool):
            raise ValueError("Marks must be a valid number between 0 and 100.")
        try:
            numeric_mark = float(mark)
        except (TypeError, ValueError) as exc:
            raise ValueError("Marks must be a valid number between 0 and 100.") from exc

        grade, point = calculate_grade(numeric_mark)

        self.marks.setdefault(student_id, {})[course_code] = {
            "marks": numeric_mark,
            "grade": grade,
            "grade_point": point,
        }
        self._save()

    def list_students(self):
        return [
            self.students[key]
            for key in sorted(self.students, key=lambda item: str(item).casefold())
        ]

    def list_courses(self):
        return [
            self.courses[key]
            for key in sorted(self.courses, key=lambda item: str(item).casefold())
        ]

    def get_result_sheet(self, student_id):
        student_id = self._normalise_text(student_id, "Student ID")

        if student_id not in self.students:
            raise KeyError(f"Student ID '{student_id}' was not found.")

        recorded_marks = self.marks.get(student_id, {})
        if not recorded_marks:
            raise ValueError("No marks have been entered for this student.")

        course_rows = []
        for course_code in sorted(recorded_marks):
            if course_code not in self.courses:
                raise ValueError(
                    f"Saved marks refer to unknown course '{course_code}'. "
                    "Please check the data file."
                )

            saved_result = recorded_marks[course_code]
            if not isinstance(saved_result, dict) or "marks" not in saved_result:
                raise ValueError(f"Saved marks for course '{course_code}' are invalid.")

            mark = saved_result["marks"]
            grade, point = calculate_grade(mark)
            course = self.courses[course_code]

            course_rows.append({
                "course_code": course_code,
                "course_title": course["title"],
                "credit": course["credit"],
                "marks": float(mark),
                "grade": grade,
                "grade_point": point,
            })

        cgpa, total_credits = calculate_cgpa(course_rows)

        return {
            "student_id": student_id,
            "student_name": self.students[student_id]["name"],
            "courses": course_rows,
            "total_credits": total_credits,
            "cgpa": cgpa,
            "has_failed": any(row["grade"] == "F" for row in course_rows),
        }
