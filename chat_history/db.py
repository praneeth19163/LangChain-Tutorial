import sqlite3
from faker import Faker
import random

# Initialize Faker
fake = Faker()

# Define domains and salary ranges
domains = ["Python", "Java", "JavaScript", "C++", "Go", "Ruby", "Swift", "Kotlin", "PHP", "R"]
salary_range = (50000, 150000)

# Connect to SQLite database
conn = sqlite3.connect("employee.db")
cursor = conn.cursor()

# Create employees table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    mail TEXT UNIQUE NOT NULL,
    domain TEXT NOT NULL,
    salary INTEGER NOT NULL
)
''')

# Generate 500+ employee records
employees_data = []
for _ in range(500):
    name = fake.name()
    mail = fake.unique.email()
    domain = random.choice(domains)
    salary = random.randint(*salary_range)
    employees_data.append((name, mail, domain, salary))

# Insert data into the database
cursor.executemany("INSERT INTO employees (name, mail, domain, salary) VALUES (?, ?, ?, ?)", employees_data)

# Commit and close connection
conn.commit()
conn.close()

print("Database populated with 500+ employees successfully!")
