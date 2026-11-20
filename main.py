"""Command-line interface for Student Result Manager."""

from student_manager import StudentResultManager


def print_menu():
    print("\n===== STUDENT RESULT MANAGER =====")
    print("1. Add Student")
    print("2. Add Course")
    print("3. Enter/Update Student Marks")
    print("4. View All Students")
    print("5. View All Courses")
    print("6. Show Student Result Sheet")
    print("7. Exit")


def print_result(result):
    print("\n" + "=" * 78)
    print("                         STUDENT RESULT SHEET")
    print("=" * 78)
    print(f"Student ID   : {result['student_id']}")
    print(f"Student Name : {result['student_name']}")
    print("-" * 78)
    print(
        f"{'Course Code':<14}{'Course Title':<27}"
        f"{'Credit':>8}{'Marks':>8}{'Grade':>8}{'Point':>8}"
    )
    print("-" * 78)

    for item in result["courses"]:
        title = item["course_title"][:26]
        print(
            f"{item['course_code']:<14}{title:<27}"
            f"{item['credit']:>8.2f}{item['marks']:>8.2f}"
            f"{item['grade']:>8}{item['grade_point']:>8.2f}"
        )

    print("-" * 78)
    print(f"Total Credits: {result['total_credits']:.2f}")
    print(f"CGPA         : {result['cgpa']:.2f}")
    status = "FAIL (at least one course has F grade)" if result["has_failed"] else "PASS"
    print(f"Status       : {status}")
    print("=" * 78)


def main():
    manager = StudentResultManager()

    while True:
        print_menu()
        choice = input("Choose an option (1-7): ").strip()

        try:
            if choice == "1":
                student_id = input("Student ID: ").strip()
                name = input("Student Name: ").strip()
                manager.add_student(student_id, name)
                print("Student added successfully.")

            elif choice == "2":
                course_code = input("Course Code: ").strip().upper()
                title = input("Course Title: ").strip()
                credit = input("Credit: ").strip()
                manager.add_course(course_code, title, credit)
                print("Course added successfully.")

            elif choice == "3":
                student_id = input("Student ID: ").strip()
                course_code = input("Course Code: ").strip().upper()
                marks = input("Marks (0-100): ").strip()
                manager.enter_marks(student_id, course_code, marks)
                print("Marks saved successfully.")

            elif choice == "4":
                students = manager.list_students()
                if not students:
                    print("No students found.")
                else:
                    print("\nSTUDENT LIST")
                    for student in students:
                        print(f"{student['student_id']} - {student['name']}")

            elif choice == "5":
                courses = manager.list_courses()
                if not courses:
                    print("No courses found.")
                else:
                    print("\nCOURSE LIST")
                    for course in courses:
                        print(
                            f"{course['course_code']} - {course['title']} "
                            f"({course['credit']:g} credits)"
                        )

            elif choice == "6":
                student_id = input("Student ID: ").strip()
                print_result(manager.get_result_sheet(student_id))

            elif choice == "7":
                print("Thank you for using Student Result Manager.")
                break

            else:
                print("Invalid choice. Please select a number from 1 to 7.")

        except (ValueError, KeyError) as exc:
            print(f"Error: {exc}")
        except (EOFError, KeyboardInterrupt):
            print("\nApplication closed.")
            break


if __name__ == "__main__":
    main()
