import sqlite3

class UserModel:
    def __init__(self):
        self.conn = sqlite3.connect("student_result.db")
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """Create users table if not exists"""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT,
                role TEXT
            )
        """)
        self.conn.commit()

    # --- Add new user (used by admin) ---
    def add_user(self, username, password, role):
        try:
            # Ensure table exists
            self.create_table()

            # Perform insertion
            self.cursor.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                (username, password, role)
            )
            self.conn.commit()
            return True

        except sqlite3.IntegrityError:
            # Username already exists
            return "exists"
        except Exception as e:
            print("Error adding user:", e)
            return str(e)

    # --- Fetch all users (for admin display) ---
    def get_all_users(self, role=None):
        try:
            if role:
                self.cursor.execute(
                    "SELECT username, password FROM users WHERE role=?", (role,))
            else:
                self.cursor.execute(
                    "SELECT username, password, role FROM users")
            return self.cursor.fetchall()
        except Exception as e:
            print("Error fetching users:", e)
            return []

    # --- Delete user by username ---
    def delete_user(self, username):
        try:
            self.cursor.execute("DELETE FROM users WHERE username=?", (username,))
            self.conn.commit()
            return True
        except Exception as e:
            print("Error deleting user:", e)
            return False

    # --- Validate login credentials ---
    def validate_user(self, username, password):
        query = "SELECT username, password, role FROM users WHERE username=? AND password=?"
        self.cursor.execute(query, (username, password))
        return self.cursor.fetchone()


    def close_connection(self):
        self.conn.close()
