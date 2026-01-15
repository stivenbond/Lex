import sqlite3
import json
import os

DB_NAME = "educanvas.db"

class DBManager:
    def __init__(self, db_path=DB_NAME):
        self.db_path = db_path
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def init_db(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Load schema from SQL file
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
        with open(schema_path, 'r') as f:
            schema_script = f.read()
            
        cursor.executescript(schema_script)
        conn.commit()
        conn.close()

    def execute_query(self, query, params=()):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        conn.close()

    def fetch_all(self, query, params=()):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        return results

    def fetch_one(self, query, params=()):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        result = cursor.fetchone()
        conn.close()
        return result

    def create_lesson(self, title, content_json):
        query = "INSERT INTO lessons (title, raw_content) VALUES (?, ?)"
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (title, json.dumps(content_json)))
        lesson_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return lesson_id

    def create_diary_entry(self, lesson_id, cohort_name, data_json):
        query = "INSERT INTO diaries (lesson_id, cohort_name, data) VALUES (?, ?, ?)"
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (lesson_id, cohort_name, json.dumps(data_json)))
        diary_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return diary_id
