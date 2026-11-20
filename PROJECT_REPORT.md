# CSE402 Project Report
## Student Result Manager

### 1. Introduction
Student Result Manager is a Python command-line application designed to help a teacher record student and course information, enter marks, calculate grades and grade points, calculate credit-weighted CGPA and display student result sheets.

### 2. Objectives
- Maintain student records with unique Student IDs.
- Maintain course code, title and credit information.
- Validate marks within the 0–100 range.
- Automatically calculate letter grades and grade points.
- Calculate credit-weighted CGPA.
- Display an organized student result sheet.

### 3. Tools and Technologies
- Programming language: Python
- Data storage: JSON file
- Testing: Python `unittest`
- Design: UML (PlantUML source)

### 4. Functional Requirements
The application implements the six functional requirements in the assignment. Student IDs and course codes must be unique. Marks outside 0–100 are rejected. Grade conversion follows the assignment grading table. CGPA is weighted by course credits.

### 5. System Design
- `main.py`: command-line menu and user interaction.
- `student_manager.py`: student, course and mark manager, JSON persistence and result generation.
- `grading.py`: grade and grade-point conversion.
- `cgpa.py`: weighted CGPA calculation.
- `tests/`: automated test cases.
- `UML/`: use-case, class and activity diagrams.

### 6. CGPA Calculation
CGPA is calculated using:

`CGPA = Σ(Credit × Grade Point) / Σ(Credit)`

Only courses with entered marks are included. An F grade contributes 0.00 points and is included in the calculation.

### 7. Testing
Automated tests (19 cases) cover grade boundaries, decimal and invalid marks, weighted CGPA, F-grade handling, invalid credits, duplicate student IDs and course codes, mark updates, unknown student/course IDs, JSON persistence and malformed saved data.

Run the tests with:

`python -m unittest discover -s tests -v`

### 8. Limitations and Future Improvements
- The current version is a command-line application.
- JSON is used for local storage; a database can be added in a future version.
- Authentication, editing/deleting records, PDF export and a graphical interface can be added later.

### 9. Conclusion
Student Result Manager fulfills the assignment's stated functional requirements and includes UML source diagrams, automated tests and GitHub repository instructions.
