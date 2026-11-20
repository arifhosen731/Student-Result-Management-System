"""Convert marks into letter grades and grade points."""

import math

# Minimum mark required for each grade, following the assignment scale.
GRADE_SCALE = (
    (80, "A+", 4.00),
    (75, "A", 3.75),
    (70, "A-", 3.50),
    (65, "B+", 3.25),
    (60, "B", 3.00),
    (55, "B-", 2.75),
    (50, "C+", 2.50),
    (45, "C", 2.25),
    (40, "D", 2.00),
    (0, "F", 0.00),
)


def calculate_grade(mark):
    """Return (letter_grade, grade_point) for marks from 0 through 100.

    Decimal marks are supported. For example, 79.5 receives grade A.
    """
    if isinstance(mark, bool):
        raise ValueError("Marks must be a number between 0 and 100.")

    try:
        mark = float(mark)
    except (TypeError, ValueError) as exc:
        raise ValueError("Marks must be a valid number.") from exc

    if not math.isfinite(mark):
        raise ValueError("Marks must be a finite number.")
    if not 0 <= mark <= 100:
        raise ValueError("Marks must be between 0 and 100.")

    for minimum, grade, point in GRADE_SCALE:
        if mark >= minimum:
            return grade, point

    # The range validation above makes this a defensive fallback.
    raise ValueError("Unable to calculate grade.")
