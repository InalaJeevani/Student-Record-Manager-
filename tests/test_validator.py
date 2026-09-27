"""Unit tests for StudentValidator and Regex Email Validation."""

import unittest
from student_manager.exceptions import (
    InvalidEmailError,
    InvalidGradeError,
    InvalidNameError,
    InvalidStudentIdError,
    InvalidCourseError,
)
from student_manager.validator import StudentValidator


class TestStudentValidator(unittest.TestCase):
    """Test suite covering email regex, ID, name, marks, and grade calculation."""

    def test_valid_emails(self) -> None:
        """Ensure standard, valid email formats are accepted and normalized."""
        valid_cases = [
            "student@example.com",
            "first.last@domain.co.uk",
            "user123@sub.university.edu",
            "name+tag@service.io",
            "test_user-123@domain.org",
            "ALICE@SCHOOL.EDU",
        ]
        for email in valid_cases:
            with self.subTest(email=email):
                result = StudentValidator.validate_email(email)
                self.assertEqual(result, email.strip().lower())

    def test_invalid_emails_raise_exception(self) -> None:
        """Ensure malformed emails raise InvalidEmailError."""
        invalid_cases = [
            "",
            "   ",
            "plainaddress",
            "missingdomain@",
            "@missinguser.com",
            "missing.dot@com",
            "user@domain..com",
            ".user@domain.com",
            "user@.domain.com",
            "user@domain.c",  # TLD shorter than 2 chars
            "user name@domain.com",  # space inside
            "user@domain.",
            None,
        ]
        for email in invalid_cases:
            with self.subTest(email=email):
                with self.assertRaises(InvalidEmailError):
                    StudentValidator.validate_email(email)

    def test_valid_student_ids(self) -> None:
        """Verify valid student IDs are normalized to uppercase."""
        self.assertEqual(StudentValidator.validate_student_id("stu101"), "STU101")
        self.assertEqual(StudentValidator.validate_student_id("CS-2024-01"), "CS-2024-01")
        self.assertEqual(StudentValidator.validate_student_id("ID_99"), "ID_99")

    def test_invalid_student_ids_raise_exception(self) -> None:
        """Verify invalid or empty IDs raise InvalidStudentIdError."""
        invalid_ids = ["", "  ", "a", "12", "id with spaces", "id#123", None]
        for sid in invalid_ids:
            with self.subTest(sid=sid):
                with self.assertRaises(InvalidStudentIdError):
                    StudentValidator.validate_student_id(sid)

    def test_valid_names(self) -> None:
        """Verify valid names are capitalized properly."""
        self.assertEqual(StudentValidator.validate_name("john doe"), "John Doe")
        self.assertEqual(StudentValidator.validate_name("mary-jane watson"), "Mary-jane Watson")
        self.assertEqual(StudentValidator.validate_name("o'connor"), "O'connor")

    def test_invalid_names_raise_exception(self) -> None:
        """Verify names with numbers, symbols, or invalid lengths raise InvalidNameError."""
        invalid_names = ["", " ", "A", "John123", "User@Domain", None]
        for name in invalid_names:
            with self.subTest(name=name):
                with self.assertRaises(InvalidNameError):
                    StudentValidator.validate_name(name)

    def test_valid_marks(self) -> None:
        """Verify valid numeric scores are parsed and rounded to float."""
        self.assertEqual(StudentValidator.validate_marks(100), 100.0)
        self.assertEqual(StudentValidator.validate_marks(0), 0.0)
        self.assertEqual(StudentValidator.validate_marks("85.556"), 85.56)
        self.assertEqual(StudentValidator.validate_marks(72.5), 72.5)

    def test_invalid_marks_raise_exception(self) -> None:
        """Verify scores outside 0-100 or non-numeric strings raise InvalidGradeError."""
        invalid_marks = [-1, 101, -0.01, 100.5, "abc", "eighty", "", None]
        for m in invalid_marks:
            with self.subTest(marks=m):
                with self.assertRaises(InvalidGradeError):
                    StudentValidator.validate_marks(m)

    def test_letter_grade_calculation(self) -> None:
        """Verify grading scale from A+ down to F."""
        self.assertEqual(StudentValidator.calculate_letter_grade(95.0), "A+")
        self.assertEqual(StudentValidator.calculate_letter_grade(90.0), "A+")
        self.assertEqual(StudentValidator.calculate_letter_grade(85.0), "A")
        self.assertEqual(StudentValidator.calculate_letter_grade(80.0), "A")
        self.assertEqual(StudentValidator.calculate_letter_grade(75.0), "B")
        self.assertEqual(StudentValidator.calculate_letter_grade(65.0), "C")
        self.assertEqual(StudentValidator.calculate_letter_grade(50.0), "D")
        self.assertEqual(StudentValidator.calculate_letter_grade(49.9), "F")
        self.assertEqual(StudentValidator.calculate_letter_grade(0.0), "F")

    def test_course_validation(self) -> None:
        """Verify course names are cleaned and empty courses raise InvalidCourseError."""
        self.assertEqual(StudentValidator.validate_course(" Computer Science "), "Computer Science")
        with self.assertRaises(InvalidCourseError):
            StudentValidator.validate_course("")
        with self.assertRaises(InvalidCourseError):
            StudentValidator.validate_course(None)


if __name__ == "__main__":
    unittest.main()
