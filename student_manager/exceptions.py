"""Custom exceptions for the Student Record Manager system.

Provides a clean exception hierarchy for domain errors, input validation,
file storage operations, and record lookups.
"""


class StudentRecordError(Exception):
    """Base exception for all Student Record Manager errors."""

    def __init__(self, message: str = "An error occurred in Student Record Manager.") -> None:
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        return self.message


class ValidationError(StudentRecordError):
    """Base exception raised when student input data violates domain validation rules."""

    def __init__(self, message: str = "Invalid student data provided.", field: str | None = None) -> None:
        super().__init__(message)
        self.field = field


class InvalidEmailError(ValidationError):
    """Raised when an email address fails RFC-compliant regex validation."""

    def __init__(
        self,
        email: str,
        message: str | None = None,
    ) -> None:
        msg = message or (
            f"Invalid email address '{email}'. Expected format: name@domain.com "
            "(must contain valid alphanumeric prefix, '@', domain, and a 2+ letter extension)."
        )
        super().__init__(msg, field="email")
        self.email = email


class InvalidStudentIdError(ValidationError):
    """Raised when a student ID does not match expected ID pattern or format."""

    def __init__(
        self,
        student_id: str,
        message: str | None = None,
    ) -> None:
        msg = message or (
            f"Invalid student ID '{student_id}'. Student ID must be 3-15 alphanumeric characters "
            "(e.g., 'STU001', 'CS101', '2024-001')."
        )
        super().__init__(msg, field="student_id")
        self.student_id = student_id


class InvalidNameError(ValidationError):
    """Raised when a student name is empty, too short, or contains invalid characters."""

    def __init__(
        self,
        name: str,
        message: str | None = None,
    ) -> None:
        msg = message or (
            f"Invalid student name '{name}'. Name must contain between 2 and 60 characters, "
            "using only alphabetic characters, spaces, hyphens, or apostrophes."
        )
        super().__init__(msg, field="name")
        self.name = name


class InvalidGradeError(ValidationError):
    """Raised when marks or GPA is out of range or not a valid number."""

    def __init__(
        self,
        grade_value: object,
        message: str | None = None,
    ) -> None:
        msg = message or (
            f"Invalid marks/grade '{grade_value}'. Score must be a numeric value between 0.0 and 100.0."
        )
        super().__init__(msg, field="marks")
        self.grade_value = grade_value


class InvalidCourseError(ValidationError):
    """Raised when course name is empty or invalid."""

    def __init__(
        self,
        course: str,
        message: str | None = None,
    ) -> None:
        msg = message or f"Invalid course '{course}'. Course name cannot be empty (min 2 characters)."
        super().__init__(msg, field="course")
        self.course = course


class StudentNotFoundError(StudentRecordError):
    """Raised when an operation requests a student ID that does not exist in records."""

    def __init__(self, student_id: str) -> None:
        super().__init__(f"Student with ID '{student_id}' was not found in records.")
        self.student_id = student_id


class DuplicateStudentError(StudentRecordError):
    """Raised when attempting to add a student whose ID already exists."""

    def __init__(self, student_id: str) -> None:
        super().__init__(f"Student with ID '{student_id}' already exists in records. Use update instead.")
        self.student_id = student_id


class StorageError(StudentRecordError):
    """Raised when file reading, writing, serialization, or deserialization fails."""

    def __init__(self, message: str, original_exception: Exception | None = None) -> None:
        super().__init__(message)
        self.original_exception = original_exception
