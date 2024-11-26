import psycopg2
from prettytable import PrettyTable

# Підключення до бази даних PostgreSQL
conn = psycopg2.connect(
    dbname="app",
    user="postgres",
    password="102712",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Функція для виконання SQL-запитів і виведення результатів
def execute_query(query, params=None):
    cursor.execute(query, params)
    return cursor.fetchall()

# Функція для виведення даних в табличному форматі
def print_table(headers, data):
    table = PrettyTable(headers)
    for row in data:
        table.add_row(row)
    print(table)

# 1. Відобразити всіх студентів, які є старостами, відсортованих за прізвищем
print("\n1. Студенти-старости, відсортовані за прізвищем:")
query = """
    SELECT last_name, first_name, group_name
    FROM Students
    WHERE is_headman = TRUE
    ORDER BY last_name;
"""
data = execute_query(query)
print_table(["Прізвище", "Ім'я", "Група"], data)

# 2. Середній бал для кожного студента
print("\n2. Середній бал для кожного студента:")
query = """
    SELECT s.last_name, s.first_name, AVG(e.grade) AS average_grade
    FROM Exams e
    JOIN Students s ON e.student_id = s.student_id
    GROUP BY s.student_id, s.last_name, s.first_name
    ORDER BY average_grade DESC;
"""
data = execute_query(query)
print_table(["Прізвище", "Ім'я", "Середній бал"], data)

# 3. Загальна кількість годин для кожного предмету
print("\n3. Загальна кількість годин для кожного предмету:")
query = """
    SELECT subject_name, hours_per_semester * semesters_count AS total_hours
    FROM Subjects;
"""
data = execute_query(query)
print_table(["Назва предмету", "Загальна кількість годин"], data)

# 4. Успішність студентів по обраному предмету
print("\n4. Успішність студентів по обраному предмету:")
subject_id = int(input("Введіть ID предмету: "))
query = """
    SELECT s.last_name, s.first_name, e.grade
    FROM Exams e
    JOIN Students s ON e.student_id = s.student_id
    WHERE e.subject_id = %s;
"""
data = execute_query(query, (subject_id,))
print_table(["Прізвище", "Ім'я", "Оцінка"], data)

# 5. Кількість студентів на кожному факультеті
print("\n5. Кількість студентів на кожному факультеті:")
query = """
    SELECT faculty, COUNT(*) AS student_count
    FROM Students
    GROUP BY faculty;
"""
data = execute_query(query)
print_table(["Факультет", "Кількість студентів"], data)

# 6. Оцінки кожного студента по кожному предмету
print("\n6. Оцінки кожного студента по кожному предмету:")
query = """
    SELECT s.last_name, s.first_name, sub.subject_name, e.grade
    FROM Exams e
    JOIN Students s ON e.student_id = s.student_id
    JOIN Subjects sub ON e.subject_id = sub.subject_id
    ORDER BY s.last_name, sub.subject_name;
"""
data = execute_query(query)
print_table(["Прізвище", "Ім'я", "Предмет", "Оцінка"], data)

# Закриття з'єднання
cursor.close()
conn.close()