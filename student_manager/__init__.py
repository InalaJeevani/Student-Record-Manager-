"""Student Record Manager Package.

A modular, production-ready system for managing student records with
input validation, regex email checking, robust exception handling,
and persistent file storage.
"""

from .exceptions import (
    StudentRecordError,
    ValidationError,
    InvalidEmailError,
    InvalidStudentIdError,
    InvalidNameError,
    InvalidGradeError,
    InvalidCourseError,
    StudentNotFoundError,
    DuplicateStudentError,
    StorageError,
)
from .models import Student
from .validator import StudentValidator
from .storage import StorageManager
from .manager import StudentRecordManager

__all__ = [
    "StudentRecordError",
    "ValidationError",
    "InvalidEmailError",
    "InvalidStudentIdError",
    "InvalidNameError",
    "InvalidGradeError",
    "InvalidCourseError",
    "StudentNotFoundError",
    "DuplicateStudentError",
    "StorageError",
    "Student",
    "StudentValidator",
    "StorageManager",
    "StudentRecordManager",
]
