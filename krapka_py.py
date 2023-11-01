import sqlite3
from faker import Faker
import random
import datetime

fake = Faker()


conn = sqlite3.connect(r"C:\Users\katya\Documents\GitHub\PyWebDZ6\database")
cursor = conn.cursor()

for _ in range(50):
    cursor.execute('INSERT INTO students (name, group_id) VALUES (?, ?)', (fake.name(), random.randint(1, 3)))

for group_id in range(1, 4):  #групи
    cursor.execute('INSERT INTO groups (name) VALUES (?)', (f'Group {group_id}',))

for _ in range(5):  #викладачі
    cursor.execute('INSERT INTO teachers (name) VALUES (?)', (fake.name(),))

for subject_id in range(1, 9):  #предмети
    cursor.execute('INSERT INTO subjects (name, teacher_id) VALUES (?, ?)', (fake.job(), random.randint(1, 5)))

for student_id in range(1, 51):  #оцінки
    for subject_id in range(1, 9):
        cursor.execute('INSERT INTO grades (student_id, subject_id, grade, date) VALUES (?, ?, ?, ?)',
                       (student_id, subject_id, random.randint(60, 100), fake.date_between(start_date='-1y', end_date='today')))

# Зберегти зміни та закрити з'єднання
conn.commit()
conn.close()
