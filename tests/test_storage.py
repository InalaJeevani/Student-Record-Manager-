"""Unit tests for StorageManager."""

import json
import tempfile
import unittest
from pathlib import Path

from student_manager.exceptions import StorageError
from student_manager.models import Student
from student_manager.storage import StorageManager


class TestStorageManager(unittest.TestCase):
    """Test suite covering persistent storage, JSON serialization, and CSV exports."""

    def setUp(self) -> None:
        """Create a temporary directory for isolation."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.json_path = Path(self.temp_dir.name) / "test_students.json"
        self.csv_path = Path(self.temp_dir.name) / "test_students.csv"
        self.storage = StorageManager(self.json_path)

        self.student1 = Student.create(
            student_id="STU001",
            name="Alice Wonder",
            email="alice@wonderland.com",
            course="Literature",
            marks=95.0,
        )
        self.student2 = Student.create(
            student_id="STU002",
            name="Mad Hatter",
            email="hatter@tea.party.org",
            course="Design",
            marks=77.0,
        )

    def tearDown(self) -> None:
        """Clean up temporary test directory."""
        self.temp_dir.cleanup()

    def test_save_and_load_records(self) -> None:
        """Verify saving to JSON and loading back maintains integrity."""
        records = {self.student1.student_id: self.student1, self.student2.student_id: self.student2}
        saved_path = self.storage.save_to_json(records)
        self.assertTrue(Path(saved_path).exists())

        loaded = self.storage.load_from_json()
        self.assertEqual(len(loaded), 2)
        self.assertIn("STU001", loaded)
        self.assertIn("STU002", loaded)
        self.assertEqual(loaded["STU001"].name, "Alice Wonder")
        self.assertEqual(loaded["STU002"].marks, 77.0)

    def test_load_non_existent_file_returns_empty_dict(self) -> None:
        """Verify loading from non-existent file returns empty dict gracefully."""
        non_existent = Path(self.temp_dir.name) / "missing.json"
        storage = StorageManager(non_existent)
        records = storage.load_from_json()
        self.assertEqual(records, {})

    def test_corrupted_json_raises_storage_error(self) -> None:
        """Verify corrupt JSON file raises a clear StorageError exception."""
        with open(self.json_path, "w", encoding="utf-8") as f:
            f.write("{ invalid json [ content ...")

        with self.assertRaises(StorageError):
            self.storage.load_from_json()

    def test_export_to_csv(self) -> None:
        """Verify exporting to CSV generates valid CSV header and rows."""
        records = [self.student1, self.student2]
        out_csv = self.storage.export_to_csv(records, self.csv_path)
        self.assertTrue(Path(out_csv).exists())

        with open(out_csv, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f.readlines()]

        self.assertGreaterEqual(len(lines), 3)  # header + 2 student rows
        self.assertIn("student_id,name,email,course,marks,grade", lines[0])
        self.assertIn("STU001", lines[1])


if __name__ == "__main__":
    unittest.main()
