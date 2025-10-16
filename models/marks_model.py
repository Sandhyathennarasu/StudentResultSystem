import sqlite3

class MarksModel:
    def __init__(self):
        self.conn = sqlite3.connect("student_result.db")
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                subject TEXT,
                marks INTEGER
            )
        """)
        self.conn.commit()

    # Fetch all results for a specific student
    def get_student_results(self, username):
        self.cursor.execute("SELECT subject, marks FROM results WHERE username=?", (username,))
        return self.cursor.fetchall()

    # Add new result (used by teacher/admin)
    def add_result(self, username, subject, marks):
        self.cursor.execute(
            "INSERT INTO results (username, subject, marks) VALUES (?, ?, ?)",
            (username, subject, marks)
        )
        self.conn.commit()

    def close_connection(self):
        self.conn.close()
