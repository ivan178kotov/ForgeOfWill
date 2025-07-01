import sqlite3

DB_NAME = "forge_of_will.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Таблица пользователей
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        level INTEGER DEFAULT 1,
        os INTEGER DEFAULT 0,
        last_active DATE
    )
    ''')

    # Таблица прогресса
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS progress (
        progress_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        quest_type TEXT,
        completion_date DATE,
        count INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )
    ''')

    # Таблица артефактов
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS artifacts (
        artifact_id INTEGER PRIMARY KEY,
        name TEXT,
        description TEXT,
        cost INTEGER
    )''')

    # Стандартные артефакты
    default_artifacts = [
        (1, "Энергетический заряд", "Книга по мотивации", 100),
        (2, "Стальной амулет", "Качественный фитнес-браслет", 250),
        (3, "Плащ преодоления", "Билет на мастер-класс", 500),
        (4, "Легендарный клинок", "Путешествие в горы", 1000)
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO artifacts VALUES (?, ?, ?, ?)",
        default_artifacts
    )

    conn.commit()
    conn.close()


def get_user(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user


def create_user(user_id, username):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)",
        (user_id, username)
    )
    conn.commit()
    conn.close()


def update_os(user_id, amount):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET os = os + ? WHERE user_id = ?",
        (amount, user_id)
    )
    conn.commit()
    conn.close()


def record_progress(user_id, quest_type):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    cursor.execute(
        "INSERT INTO progress (user_id, quest_type, completion_date, count) VALUES (?, ?, ?, 1)",
        (user_id, quest_type, today)
    )
    conn.commit()
    conn.close()


# Инициализация БД при импорте
init_db()