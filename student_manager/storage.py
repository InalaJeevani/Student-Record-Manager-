"""Persistent storage manager for Student Record Manager.

Supports saving and loading student records to/from JSON and CSV formats
with robust error handling, atomic write operations, and directory management.
"""

from __future__ import annotations

import csv
import json
import os
import tempfile
from pathlib import Path
from typing import Dict, List, Mapping

from .exceptions import StorageError
from .models import Student


class StorageManager:
    """Handles persistent storage of student records on disk."""

    DEFAULT_DATA_DIR = Path(__file__).resolve().parent.parent / "data"
    DEFAULT_JSON_PATH = DEFAULT_DATA_DIR / "students.json"

    def __init__(self, file_path: str | Path | None = None) -> None:
        """Initialize the storage manager with a target file path.

        Args:
            file_path: Optional custom path to store records.
        """
        self.file_path = Path(file_path) if file_path else self.DEFAULT_JSON_PATH

    def ensure_directory_exists(self) -> None:
        """Ensure the directory for the target file exists."""
        try:
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            raise StorageError(
                f"Failed to create data directory '{self.file_path.parent}': {e}",
                original_exception=e,
            ) from e

    def save_to_json(
        self,
        students: Mapping[str, Student] | List[Student],
        target_path: str | Path | None = None,
    ) -> str:
        """Save a collection of student records to a JSON file safely.

        Args:
            students: Mapping of {id: Student} or list of Student instances.
            target_path: Optional override path.

        Returns:
            The absolute file path where records were saved.

        Raises:
            StorageError: If serialization or writing fails.
        """
        dest_path = Path(target_path) if target_path else self.file_path
        try:
            dest_path.parent.mkdir(parents=True, exist_ok=True)

            if isinstance(students, dict):
                records = [s.to_dict() for s in students.values()]
            else:
                records = [s.to_dict() for s in students]

            # Atomic write: write to temp file first, then atomically replace
            temp_dir = dest_path.parent
            with tempfile.NamedTemporaryFile(
                "w", encoding="utf-8", dir=temp_dir, delete=False
            ) as tf:
                temp_name = tf.name
                json.dump(records, tf, indent=4, ensure_ascii=False)

            # Replace destination file safely
            if os.path.exists(dest_path):
                os.replace(temp_name, dest_path)
            else:
                os.rename(temp_name, dest_path)

            return str(dest_path.resolve())

        except (OSError, TypeError, ValueError) as err:
            raise StorageError(
                f"Failed to save student records to '{dest_path}': {err}",
                original_exception=err,
            ) from err

    def load_from_json(
        self, source_path: str | Path | None = None
    ) -> Dict[str, Student]:
        """Load student records from a JSON file.

        Args:
            source_path: Optional override path to load from.

        Returns:
            Dictionary mapping student ID to Student objects.

        Raises:
            StorageError: If reading, parsing, or deserialization fails.
        """
        src = Path(source_path) if source_path else self.file_path
        if not src.exists():
            # If file doesn't exist yet, return an empty dictionary
            return {}

        try:
            with open(src, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    return {}
                data = json.loads(content)

            if not isinstance(data, list):
                raise StorageError(
                    f"Invalid file format in '{src}': expected a JSON array of students."
                )

            students: Dict[str, Student] = {}
            for item in data:
                if not isinstance(item, dict):
                    continue
                student = Student.from_dict(item)
                students[student.student_id] = student

            return students

        except json.JSONDecodeError as err:
            raise StorageError(
                f"Corrupted or invalid JSON data in '{src}' at line {err.lineno}: {err.msg}",
                original_exception=err,
            ) from err
        except OSError as err:
            raise StorageError(
                f"Failed to read student records from '{src}': {err}",
                original_exception=err,
            ) from err

    def export_to_csv(
        self,
        students: Mapping[str, Student] | List[Student],
        csv_path: str | Path,
    ) -> str:
        """Export student records to a CSV spreadsheet format.

        Args:
            students: Mapping or list of students.
            csv_path: Path for output CSV file.

        Returns:
            Absolute path of saved CSV.

        Raises:
            StorageError: If CSV writing fails.
        """
        out_path = Path(csv_path)
        try:
            out_path.parent.mkdir(parents=True, exist_ok=True)
            fieldnames = [
                "student_id",
                "name",
                "email",
                "course",
                "marks",
                "grade",
                "created_at",
                "updated_at",
            ]

            records = (
                list(students.values()) if isinstance(students, dict) else list(students)
            )

            with open(out_path, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for student in records:
                    writer.writerow(student.to_dict())

            return str(out_path.resolve())

        except OSError as err:
            raise StorageError(
                f"Failed to export student records to CSV '{out_path}': {err}",
                original_exception=err,
            ) from err
