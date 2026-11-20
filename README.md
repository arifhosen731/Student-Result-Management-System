# Student Result Manager (CSE402)

A Python command-line application that allows a teacher to manage student records, courses, marks, grades, grade points and credit-weighted CGPA.

## Assignment requirements covered

1. Add students with unique Student IDs.
2. Add courses with a course code, title and credit value.
3. Enter or update marks for a student in a course; marks outside 0–100 are rejected.
4. Calculate letter grades and grade points using the assignment's grading scale.
5. Calculate CGPA weighted by course credits.
6. Display a student result sheet with course, mark, grade, grade point and CGPA.
7. Include UML source diagrams, a GitHub-ready structure and automated tests.

## Requirements

- Python 3.9 or later
- No third-party packages required

## Run the application

Open this project folder in VS Code. Open **Terminal → New Terminal**, then run:

```bash
python main.py
```

The application stores its data in `data/records.json`, located beside `student_manager.py`. Data is saved automatically.

The included `data/records.json` contains demo data for Student ID `101` (Rahim). Use menu option 6 and enter `101` to view the sample result. If you want a fresh start, back up and replace the JSON file with:

```json
{
    "students": {},
    "courses": {},
    "marks": {}
}
```

## Run automated tests

From the project root folder:

```bash
python -m unittest discover -s tests -v
```

## Grading scale

| Marks | Grade | Grade Point |
|---|---|---:|
| 80–100 | A+ | 4.00 |
| 75–79 | A | 3.75 |
| 70–74 | A- | 3.50 |
| 65–69 | B+ | 3.25 |
| 60–64 | B | 3.00 |
| 55–59 | B- | 2.75 |
| 50–54 | C+ | 2.50 |
| 45–49 | C | 2.25 |
| 40–44 | D | 2.00 |
| 0–39 | F | 0.00 |

For decimal marks, the lower boundary of each grade band is used (for example, 79.5 receives A).

## CGPA formula

`CGPA = Sum(Credit × Grade Point) / Sum(Credit)`

Only courses with entered marks are included. An F grade contributes 0.00 grade points and remains included in the credit-weighted CGPA. The result sheet reports FAIL if at least one recorded course has an F grade.

## Project structure

```text
Student_Result_Manager/
├── main.py
├── student_manager.py
├── grading.py
├── cgpa.py
├── data/
│   ├── records.json
│   └── README.txt
├── tests/
│   ├── test_student_manager.py
│   ├── test_grading.py
│   └── test_cgpa.py
├── UML/
│   ├── use_case.puml
│   ├── class_diagram.puml
│   └── activity_diagram.puml
├── README.md
└── PROJECT_REPORT.md
```

## UML diagrams

PlantUML source files are in the `UML/` folder. They can be rendered with PlantUML or a compatible VS Code extension.

## Upload to GitHub

Create an empty GitHub repository, then run these commands from the project root (replace the URL with your own repository URL):

```bash
git init
git add .
git commit -m "Initial Student Result Manager project"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/Student_Result_Manager.git
git push -u origin main
```


## Assignment submission checklist

See `REQUIREMENT_TRACEABILITY.md` for a requirement-by-requirement mapping.
See `GITHUB_UPLOAD_GUIDE.md` for publishing this project to your own GitHub account.
The GitHub repository is not online until you complete those account-specific steps.

The test suite currently contains 19 automated test cases.
