# 🎓 Student Record Manager

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-24%20Passing-brightgreen.svg)]()
[![Code Style](https://img.shields.io/badge/Code%20Style-Clean%20PEP8-orange.svg)]()

A modular, production-ready **Student Record Management System** built with Python. Designed with clean object-oriented architecture, strict input validation using regular expressions, custom exception hierarchies, and persistent file storage.

---

## 📑 Table of Contents

- [Features](#-features)
- [Project Architecture](#-project-architecture)
- [Email Regex Validation](#-email-regex-validation)
- [Exception Handling Architecture](#-exception-handling-architecture)
- [Quick Start Guide](#-quick-start-guide)
  - [Prerequisites](#prerequisites)
  - [Installation & Setup](#installation--setup)
  - [Running the Application](#running-the-application)
- [Running Unit Tests](#-running-unit-tests)
- [How to Deploy to GitHub](#-how-to-deploy-to-github)
- [License](#-license)

---

## ✨ Features

- **➕ Add Student**: Enroll new students with Student ID, Full Name, Email, Course, and Marks. Automatically computes letter grades (`A+`, `A`, `B`, `C`, `D`, `F`).
- **🔍 Validate Email using Regex**: Robust RFC-compliant regex validation checks the email prefix, `@` symbol, domain name, and minimum 2-character Top-Level Domain (TLD).
- **💾 Save Data to File**: Records are automatically saved to persistent JSON storage using atomic temporary file substitution to prevent data corruption. Also supports exporting to CSV.
- **📖 Read Student Data**: Load, search, filter, and display student records in formatted terminal tables or reload persisted records directly from disk.
- **🛡️ Handle Invalid Input using Exceptions**: Comprehensive custom exception hierarchy catches errors at the domain and application layers, displaying clear, actionable messages to the user without crashing.
- **📊 Analytics & Statistics**: Displays class average, pass/fail ratios, top & lowest performers, grade distribution histograms, and course demographics.
- **🧪 100% Tested**: 24 unit test cases verifying validation, regex rules, file IO, model behavior, and edge cases.

---

## 🏛️ Project Architecture

```
Student Record Manager/
│
├── student_manager/
│   ├── __init__.py           # Package exports
│   ├── exceptions.py         # Custom exception hierarchy
│   ├── validator.py          # Regex email & input validation logic
│   ├── models.py             # Student dataclass model & serialization
│   ├── storage.py            # JSON/CSV file storage & atomic persistence
│   └── manager.py            # Business logic, CRUD operations, & analytics
│
├── tests/
│   ├── __init__.py           # Test suite initializer
│   ├── test_validator.py     # Regex and validator unit tests
│   ├── test_models.py        # Student model unit tests
│   ├── test_storage.py       # Storage & file persistence unit tests
│   └── test_manager.py       # Manager CRUD & analytics unit tests
│
├── data/
│   ├── students.json         # Persistent JSON record database
│   └── students_export.csv   # Optional CSV spreadsheet export
│
├── .github/
│   └── workflows/
│       └── python-tests.yml  # GitHub Actions CI workflow
│
├── main.py                   # Interactive Command-Line Interface (CLI)
├── deploy_to_github.ps1      # 1-click GitHub deployment automation script
├── requirements.txt          # Project dependencies (zero-dependency core)
├── .gitignore                # Git ignore rules for Python
├── LICENSE                   # MIT License
└── README.md                 # Project documentation
```

---

## 📧 Email Regex Validation

Email validation uses the following regular expression pattern:

```python
EMAIL_REGEX = re.compile(
    r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9]+(?:-[a-zA-Z0-9]+)*(?:\.[a-zA-Z0-9]+(?:-[a-zA-Z0-9]+)*)*\.[a-zA-Z]{2,}$"
)
```

### Breakdown:

| Token | Meaning |
|---|---|
| `^[a-zA-Z0-9_.+-]+` | Starts with valid alphanumeric characters, underscores, dots, pluses, or hyphens |
| `@` | Required '@' symbol separating local-part and domain |
| `[a-zA-Z0-9]+(?:-[a-zA-Z0-9]+)*` | Domain name with support for internal hyphens |
| `(?:\.[a-zA-Z0-9]+(?:-[a-zA-Z0-9]+)*)*` | Optional subdomains (e.g. `dept.university.edu`) |
| `\.[a-zA-Z]{2,}$` | Top-Level Domain (TLD) of at least 2 alphabetic characters |

In addition to the regex pattern, the validator rejects consecutive dots (e.g., `user..name@domain.com`) and improper dot boundaries, raising `InvalidEmailError` if rules are violated.

---

## ⚠️ Exception Handling Architecture

The project features a dedicated exception hierarchy inheriting from `StudentRecordError`:

```
StudentRecordError (Base)
│
├── ValidationError (Data validation failure)
│   ├── InvalidEmailError       (Malformed email address)
│   ├── InvalidStudentIdError   (Invalid format or length < 3 chars)
│   ├── InvalidNameError        (Invalid characters or empty name)
│   ├── InvalidGradeError       (Marks < 0 or > 100 or non-numeric)
│   └── InvalidCourseError      (Empty or invalid course name)
│
├── StudentNotFoundError        (ID not found during lookup/update/delete)
├── DuplicateStudentError       (Attempting to add existing student ID)
└── StorageError                (Corrupted JSON, read/write I/O failures)
```

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.10 or higher.
- Git (optional, for deploying to GitHub).

### Installation & Setup

1. **Clone or navigate to the project directory**:
   ```bash
   cd "C:\Users\I.Jeevani\Desktop\Student Record Manager"
   ```

2. **(Optional) Create a virtual environment**:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   ```

3. **Install dependencies**:
   *(The core application uses the Python Standard Library with zero third-party dependencies required!)*
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

Execute `main.py` directly from the terminal:

```bash
python main.py
```

### CLI Menu Options:
```
========================================================================
             STUDENT RECORD MANAGEMENT SYSTEM                
       Validation * Regex Email * Persistent Storage * Reports
========================================================================

--- MAIN MENU ---
[1] Add New Student
[2] View All Students
[3] Search Student (ID, Name, Email, Course)
[4] Update Student Details
[5] Delete Student Record
[6] View Class Statistics & Performance
[7] Export Records to CSV
[8] Load Sample / Demo Records
[9] Reload Records from Disk
[0] Exit System
```

---

## 🧪 Running Unit Tests

Run all 24 unit tests using Python's built-in `unittest` runner:

```bash
python -m unittest discover -s tests -v
```

Expected output:
```
test_add_student_success ... ok
test_delete_student ... ok
test_duplicate_student_raises_exception ... ok
test_get_and_search_students ... ok
test_invalid_email_raises_exception ... ok
test_statistics_calculation ... ok
test_update_student ... ok
test_dict_serialization_roundtrip ... ok
test_student_factory_creation ... ok
test_student_update_validates_new_fields ... ok
test_corrupted_json_raises_storage_error ... ok
test_export_to_csv ... ok
test_load_non_existent_file_returns_empty_dict ... ok
test_save_and_load_records ... ok
test_course_validation ... ok
test_invalid_emails_raise_exception ... ok
test_invalid_marks_raise_exception ... ok
test_invalid_names_raise_exception ... ok
test_invalid_student_ids_raise_exception ... ok
test_letter_grade_calculation ... ok
test_valid_emails ... ok
test_valid_marks ... ok
test_valid_names ... ok
test_valid_student_ids ... ok

----------------------------------------------------------------------
Ran 24 tests in 0.020s

OK
```

---

## 🌐 How to Deploy to GitHub

### Method A: Using the Automated PowerShell Script (Easiest)

Run the included deployment script:
```powershell
powershell -ExecutionPolicy Bypass -File .\deploy_to_github.ps1
```
The script will guide you to log in with GitHub CLI (`gh`), create the remote repository, and push the code automatically.

---

### Method B: Manual Steps using Git and GitHub CLI

1. **Initialize Git and Stage Files**:
   ```bash
   git init -b main
   git add .
   git commit -m "feat: initial commit - Student Record Manager"
   ```

2. **Log into GitHub CLI**:
   ```bash
   gh auth login
   ```
   *(Select `GitHub.com`, choose `HTTPS`, and authenticate in browser or with a Personal Access Token).*

3. **Create the GitHub Repository and Push**:
   ```bash
   gh repo create student-record-manager --public --source=. --remote=origin --push
   ```

---

### Method C: Manual Push to an Existing GitHub Repository

1. Go to [GitHub.com/new](https://github.com/new) and create a repository named `student-record-manager`.
2. Run the following commands in your terminal:
   ```bash
   git init -b main
   git add .
   git commit -m "feat: Student Record Manager with regex validation and file storage"
   git remote add origin https://github.com/<your-username>/student-record-manager.git
   git branch -M main
   git push -u origin main
   ```

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).
