# Assignment Requirement Traceability

This checklist maps the CSE402 Project Idea requirements to the implementation.

| Requirement in assignment | Implementation | Verification |
|---|---|---|
| Add a student with ID and name; IDs must be unique | `student_manager.py` → `add_student()` | `tests/test_student_manager.py` |
| Add a course with code, title and credit | `student_manager.py` → `add_course()` | `tests/test_student_manager.py` |
| Enter marks out of 100; reject below 0 or above 100 | `student_manager.py` → `enter_marks()` and `grading.py` → `calculate_grade()` | `tests/test_grading.py`, `tests/test_student_manager.py` |
| Calculate letter grade and grade point using the given scale | `grading.py` → `GRADE_SCALE`, `calculate_grade()` | `tests/test_grading.py`; integration check in `tests/test_student_manager.py` verifies the full scale in a result sheet |
| Calculate CGPA weighted by course credits | `cgpa.py` → `calculate_cgpa()` | `tests/test_cgpa.py`; integration check in `tests/test_student_manager.py` verifies credit weighting in a result sheet |
| Show result sheet with course, mark, grade, point and CGPA | `main.py` → `print_result()`; `student_manager.py` → `get_result_sheet()` | `tests/test_student_manager.py` |
| UML | `UML/*.puml` and `UML/rendered/*.svg` | Open the SVG diagrams or render the PlantUML source |
| GitHub repository | GitHub upload guide in `GITHUB_UPLOAD_GUIDE.md` | Must be published to the student's own GitHub account |
| Testing codes | `tests/` | Run the unittest command in README |

## CGPA calculation note

The application includes only courses for which marks have been entered. Each included course is weighted by its credit. An F grade contributes 0.00 grade points. The result sheet reports FAIL if any recorded course has an F grade.

The demo data in `data/records.json` has a CGPA of 3.73. The separate CGPA unit-test example uses a different set of grade points and correctly expects 3.64.
