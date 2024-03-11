import sqlite3

db = sqlite3.connect("src/itctms_system.db",isolation_level=None)
cursor = db.cursor()


async def db_start():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            event_id INTEGER PRIMARY KEY,
            name TEXT,
            date TEXT,
            place TEXT,
            kvota INTEGER,
            info TEXT,
            details TEXT,
            registration_expire_date TEXT,
            points INTEGER
        )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS registrations (
        student_tg_id INTEGER,
        event_id INTEGER,
        registration_time TEXT,
        registration_platform TEXT
    )
''')
    db.commit()



    
    

# async def insert_student(telegram_id, student_tg_username, name, surname, mid_name, grade, student_group):
#     cursor.execute(
#         """
#         INSERT OR IGNORE INTO students (telegram_id, student_tg_username, name, surname, mid_name, grade, student_group)
#         VALUES (?, ?, ?, ?, ?, ?, ?)
#         """,
#         (telegram_id, student_tg_username, name, surname, mid_name, grade, student_group)
#     )
#     db.commit()

    




