import sqlite3

db = sqlite3.connect("src/itctms_system.db")
cursor = db.cursor()


async def db_start():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY,
            telegram_id INTEGER,
            student_tg_username TEXT,
            name TEXT,
            surname TEXT,
            mid_name TEXT,
            grade INTEGER,
            student_group INTEGER
        )
    ''')

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

    db.commit()

    
    
    
    
    

async def insert_student(telegram_id, student_tg_username, name, surname, mid_name, grade, student_group):
    cursor.execute(
        """
        INSERT OR IGNORE INTO students (telegram_id,student_tg_username, name, surname, mid_name, grade, student_group)
        VALUES (?, ?, ?, ?, ?, ?,?)
        """,
        (telegram_id,student_tg_username, name, surname, mid_name, grade, student_group)
    )
    db.commit()


async def insert_event(name, date, place,kvota,info, details, registration_expire_date,points):
    # Создание подключения к базе данных
    # Вставка данных в таблицу events
    cursor.execute('''
        INSERT INTO events (name, date, place, kvota, info, details, registration_expire_date, points)
        VALUES (?, ?, ?, ?, ?, ?,?,?)
    ''', (name, date, place, kvota, info, details, registration_expire_date, points))

    # Сохранение изменений и закрытие подключения к базе данных
    db.commit()


    
