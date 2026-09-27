"""High-level management system for Student records."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

from .exceptions import DuplicateStudentError, StudentNotFoundError
from .models import Student
from .storage import StorageManager
from .validator import StudentValidator


class StudentRecordManager:
    """Manages the lifecycle of student records, in-memory caching, and file persistence."""

    def __init__(
        self,
        storage: Optional[StorageManager] = None,
        auto_load: bool = True,
    ) -> None:
        """Initialize the StudentRecordManager.

        Args:
            storage: Optional custom StorageManager instance.
            auto_load: If True, automatically loads existing records from storage file.
        """
        self.storage = storage or StorageManager()
        self.records: Dict[str, Student] = {}

        if auto_load:
            self.load_from_file()

    def add_student(
        self,
        student_id: str,
        name: str,
        email: str,
        course: str,
        marks: float | int | str,
        auto_save: bool = True,
    ) -> Student:
        """Validate and add a new student to records.

        Args:
            student_id: Unique student ID.
            name: Student name.
            email: Student email (validated using regex).
            course: Department/Course.
            marks: Numeric score (0.0 to 100.0).
            auto_save: Whether to persist records immediately.

        Returns:
            The created Student object.

        Raises:
            DuplicateStudentError: If student with student_id already exists.
            ValidationError: If any field fails validation rules.
            StorageError: If auto_save is True and file writing fails.
        """
        # Validate ID first to normalize casing before duplicate check
        normalized_id = StudentValidator.validate_student_id(student_id)

        if normalized_id in self.records:
            raise DuplicateStudentError(normalized_id)

        student = Student.create(
            student_id=normalized_id,
            name=name,
            email=email,
            course=course,
            marks=marks,
        )

        self.records[student.student_id] = student

        if auto_save:
            self.save_to_file()

        return student

    def get_student(self, student_id: str) -> Student:
        """Retrieve a student record by student ID.

        Args:
            student_id: Student ID to search for.

        Returns:
            Matching Student object.

        Raises:
            StudentNotFoundError: If ID is not present in records.
        """
        normalized_id = (student_id or "").strip().upper()
        if normalized_id not in self.records:
            raise StudentNotFoundError(normalized_id)
        return self.records[normalized_id]

    def get_all_students(self) -> List[Student]:
        """Return a sorted list of all active student records.

        Returns:
            List of Student objects sorted by student ID.
        """
        return sorted(self.records.values(), key=lambda s: s.student_id)

    def search_students(self, keyword: str) -> List[Student]:
        """Search student records by ID, name, email, or course (case-insensitive).

        Args:
            keyword: Substring to search for.

        Returns:
            List of matching Student objects.
        """
        if not keyword:
            return self.get_all_students()

        q = keyword.strip().lower()
        results: List[Student] = []

        for student in self.records.values():
            if (
                q in student.student_id.lower()
                or q in student.name.lower()
                or q in student.email.lower()
                or q in student.course.lower()
                or q in student.grade.lower()
            ):
                results.append(student)

        return sorted(results, key=lambda s: s.student_id)

    def update_student(
        self,
        student_id: str,
        name: Optional[str] = None,
        email: Optional[str] = None,
        course: Optional[str] = None,
        marks: Optional[float | int | str] = None,
        auto_save: bool = True,
    ) -> Student:
        """Update existing student details.

        Args:
            student_id: ID of the student to update.
            name: New name, if provided.
            email: New email, if provided.
            course: New course, if provided.
            marks: New marks, if provided.
            auto_save: Whether to persist records immediately.

        Returns:
            The updated Student object.

        Raises:
            StudentNotFoundError: If ID does not exist.
            ValidationError: If any updated field is invalid.
            StorageError: If saving to disk fails.
        """
        student = self.get_student(student_id)
        student.update(name=name, email=email, course=course, marks=marks)

        if auto_save:
            self.save_to_file()

        return student

    def delete_student(self, student_id: str, auto_save: bool = True) -> Student:
        """Remove a student record from the system.

        Args:
            student_id: Student ID to delete.
            auto_save: Whether to persist change immediately.

        Returns:
            The removed Student object.

        Raises:
            StudentNotFoundError: If student ID is not found.
            StorageError: If disk save fails.
        """
        student = self.get_student(student_id)
        del self.records[student.student_id]

        if auto_save:
            self.save_to_file()

        return student

    def save_to_file(self, target_path: Optional[str | Path] = None) -> str:
        """Persist in-memory records to file storage.

        Args:
            target_path: Optional file destination path.

        Returns:
            Destination path string.
        """
        return self.storage.save_to_json(self.records, target_path=target_path)

    def load_from_file(self, source_path: Optional[str | Path] = None) -> int:
        """Load records from file into memory.

        Args:
            source_path: Optional source file path.

        Returns:
            Count of loaded students.
        """
        self.records = self.storage.load_from_json(source_path=source_path)
        return len(self.records)

    def export_csv(self, csv_path: str | Path) -> str:
        """Export all current student records to CSV format.

        Args:
            csv_path: Target CSV file path.

        Returns:
            Resolved path of the CSV file.
        """
        return self.storage.export_to_csv(self.records, csv_path)

    def get_statistics(self) -> Dict[str, Any]:
        """Compute aggregated performance and demographic statistics.

        Returns:
            Dictionary with statistical metrics.
        """
        total = len(self.records)
        if total == 0:
            return {
                "total_students": 0,
                "average_marks": 0.0,
                "highest_score": None,
                "lowest_score": None,
                "passing_count": 0,
                "failing_count": 0,
                "pass_percentage": 0.0,
                "grade_distribution": {},
                "course_distribution": {},
            }

        students_list = list(self.records.values())
        total_marks = sum(s.marks for s in students_list)
        avg_marks = round(total_marks / total, 2)

        highest = max(students_list, key=lambda s: s.marks)
        lowest = min(students_list, key=lambda s: s.marks)

        passing = sum(1 for s in students_list if s.is_passing())
        failing = total - passing
        pass_pct = round((passing / total) * 100, 2)

        grades: Dict[str, int] = {}
        for s in students_list:
            grades[s.grade] = grades.get(s.grade, 0) + 1

        courses: Dict[str, int] = {}
        for s in students_list:
            courses[s.course] = courses.get(s.course, 0) + 1

        return {
            "total_students": total,
            "average_marks": avg_marks,
            "highest_score": {
                "student_id": highest.student_id,
                "name": highest.name,
                "marks": highest.marks,
                "grade": highest.grade,
            },
            "lowest_score": {
                "student_id": lowest.student_id,
                "name": lowest.name,
                "marks": lowest.marks,
                "grade": lowest.grade,
            },
            "passing_count": passing,
            "failing_count": failing,
            "pass_percentage": pass_pct,
            "grade_distribution": grades,
            "course_distribution": courses,
        }
