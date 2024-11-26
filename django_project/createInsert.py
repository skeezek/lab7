import psycopg2
from psycopg2 import sql

# Параметри підключення
db_params = {
    "dbname": "app",
    "user": "postgres",
    "password": "102712",
    "host": "localhost",
    "port": 5432
}

# SQL для створення таблиць
CREATE_TABLES = """
CREATE TABLE IF NOT EXISTS Students (
    student_id SERIAL PRIMARY KEY,
    last_name VARCHAR(50) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    patronymic VARCHAR(50),
    address TEXT,
    phone VARCHAR(15) CHECK (phone ~ '^\\+?[0-9]+$'),
    course INTEGER CHECK (course BETWEEN 1 AND 4),
    faculty VARCHAR(50) CHECK (faculty IN ('Аграрного менеджменту', 'Економіки', 'Інформаційних технологій')),
    group_name VARCHAR(10),
    is_headman BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS Subjects (
    subject_id SERIAL PRIMARY KEY,
    subject_name VARCHAR(100) NOT NULL,
    hours_per_semester INTEGER NOT NULL CHECK (hours_per_semester > 0),
    semesters_count INTEGER NOT NULL CHECK (semesters_count > 0)
);

CREATE TABLE IF NOT EXISTS Exams (
    exam_id SERIAL PRIMARY KEY,
    exam_date DATE NOT NULL,
    student_id INTEGER REFERENCES Students(student_id),
    subject_id INTEGER REFERENCES Subjects(subject_id),
    grade INTEGER CHECK (grade BETWEEN 2 AND 5)
);
"""

# Дані для заповнення таблиць
INSERT_DATA = """
INSERT INTO Students (last_name, first_name, patronymic, address, phone, course, faculty, group_name, is_headman)
VALUES 
    ('Іванов', 'Іван', 'Іванович', 'вул. Лесі Українки, 12', '+380501234567', 1, 'Економіки', 'ЕК-101', FALSE),
    ('Петренко', 'Петро', 'Петрович', 'вул. Миру, 10', '+380972345678', 3, 'Інформаційних технологій', 'ІТ-303', TRUE);

INSERT INTO Subjects (subject_name, hours_per_semester, semesters_count)
VALUES
    ('Математика', 60, 2),
    ('Програмування', 90, 3),
    ('Економіка', 45, 1);

INSERT INTO Exams (exam_date, student_id, subject_id, grade)
VALUES
    ('2024-01-20', 1, 1, 5),
    ('2024-03-15', 1, 2, 4),
    ('2024-06-10', 2, 3, 3);
"""

# Створення бази, таблиць та наповнення
def setup_database():
    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Створення таблиць
        cursor.execute(CREATE_TABLES)
        conn.commit()

        # Наповнення таблиць
        cursor.execute(INSERT_DATA)
        conn.commit()

        print("Database setup complete.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

setup_database()