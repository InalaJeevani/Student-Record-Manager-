"""Data models for Student Record Manager."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any
from .validator import StudentValidator


@dataclass
class Student:
    """Represents an individual student record."""

    student_id: str
    name: str
    email: str
    course: str
    marks: float
    grade: str = field(default="")
    created_at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    updated_at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def __post_init__(self) -> None:
        """Derive letter grade if not already populated."""
        if not self.grade:
            self.grade = StudentValidator.calculate_letter_grade(self.marks)

    @classmethod
    def create(
        cls,
        student_id: str,
        name: str,
        email: str,
        course: str,
        marks: float | int | str,
    ) -> Student:
        """Factory method to validate and instantiate a new Student object.

        Args:
            student_id: Unique student identifier.
            name: Full name.
            email: Email address (validated via regex).
            course: Course name.
            marks: Numerical marks (0.0 - 100.0).

        Returns:
            A validated Student instance.

        Raises:
            ValidationError: Subclass of ValidationError if any field is invalid.
        """
        valid_id = StudentValidator.validate_student_id(student_id)
        valid_name = StudentValidator.validate_name(name)
        valid_email = StudentValidator.validate_email(email)
        valid_course = StudentValidator.validate_course(course)
        valid_marks = StudentValidator.validate_marks(marks)
        letter_grade = StudentValidator.calculate_letter_grade(valid_marks)

        return cls(
            student_id=valid_id,
            name=valid_name,
            email=valid_email,
            course=valid_course,
            marks=valid_marks,
            grade=letter_grade,
        )

    def update(
        self,
        name: str | None = None,
        email: str | None = None,
        course: str | None = None,
        marks: float | int | str | None = None,
    ) -> None:
        """Update student fields with validation.

        Args:
            name: Optional new name.
            email: Optional new email.
            course: Optional new course.
            marks: Optional new marks.
        """
        if name is not None:
            self.name = StudentValidator.validate_name(name)
        if email is not None:
            self.email = StudentValidator.validate_email(email)
        if course is not None:
            self.course = StudentValidator.validate_course(course)
        if marks is not None:
            self.marks = StudentValidator.validate_marks(marks)
            self.grade = StudentValidator.calculate_letter_grade(self.marks)

        self.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self) -> dict[str, Any]:
        """Convert student record to dictionary representation for file persistence."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Student:
        """Reconstruct a Student instance from a dictionary representation.

        Args:
            data: Dictionary with student record fields.

        Returns:
            Student instance.
        """
        return cls(
            student_id=str(data.get("student_id", "")),
            name=str(data.get("name", "")),
            email=str(data.get("email", "")),
            course=str(data.get("course", "")),
            marks=float(data.get("marks", 0.0)),
            grade=str(data.get("grade", "")),
            created_at=str(data.get("created_at", "")),
            updated_at=str(data.get("updated_at", "")),
        )

    def is_passing(self) -> bool:
        """Return True if student marks are 50.0 or higher."""
        return self.marks >= 50.0
