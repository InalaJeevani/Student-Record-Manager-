"""Input validation utilities and regex validators for Student Record Manager.

Enforces strict domain validation on emails, student IDs, names,
courses, and marks, raising granular custom exceptions upon violation.
"""

from __future__ import annotations

import re
from .exceptions import (
    InvalidEmailError,
    InvalidGradeError,
    InvalidNameError,
    InvalidStudentIdError,
    InvalidCourseError,
)


class StudentValidator:
    """Validator providing static methods to validate student attributes."""

    # RFC 5322 compatible regex for general email validation:
    # Requires standard alphanumeric characters, allowed symbols, @ symbol,
    # valid domain label, and a top-level domain of at least 2 characters.
    EMAIL_REGEX: re.Pattern[str] = re.compile(
        r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9]+(?:-[a-zA-Z0-9]+)*(?:\.[a-zA-Z0-9]+(?:-[a-zA-Z0-9]+)*)*\.[a-zA-Z]{2,}$"
    )

    # Student ID: 3-20 characters consisting of letters, digits, dashes, and underscores
    STUDENT_ID_REGEX: re.Pattern[str] = re.compile(r"^[A-Za-z0-9_-]{3,20}$")

    # Name: 2-60 characters, letters, spaces, hyphens, and apostrophes
    NAME_REGEX: re.Pattern[str] = re.compile(r"^[A-Za-z]+(?:[' -][A-Za-z]+)*$")

    @classmethod
    def validate_email(cls, email: str | None) -> str:
        """Validate an email address against regular expression standards.

        Args:
            email: Email address string to validate.

        Returns:
            Clean, lowercase validated email string.

        Raises:
            InvalidEmailError: If the email is empty or does not match regex pattern.
        """
        if not email or not isinstance(email, str):
            raise InvalidEmailError("<empty>", "Email cannot be empty or missing.")

        cleaned = email.strip()

        # Reject consecutive dots or invalid punctuation edges
        if ".." in cleaned or cleaned.startswith(".") or "@." in cleaned:
            raise InvalidEmailError(cleaned, f"Email '{cleaned}' contains improper dot placement.")

        if not cls.EMAIL_REGEX.match(cleaned):
            raise InvalidEmailError(
                cleaned,
                f"Email '{cleaned}' does not match standard pattern (e.g. user@domain.com).",
            )

        return cleaned.lower()

    @classmethod
    def validate_student_id(cls, student_id: str | None) -> str:
        """Validate a student ID format.

        Args:
            student_id: Student ID string to validate.

        Returns:
            Normalized uppercase student ID.

        Raises:
            InvalidStudentIdError: If student ID is invalid.
        """
        if not student_id or not isinstance(student_id, str):
            raise InvalidStudentIdError("<empty>", "Student ID cannot be empty.")

        cleaned = student_id.strip()
        if not cls.STUDENT_ID_REGEX.match(cleaned):
            raise InvalidStudentIdError(
                cleaned,
                f"Student ID '{cleaned}' is invalid. Must be 3-20 characters (alphanumeric, dashes, underscores).",
            )

        return cleaned.upper()

    @classmethod
    def validate_name(cls, name: str | None) -> str:
        """Validate a student's full name.

        Args:
            name: Student name to validate.

        Returns:
            Properly capitalized cleaned name.

        Raises:
            InvalidNameError: If name length or characters are invalid.
        """
        if not name or not isinstance(name, str):
            raise InvalidNameError("<empty>", "Student name cannot be empty.")

        cleaned = name.strip()
        if len(cleaned) < 2 or len(cleaned) > 60:
            raise InvalidNameError(
                cleaned,
                f"Student name '{cleaned}' must be between 2 and 60 characters long.",
            )

        if not cls.NAME_REGEX.match(cleaned):
            raise InvalidNameError(
                cleaned,
                f"Student name '{cleaned}' contains invalid characters. Only letters, spaces, hyphens, and apostrophes are allowed.",
            )

        # Normalize capitalization
        return " ".join(part.capitalize() for part in cleaned.split())

    @classmethod
    def validate_course(cls, course: str | None) -> str:
        """Validate a course or department name.

        Args:
            course: Course name to validate.

        Returns:
            Cleaned course name.

        Raises:
            InvalidCourseError: If course name is invalid or empty.
        """
        if not course or not isinstance(course, str):
            raise InvalidCourseError("<empty>", "Course name cannot be empty.")

        cleaned = course.strip()
        if len(cleaned) < 2 or len(cleaned) > 50:
            raise InvalidCourseError(
                cleaned,
                f"Course name '{cleaned}' must be between 2 and 50 characters long.",
            )

        return cleaned

    @classmethod
    def validate_marks(cls, marks: float | int | str | None) -> float:
        """Validate marks or score for a student.

        Args:
            marks: Numeric or string representation of marks (0.0 to 100.0).

        Returns:
            Float value rounded to 2 decimal places.

        Raises:
            InvalidGradeError: If marks cannot be parsed or are out of 0.0 - 100.0 bounds.
        """
        if marks is None:
            raise InvalidGradeError("<missing>", "Marks value cannot be empty.")

        try:
            num = float(marks)
        except (ValueError, TypeError):
            raise InvalidGradeError(marks, f"Marks '{marks}' is not a valid numeric score.")

        if num < 0.0 or num > 100.0:
            raise InvalidGradeError(
                num,
                f"Marks '{num}' is out of range. Score must be between 0.0 and 100.0.",
            )

        return round(num, 2)

    @classmethod
    def calculate_letter_grade(cls, marks: float) -> str:
        """Compute the corresponding letter grade based on marks.

        Args:
            marks: Numeric score between 0.0 and 100.0.

        Returns:
            Letter grade: A+, A, B, C, D, or F.
        """
        if marks >= 90.0:
            return "A+"
        elif marks >= 80.0:
            return "A"
        elif marks >= 70.0:
            return "B"
        elif marks >= 60.0:
            return "C"
        elif marks >= 50.0:
            return "D"
        else:
            return "F"
