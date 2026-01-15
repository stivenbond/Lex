import sqlite3
import os

def init_db(db_path="lex_database.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Teachers
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS teachers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    ''')

    # Syllabuses
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS syllabuses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        teacher_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        academic_year TEXT,
        FOREIGN KEY (teacher_id) REFERENCES teachers(id)
    )
    ''')

    # Topics
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS topics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        syllabus_id INTEGER NOT NULL,
        topic_id_string TEXT,
        name TEXT NOT NULL,
        order_index INTEGER NOT NULL,
        FOREIGN KEY (syllabus_id) REFERENCES syllabuses(id)
    )
    ''')

    # Diary Fields (Schema definition)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS diary_fields (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        teacher_id INTEGER NOT NULL,
        label TEXT NOT NULL,
        description TEXT,
        stability TEXT CHECK(stability IN ('STATIC', 'DYNAMIC')) NOT NULL,
        FOREIGN KEY (teacher_id) REFERENCES teachers(id)
    )
    ''')

    # Cohorts
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cohorts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        teacher_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        FOREIGN KEY (teacher_id) REFERENCES teachers(id)
    )
    ''')

    # Diary Entries
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS diary_entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        teacher_id INTEGER NOT NULL,
        topic_id INTEGER NOT NULL,
        cohort_id INTEGER NOT NULL,
        teaching_date TEXT NOT NULL,
        is_reference BOOLEAN NOT NULL DEFAULT 0,
        reference_entry_id INTEGER,
        FOREIGN KEY (teacher_id) REFERENCES teachers(id),
        FOREIGN KEY (topic_id) REFERENCES topics(id),
        FOREIGN KEY (cohort_id) REFERENCES cohorts(id),
        FOREIGN KEY (reference_entry_id) REFERENCES diary_entries(id) ON DELETE SET NULL
    )
    ''')

    # Diary Values
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS diary_values (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        entry_id INTEGER NOT NULL,
        field_id INTEGER NOT NULL,
        value TEXT,
        FOREIGN KEY (entry_id) REFERENCES diary_entries(id) ON DELETE CASCADE,
        FOREIGN KEY (field_id) REFERENCES diary_fields(id)
    )
    ''')

    # Text Blocks (Lesson Content)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS text_blocks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic_id INTEGER NOT NULL,
        content TEXT NOT NULL,
        order_index INTEGER NOT NULL,
        x REAL DEFAULT 0,
        y REAL DEFAULT 0,
        FOREIGN KEY (topic_id) REFERENCES topics(id) ON DELETE CASCADE
    )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
