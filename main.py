"""Command-Line Interface for Student Record Manager.

Provides an interactive, menu-driven CLI with rich table formatting,
regex email validation, persistent storage, and comprehensive exception handling.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Optional

from student_manager.exceptions import (
    DuplicateStudentError,
    InvalidCourseError,
    InvalidEmailError,
    InvalidGradeError,
    InvalidNameError,
    InvalidStudentIdError,
    StudentNotFoundError,
    StudentRecordError,
    ValidationError,
    StorageError,
)
from student_manager.manager import StudentRecordManager
from student_manager.models import Student


# Ensure standard UTF-8 console output on Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


# ANSI color codes for enhanced terminal output
class Colors:
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RESET = "\033[0m"


def clear_screen() -> None:
    """Clear terminal screen gracefully."""
    os.system("cls" if os.name == "nt" else "clear")


def print_banner() -> None:
    """Print the program welcome banner."""
    print(f"{Colors.CYAN}{Colors.BOLD}")
    print("=" * 72)
    print("             STUDENT RECORD MANAGEMENT SYSTEM                ")
    print("       Validation * Regex Email * Persistent Storage * Reports")
    print("=" * 72)
    print(f"{Colors.RESET}")


def print_menu() -> None:
    """Print the available user action options."""
    print(f"\n{Colors.BOLD}--- MAIN MENU ---{Colors.RESET}")
    print(f"{Colors.GREEN}[1]{Colors.RESET} Add New Student")
    print(f"{Colors.GREEN}[2]{Colors.RESET} View All Students")
    print(f"{Colors.GREEN}[3]{Colors.RESET} Search Student (ID, Name, Email, Course)")
    print(f"{Colors.GREEN}[4]{Colors.RESET} Update Student Details")
    print(f"{Colors.GREEN}[5]{Colors.RESET} Delete Student Record")
    print(f"{Colors.GREEN}[6]{Colors.RESET} View Class Statistics & Performance")
    print(f"{Colors.GREEN}[7]{Colors.RESET} Export Records to CSV")
    print(f"{Colors.GREEN}[8]{Colors.RESET} Load Sample / Demo Records")
    print(f"{Colors.GREEN}[9]{Colors.RESET} Reload Records from Disk")
    print(f"{Colors.RED}[0]{Colors.RESET} Exit System")


def print_student_table(students: list[Student], title: str = "Student Records") -> None:
    """Format and display student records in a tabular view.

    Args:
        students: List of students to display.
        title: Table header title.
    """
    if not students:
        print(f"\n{Colors.YELLOW}No student records found.{Colors.RESET}")
        return

    print(f"\n{Colors.BOLD}{Colors.CYAN}--- {title} ({len(students)} total) ---{Colors.RESET}")
    header = (
        f"{'ID':<10} | {'Name':<20} | {'Email':<28} | {'Course':<18} | {'Marks':<7} | {'Grade':<5}"
    )
    separator = "-" * len(header)
    print(f"{Colors.BOLD}{header}{Colors.RESET}")
    print(separator)

    for s in students:
        # Highlight failing grades in red, top grades in green
        if s.grade in ("A+", "A"):
            grade_color = Colors.GREEN
        elif s.grade == "F":
            grade_color = Colors.RED
        else:
            grade_color = Colors.YELLOW

        marks_str = f"{s.marks:.2f}"
        print(
            f"{s.student_id:<10} | "
            f"{s.name:<20} | "
            f"{s.email:<28} | "
            f"{s.course:<18} | "
            f"{marks_str:<7} | "
            f"{grade_color}{s.grade:<5}{Colors.RESET}"
        )
    print(separator)


def handle_add_student(manager: StudentRecordManager) -> None:
    """Prompt user for student details and handle validation exceptions."""
    print(f"\n{Colors.BOLD}{Colors.CYAN}--- Add New Student ---{Colors.RESET}")
    print(f"{Colors.DIM}Enter student details. Email is validated using regex (e.g. name@domain.com).{Colors.RESET}")

    try:
        student_id = input(f"{Colors.BOLD}Student ID (e.g. STU101): {Colors.RESET}").strip()
        name = input(f"{Colors.BOLD}Full Name: {Colors.RESET}").strip()
        email = input(f"{Colors.BOLD}Email Address: {Colors.RESET}").strip()
        course = input(f"{Colors.BOLD}Course / Major: {Colors.RESET}").strip()
        marks = input(f"{Colors.BOLD}Marks (0 - 100): {Colors.RESET}").strip()

        # The manager validates each field and catches domain exceptions
        student = manager.add_student(
            student_id=student_id,
            name=name,
            email=email,
            course=course,
            marks=marks,
        )

        print(
            f"\n{Colors.GREEN}[+] Student '{student.name}' (ID: {student.student_id}) "
            f"added successfully with Grade {student.grade}!{Colors.RESET}"
        )

    except DuplicateStudentError as err:
        print(f"\n{Colors.RED}[!] Duplicate Error: {err}{Colors.RESET}")
    except InvalidEmailError as err:
        print(f"\n{Colors.RED}[!] Email Validation Error: {err}{Colors.RESET}")
        print(f"{Colors.YELLOW}Hint: Ensure your email has '@' and a valid domain (e.g. alice@example.com).{Colors.RESET}")
    except (InvalidStudentIdError, InvalidNameError, InvalidCourseError, InvalidGradeError) as err:
        print(f"\n{Colors.RED}[!] Input Validation Error: {err}{Colors.RESET}")
    except StorageError as err:
        print(f"\n{Colors.RED}[!] File Storage Error: {err}{Colors.RESET}")
    except Exception as err:
        print(f"\n{Colors.RED}[!] Unexpected Error: {err}{Colors.RESET}")


def handle_view_students(manager: StudentRecordManager) -> None:
    """View all students stored in the system."""
    students = manager.get_all_students()
    print_student_table(students, title="All Enrolled Students")


def handle_search_student(manager: StudentRecordManager) -> None:
    """Search for students by ID, Name, Email, or Course."""
    keyword = input(f"\n{Colors.BOLD}Enter search keyword: {Colors.RESET}").strip()
    if not keyword:
        print(f"{Colors.YELLOW}Search term cannot be empty.{Colors.RESET}")
        return

    results = manager.search_students(keyword)
    print_student_table(results, title=f"Search Results for '{keyword}'")


def handle_update_student(manager: StudentRecordManager) -> None:
    """Prompt user to update specific fields for an existing student."""
    print(f"\n{Colors.BOLD}{Colors.CYAN}--- Update Student Details ---{Colors.RESET}")
    student_id = input(f"{Colors.BOLD}Enter Student ID to update: {Colors.RESET}").strip()

    try:
        existing = manager.get_student(student_id)
        print(f"\n{Colors.GREEN}Current Record:{Colors.RESET}")
        print(
            f"ID: {existing.student_id} | Name: {existing.name} | "
            f"Email: {existing.email} | Course: {existing.course} | Marks: {existing.marks} (Grade: {existing.grade})"
        )
        print(f"{Colors.DIM}Leave input blank to keep the current value.{Colors.RESET}\n")

        new_name = input(f"New Name [{existing.name}]: ").strip() or None
        new_email = input(f"New Email [{existing.email}]: ").strip() or None
        new_course = input(f"New Course [{existing.course}]: ").strip() or None
        new_marks = input(f"New Marks [{existing.marks}]: ").strip() or None

        if not any([new_name, new_email, new_course, new_marks]):
            print(f"{Colors.YELLOW}No changes were made.{Colors.RESET}")
            return

        updated = manager.update_student(
            student_id=existing.student_id,
            name=new_name,
            email=new_email,
            course=new_course,
            marks=new_marks,
        )

        print(
            f"\n{Colors.GREEN}[+] Student '{updated.student_id}' successfully updated! "
            f"New Grade: {updated.grade}{Colors.RESET}"
        )

    except StudentNotFoundError as err:
        print(f"\n{Colors.RED}[!] Not Found: {err}{Colors.RESET}")
    except (InvalidEmailError, ValidationError) as err:
        print(f"\n{Colors.RED}[!] Validation Error: {err}{Colors.RESET}")
    except StorageError as err:
        print(f"\n{Colors.RED}[!] Storage Error: {err}{Colors.RESET}")


def handle_delete_student(manager: StudentRecordManager) -> None:
    """Remove a student after explicit confirmation."""
    print(f"\n{Colors.BOLD}{Colors.CYAN}--- Delete Student Record ---{Colors.RESET}")
    student_id = input(f"{Colors.BOLD}Enter Student ID to delete: {Colors.RESET}").strip()

    try:
        student = manager.get_student(student_id)
        confirm = (
            input(
                f"{Colors.YELLOW}Are you sure you want to delete '{student.name}' (ID: {student.student_id})? (y/N): {Colors.RESET}"
            )
            .strip()
            .lower()
        )

        if confirm == "y" or confirm == "yes":
            deleted = manager.delete_student(student_id)
            print(f"\n{Colors.GREEN}[+] Student '{deleted.name}' has been deleted.{Colors.RESET}")
        else:
            print(f"\n{Colors.YELLOW}Deletion cancelled.{Colors.RESET}")

    except StudentNotFoundError as err:
        print(f"\n{Colors.RED}[!] Not Found: {err}{Colors.RESET}")
    except StorageError as err:
        print(f"\n{Colors.RED}[!] Storage Error: {err}{Colors.RESET}")


def handle_view_statistics(manager: StudentRecordManager) -> None:
    """Display analytics regarding marks, passing rate, and distribution."""
    stats = manager.get_statistics()
    if stats["total_students"] == 0:
        print(f"\n{Colors.YELLOW}No student data available to compute statistics.{Colors.RESET}")
        return

    print(f"\n{Colors.BOLD}{Colors.CYAN}=== CLASS PERFORMANCE & STATISTICS ==={Colors.RESET}")
    print(f"Total Enrolled Students : {Colors.BOLD}{stats['total_students']}{Colors.RESET}")
    print(f"Class Average Marks     : {Colors.BOLD}{stats['average_marks']:.2f}%{Colors.RESET}")
    print(
        f"Passing Students        : {Colors.GREEN}{stats['passing_count']}{Colors.RESET} "
        f"({stats['pass_percentage']}%)"
    )
    print(f"Failing Students        : {Colors.RED}{stats['failing_count']}{Colors.RESET}")

    if stats["highest_score"]:
        top = stats["highest_score"]
        print(
            f"Top Performer           : {Colors.GREEN}{top['name']} ({top['student_id']}) "
            f"with {top['marks']}% [Grade {top['grade']}]{Colors.RESET}"
        )
    if stats["lowest_score"]:
        low = stats["lowest_score"]
        print(
            f"Lowest Score            : {Colors.YELLOW}{low['name']} ({low['student_id']}) "
            f"with {low['marks']}% [Grade {low['grade']}]{Colors.RESET}"
        )

    print(f"\n{Colors.BOLD}Grade Distribution:{Colors.RESET}")
    for grade, count in sorted(stats["grade_distribution"].items()):
        bars = "#" * count
        print(f"  Grade {grade:<2}: {count:>2} {Colors.CYAN}{bars}{Colors.RESET}")

    print(f"\n{Colors.BOLD}Enrollment by Course:{Colors.RESET}")
    for course, count in sorted(stats["course_distribution"].items()):
        print(f"  * {course:<20}: {count} student(s)")


def handle_export_csv(manager: StudentRecordManager) -> None:
    """Export all student records to a CSV file."""
    default_csv = Path(__file__).resolve().parent / "data" / "students_export.csv"
    prompt = f"Enter export CSV path (default: {default_csv.name}): "
    path_input = input(f"{Colors.BOLD}{prompt}{Colors.RESET}").strip()
    target_path = Path(path_input) if path_input else default_csv

    try:
        saved_path = manager.export_csv(target_path)
        print(f"\n{Colors.GREEN}[+] Records exported successfully to:{Colors.RESET} {saved_path}")
    except StorageError as err:
        print(f"\n{Colors.RED}[!] CSV Export Failed: {err}{Colors.RESET}")


def handle_load_sample_data(manager: StudentRecordManager) -> None:
    """Load sample mock student data for quick demonstration."""
    sample_records = [
        ("STU101", "Alice Johnson", "alice.johnson@university.edu", "Computer Science", 94.5),
        ("STU102", "Bob Smith", "bob.smith@techcollege.org", "Data Science", 82.0),
        ("STU103", "Charlie Brown", "charlie.b@campus.edu", "Software Engineering", 68.5),
        ("STU104", "Diana Prince", "diana.prince@academy.org", "Cybersecurity", 91.0),
        ("STU105", "Evan Wright", "evan.wright@mail.com", "Artificial Intelligence", 45.0),
    ]

    added = 0
    for sid, name, email, course, marks in sample_records:
        if sid not in manager.records:
            try:
                manager.add_student(sid, name, email, course, marks, auto_save=False)
                added += 1
            except ValidationError:
                pass

    if added > 0:
        manager.save_to_file()
        print(f"\n{Colors.GREEN}[+] Successfully loaded {added} sample student record(s)!{Colors.RESET}")
    else:
        print(f"\n{Colors.YELLOW}Sample records are already loaded.{Colors.RESET}")


def handle_reload_records(manager: StudentRecordManager) -> None:
    """Reload records directly from the storage file."""
    try:
        count = manager.load_from_file()
        print(f"\n{Colors.GREEN}[+] Successfully reloaded {count} student record(s) from disk.{Colors.RESET}")
    except StorageError as err:
        print(f"\n{Colors.RED}[!] Storage Error: {err}{Colors.RESET}")


def main() -> None:
    """Application main entrypoint loop."""
    print_banner()
    manager = StudentRecordManager()
    print(f"{Colors.DIM}Storage linked: {manager.storage.file_path}{Colors.RESET}")
    print(f"{Colors.GREEN}Loaded {len(manager.records)} existing student record(s).{Colors.RESET}")

    while True:
        try:
            print_menu()
            choice = input(f"\n{Colors.BOLD}Enter your choice [0-9]: {Colors.RESET}").strip()

            if choice == "1":
                handle_add_student(manager)
            elif choice == "2":
                handle_view_students(manager)
            elif choice == "3":
                handle_search_student(manager)
            elif choice == "4":
                handle_update_student(manager)
            elif choice == "5":
                handle_delete_student(manager)
            elif choice == "6":
                handle_view_statistics(manager)
            elif choice == "7":
                handle_export_csv(manager)
            elif choice == "8":
                handle_load_sample_data(manager)
            elif choice == "9":
                handle_reload_records(manager)
            elif choice == "0":
                print(f"\n{Colors.CYAN}Saving records and exiting... Goodbye!{Colors.RESET}\n")
                sys.exit(0)
            else:
                print(f"\n{Colors.YELLOW}Invalid option '{choice}'. Please select a number between 0 and 9.{Colors.RESET}")

        except KeyboardInterrupt:
            print(f"\n\n{Colors.CYAN}Operation cancelled by user. Exiting... Goodbye! 👋{Colors.RESET}\n")
            sys.exit(0)
        except EOFError:
            print(f"\n\n{Colors.CYAN}Input stream ended. Exiting... Goodbye! 👋{Colors.RESET}\n")
            sys.exit(0)


if __name__ == "__main__":
    main()
