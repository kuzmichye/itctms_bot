import sqlite3

db = sqlite3.connect("src/students.db")
cursor = db.cursor()


async def db_start():
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS students (
        student_id INTEGER PRIMARY KEY,
        student_tg_username INTEGER,
        name TEXT,
        surname TEXT,
        mid_name TEXT,
        grade INTEGER,
        student_group INTEGER
        )
    """
    )
    

async def insert_student(student_tg_username, name, surname, mid_name, grade, student_group):
    cursor.execute(
        """
        INSERT INTO students (student_tg_username, name, surname, mid_name, grade, student_group)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (student_tg_username, name, surname, mid_name, grade, student_group)
    )
    db.commit()