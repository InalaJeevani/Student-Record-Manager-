"""Unit tests for StudentRecordManager."""

import tempfile
import unittest
from pathlib import Path

from student_manager.exceptions import (
    DuplicateStudentError,
    InvalidEmailError,
    InvalidGradeError,
    StudentNotFoundError,
)
from student_manager.manager import StudentRecordManager
from student_manager.storage import StorageManager


class TestStudentRecordManager(unittest.TestCase):
    """Test suite covering CRUD, searches, duplicates, updates, and stats."""

    def setUp(self) -> None:
        """Create an isolated manager with temporary JSON storage."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.json_path = Path(self.temp_dir.name) / "manager_test.json"
        self.storage = StorageManager(self.json_path)
        self.manager = StudentRecordManager(storage=self.storage, auto_load=False)

    def tearDown(self) -> None:
        """Clean up temporary directory."""
        self.temp_dir.cleanup()

    def test_add_student_success(self) -> None:
        """Verify student addition persists in memory and file."""
        student = self.manager.add_student(
            student_id="STU101",
            name="Alice Walker",
            email="alice.walker@books.org",
            course="Literature",
            marks=93.0,
        )
        self.assertEqual(student.student_id, "STU101")
        self.assertEqual(student.grade, "A+")
        self.assertIn("STU101", self.manager.records)
        self.assertTrue(self.json_path.exists())

    def test_duplicate_student_raises_exception(self) -> None:
        """Verify adding an existing student ID raises DuplicateStudentError."""
        self.manager.add_student(
            student_id="STU101",
            name="Alice Walker",
            email="alice.walker@books.org",
            course="Literature",
            marks=93.0,
        )
        with self.assertRaises(DuplicateStudentError):
            self.manager.add_student(
                student_id="stu101",  # case-insensitive duplicate check
                name="Duplicate Alice",
                email="alice2@books.org",
                course="History",
                marks=80.0,
            )

    def test_invalid_email_raises_exception(self) -> None:
        """Verify email validation fails during student addition."""
        with self.assertRaises(InvalidEmailError):
            self.manager.add_student(
                student_id="STU102",
                name="Bob Walker",
                email="not-an-email",
                course="Math",
                marks=80.0,
            )

    def test_get_and_search_students(self) -> None:
        """Verify record lookups and keyword searches."""
        self.manager.add_student("STU1", "Ada Lovelace", "ada@computing.org", "Math", 99.0)
        self.manager.add_student("STU2", "Alan Turing", "alan@crypt.org", "Computer Science", 98.0)

        # Lookup by exact ID
        ada = self.manager.get_student("STU1")
        self.assertEqual(ada.name, "Ada Lovelace")

        with self.assertRaises(StudentNotFoundError):
            self.manager.get_student("NONEXISTENT")

        # Search by query
        search_math = self.manager.search_students("math")
        self.assertEqual(len(search_math), 1)
        self.assertEqual(search_math[0].student_id, "STU1")

        search_turing = self.manager.search_students("Turing")
        self.assertEqual(len(search_turing), 1)
        self.assertEqual(search_turing[0].name, "Alan Turing")

    def test_update_student(self) -> None:
        """Verify updating existing student record."""
        self.manager.add_student("STU10", "Grace Hopper", "grace@navy.mil", "CS", 88.0)
        updated = self.manager.update_student("STU10", marks=96.0, course="Computer Engineering")

        self.assertEqual(updated.marks, 96.0)
        self.assertEqual(updated.grade, "A+")
        self.assertEqual(updated.course, "Computer Engineering")

        with self.assertRaises(InvalidGradeError):
            self.manager.update_student("STU10", marks=150.0)

    def test_delete_student(self) -> None:
        """Verify deleting student removes record from memory and storage."""
        self.manager.add_student("STU20", "John von Neumann", "john@princeton.edu", "Physics", 97.0)
        self.assertIn("STU20", self.manager.records)

        deleted = self.manager.delete_student("STU20")
        self.assertEqual(deleted.student_id, "STU20")
        self.assertNotIn("STU20", self.manager.records)

        with self.assertRaises(StudentNotFoundError):
            self.manager.get_student("STU20")

    def test_statistics_calculation(self) -> None:
        """Verify aggregate statistics calculations."""
        self.manager.add_student("S01", "Student One", "s1@test.com", "CS", 100.0)
        self.manager.add_student("S02", "Student Two", "s2@test.com", "CS", 50.0)
        self.manager.add_student("S03", "Student Three", "s3@test.com", "Math", 40.0)

        stats = self.manager.get_statistics()
        self.assertEqual(stats["total_students"], 3)
        self.assertEqual(stats["average_marks"], 63.33)
        self.assertEqual(stats["passing_count"], 2)
        self.assertEqual(stats["failing_count"], 1)
        self.assertEqual(stats["pass_percentage"], 66.67)
        self.assertEqual(stats["highest_score"]["student_id"], "S01")
        self.assertEqual(stats["lowest_score"]["student_id"], "S03")


if __name__ == "__main__":
    unittest.main()
