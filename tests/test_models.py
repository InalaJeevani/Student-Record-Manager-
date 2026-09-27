"""Unit tests for the Student model."""

import unittest
from student_manager.exceptions import InvalidEmailError, InvalidGradeError
from student_manager.models import Student


class TestStudentModel(unittest.TestCase):
    """Test suite covering Student model instantiation, updates, and serialization."""

    def test_student_factory_creation(self) -> None:
        """Verify Student.create validates attributes and calculates letter grade."""
        student = Student.create(
            student_id="stu101",
            name="alice smith",
            email="alice.smith@university.edu",
            course="Physics",
            marks=92.5,
        )
        self.assertEqual(student.student_id, "STU101")
        self.assertEqual(student.name, "Alice Smith")
        self.assertEqual(student.email, "alice.smith@university.edu")
        self.assertEqual(student.course, "Physics")
        self.assertEqual(student.marks, 92.5)
        self.assertEqual(student.grade, "A+")
        self.assertTrue(student.is_passing())

    def test_student_update_validates_new_fields(self) -> None:
        """Verify updating fields updates grade and timestamps properly."""
        student = Student.create(
            student_id="STU102",
            name="Bob Brown",
            email="bob@campus.edu",
            course="Math",
            marks=40.0,
        )
        self.assertEqual(student.grade, "F")
        self.assertFalse(student.is_passing())

        # Update marks to 85
        student.update(marks=85.0)
        self.assertEqual(student.marks, 85.0)
        self.assertEqual(student.grade, "A")
        self.assertTrue(student.is_passing())

        # Updating email with invalid regex throws error
        with self.assertRaises(InvalidEmailError):
            student.update(email="bad-email-without-domain")

    def test_dict_serialization_roundtrip(self) -> None:
        """Verify to_dict and from_dict preserve all properties."""
        original = Student.create(
            student_id="STU103",
            name="Charlie Day",
            email="charlie@paddys.com",
            course="Drama",
            marks=74.0,
        )
        as_dict = original.to_dict()
        restored = Student.from_dict(as_dict)

        self.assertEqual(restored.student_id, original.student_id)
        self.assertEqual(restored.name, original.name)
        self.assertEqual(restored.email, original.email)
        self.assertEqual(restored.course, original.course)
        self.assertEqual(restored.marks, original.marks)
        self.assertEqual(restored.grade, original.grade)


if __name__ == "__main__":
    unittest.main()
