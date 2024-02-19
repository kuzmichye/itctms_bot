import sqlite3

db = sqlite3.connect("src/itctms_system.db")
cursor = db.cursor()

async def db_start():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY,
            surname TEXT,
            name TEXT,
            mid_name TEXT,
            ticket TEXT,
            institute TEXT,
            grade TEXT,
            number_group INTEGER,
            vk_username TEXT,
            tg_username TEXT
        )
    ''')
    db.commit()

'''async def check_ticket(db,ticket):
    cursor = db.cursor()
    # Проверка студенческого билета в базе данных
    cursor.execute("SELECT * FROM students WHERE ticket = ?", (ticket,))
    result = cursor.fetchone()

    if result:
        return 'Добро пожаловать!'
    else:
        return 'Не удалось найти ваш студенческий билет'''