"""Credit-weighted CGPA calculation."""

import math
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP


def _to_decimal(value, field_name):
    if isinstance(value, bool):
        raise ValueError(f"{field_name} must be a valid number.")
    try:
        number = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError) as exc:
        raise ValueError(f"{field_name} must be a valid number.") from exc
    if not number.is_finite():
        raise ValueError(f"{field_name} must be a finite number.")
    return number


def calculate_cgpa(course_results):
    """Return (CGPA rounded to 2 decimals, total credits).

    Each course result must contain positive 'credit' and 'grade_point'
    between 0.00 and 4.00. Courses with F grade (0.00 point) are included.
    """
    rows = list(course_results)
    if not rows:
        raise ValueError("CGPA cannot be calculated because no course results exist.")

    total_credits = Decimal("0")
    weighted_points = Decimal("0")

    for index, item in enumerate(rows, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"Course result #{index} is invalid.")

        if "credit" not in item or "grade_point" not in item:
            raise ValueError(f"Course result #{index} is missing credit or grade point.")

        credit = _to_decimal(item["credit"], "Credit")
        grade_point = _to_decimal(item["grade_point"], "Grade point")

        if credit <= 0:
            raise ValueError("Course credit must be greater than zero.")
        if not Decimal("0") <= grade_point <= Decimal("4"):
            raise ValueError("Grade point must be between 0.00 and 4.00.")

        total_credits += credit
        weighted_points += credit * grade_point

    cgpa = (weighted_points / total_credits).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )
    return float(cgpa), float(total_credits)
