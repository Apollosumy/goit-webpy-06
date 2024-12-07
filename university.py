import sqlite3
from faker import Faker
import random
from datetime import datetime

# Ініціалізація Faker
faker = Faker()

# Підключення до бази даних
conn = sqlite3.connect('university.db')
cursor = conn.cursor()

# Створення таблиць
cursor.executescript("""
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS groups;
DROP TABLE IF EXISTS teachers;
DROP TABLE IF EXISTS subjects;
DROP TABLE IF EXISTS grades;

CREATE TABLE groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE teachers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    teacher_id INTEGER NOT NULL,
    FOREIGN KEY (teacher_id) REFERENCES teachers (id)
);

CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    group_id INTEGER NOT NULL,
    FOREIGN KEY (group_id) REFERENCES groups (id)
);

CREATE TABLE grades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    subject_id INTEGER NOT NULL,
    grade INTEGER NOT NULL,
    date_received DATE NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students (id),
    FOREIGN KEY (subject_id) REFERENCES subjects (id)
);
""")

# Додавання даних
# Додавання груп
groups = ["Group A", "Group B", "Group C"]
cursor.executemany("INSERT INTO groups (name) VALUES (?)", [(group,) for group in groups])

# Додавання викладачів
teachers = [faker.name() for _ in range(5)]
cursor.executemany("INSERT INTO teachers (name) VALUES (?)", [(teacher,) for teacher in teachers])

# Додавання предметів
subjects = ["Math", "Physics", "Chemistry", "Biology", "History", "Literature", "Programming", "Philosophy"]
subjects_data = [(subject, random.randint(1, len(teachers))) for subject in subjects]
cursor.executemany("INSERT INTO subjects (name, teacher_id) VALUES (?, ?)", subjects_data)

# Додавання студентів
students = [(faker.name(), random.randint(1, len(groups))) for _ in range(50)]
cursor.executemany("INSERT INTO students (name, group_id) VALUES (?, ?)", students)

# Додавання оцінок
grades = []
student_ids = [row[0] for row in cursor.execute("SELECT id FROM students").fetchall()]
subject_ids = [row[0] for row in cursor.execute("SELECT id FROM subjects").fetchall()]
for student_id in student_ids:
    for _ in range(random.randint(15, 20)):
        grades.append((
            student_id,
            random.choice(subject_ids),
            random.randint(60, 100),
            faker.date_between(start_date='-1y', end_date='today')
        ))
cursor.executemany("INSERT INTO grades (student_id, subject_id, grade, date_received) VALUES (?, ?, ?, ?)", grades)

# Збереження змін і закриття
conn.commit()
