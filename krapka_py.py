import sqlite3
from faker import Faker
import random

fake = Faker()

conn = sqlite3.connect(r"C:\Users\katya\Documents\GitHub\PyWebDZ6\database")
cursor = conn.cursor()

tables = ["students", "groups", "teachers", "subjects", "grades"]

#створення таблиць
cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY,
        name TEXT,
        group_id INTEGER
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS groups (
        id INTEGER PRIMARY KEY,
        name TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS teachers (
        id INTEGER PRIMARY KEY,
        name TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS subjects (
        id INTEGER PRIMARY KEY,
        name TEXT,
        teacher_id INTEGER
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS grades (
        id INTEGER PRIMARY KEY,
        student_id INTEGER,
        subject_id INTEGER,
        grade INTEGER,
        date DATE
    )
''')

for table_name in tables:
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    result = cursor.fetchone()
    if result:
        print(f"Таблиця {table_name} створена")
    else:
        print(f"Таблиця {table_name} не була створена")

#заповнення students
for _ in range(50):
    cursor.execute('INSERT INTO students (name, group_id) VALUES (?, ?)', (fake.name(), random.randint(1, 3)))

#заповнення groups
for group_id in range(1, 4):
    cursor.execute('INSERT INTO groups (name) VALUES (?)', (f'Group {group_id}',))

#заповнення teachers
for _ in range(5):
    cursor.execute('INSERT INTO teachers (name) VALUES (?)', (fake.name(),))

#заповнення subjects
for subject_id in range(1, 9):
    cursor.execute('INSERT INTO subjects (name, teacher_id) VALUES (?, ?)', (fake.job(), random.randint(1, 5)))

#заповнення grades
for student_id in range(1, 51):
    for subject_id in range(1, 9):
        cursor.execute('INSERT INTO grades (student_id, subject_id, grade, date) VALUES (?, ?, ?, ?)',
                       (student_id, subject_id, random.randint(60, 100), fake.date_between(start_date='-1y', end_date='today')))



#знайти 5 студентів із найбільшим середнім балом з усіх предметів
cursor.execute('''
    SELECT students.name, AVG(grades.grade) as avg_grade
    FROM students
    JOIN grades ON students.id = grades.student_id
    GROUP BY students.id
    ORDER BY avg_grade DESC
    LIMIT 5
''')
result = cursor.fetchall()
print("Запит 1:")
for row in result:
    print(row)

#знайти студента із найвищим середнім балом з певного предмета
subject_id = 1
cursor.execute('''
    SELECT students.name, AVG(grades.grade) as avg_grade
    FROM students
    JOIN grades ON students.id = grades.student_id
    WHERE grades.subject_id = ?
    GROUP BY students.id
    ORDER BY avg_grade DESC
    LIMIT 1
''', (subject_id,))
result = cursor.fetchall()
print("Запит 2:")
for row in result:
    print(row)

#знайти середній бал у групах з певного предмета
subject_id = 1 
cursor.execute('''
    SELECT groups.name, AVG(grades.grade) as avg_grade
    FROM groups
    JOIN students ON groups.id = students.group_id
    JOIN grades ON students.id = grades.student_id
    WHERE grades.subject_id = ?
    GROUP BY groups.id
''', (subject_id,))
result = cursor.fetchall()
print("Запит 3:")
for row in result:
    print(row)

#знайти середній бал на потоці
cursor.execute('''
    SELECT AVG(grade) as avg_grade
    FROM grades
''')
result = cursor.fetchall()
print("Запит 4:")
for row in result:
    print(row)

#знайти які курси читає певний викладач
teacher_id = 1 
cursor.execute('''
    SELECT subjects.name
    FROM subjects
    WHERE subjects.teacher_id = ?
''', (teacher_id,))
result = cursor.fetchall()
print("Запит 5:")
for row in result:
    print(row)

#знайти список студентів у певній групі 
group_id = 1
cursor.execute('''
    SELECT students.name
    FROM students
    WHERE students.group_id = ?
''', (group_id,))
result = cursor.fetchall()
print("Запит 6:")
for row in result:
    print(row)

#знайти оцінки студентів у окремій групі з певного предмета
group_id = 1  
subject_id = 1 
cursor.execute('''
    SELECT students.name, grades.grade
    FROM students
    JOIN grades ON students.id = grades.student_id
    WHERE students.group_id = ? AND grades.subject_id = ?
''', (group_id, subject_id))
result = cursor.fetchall()
print("Запит 7:")
for row in result:
    print(row)

#знайти середній бал, який ставить певний викладач зі своїх предметів (замість <teacher_id> підставте ідентифікатор викладача)
teacher_id = 1 
cursor.execute('''
    SELECT AVG(grades.grade) as avg_grade
    FROM subjects
    JOIN grades ON subjects.id = grades.subject_id
    WHERE subjects.teacher_id = ?
''', (teacher_id,))
result = cursor.fetchall()
print("Запит 8:")
for row in result:
    print(row)

#знайти список курсів, які відвідує студент 
student_id = 1
cursor.execute('''
    SELECT subjects.name
    FROM subjects
    JOIN grades ON subjects.id = grades.subject_id
    WHERE grades.student_id = ?
''', (student_id,))
result = cursor.fetchall()
print("Запит 9:")
for row in result:
    print(row)

#список курсів, які певному студенту читає певний викладач 
student_id = 1  
teacher_id = 1 
cursor.execute('''
    SELECT subjects.name
    FROM subjects
    JOIN grades ON subjects.id = grades.subject_id
    JOIN students ON grades.student_id = students.id
    WHERE students.id = ? AND subjects.teacher_id = ?
''', (student_id, teacher_id))
result = cursor.fetchall()
print("Запит 10:")
for row in result:
    print(row)

#збереження змін та закриття з'єднання
conn.commit()
conn.close()