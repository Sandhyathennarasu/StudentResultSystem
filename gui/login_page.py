import tkinter as tk
import os
import sqlite3

DB_FILE = "student_result.db"

def initialize_database():
    """Create DB and tables only if they don't exist"""
    if not os.path.exists(DB_FILE):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT,
                role TEXT
            )
        """)

        # Create results table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                subject TEXT,
                marks INTEGER
            )
        """)

        # Add some default users
        default_users = [
            ("admin", "admin123", "admin"),
            ("teacher1", "teach123", "teacher"),
            ("student1", "stud123", "student"),
            ("student2", "stud234", "student")
        ]

        for u in default_users:
            try:
                cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", u)
            except sqlite3.IntegrityError:
                pass

        conn.commit()
        conn.close()
        print("✅ Database initialized automatically.")
    else:
        print("✅ Database already exists — skipped initialization.")


# Call the function before starting login page
initialize_database()

from tkinter import messagebox
from models.user_model import UserModel
from gui.student_dashboard import StudentDashboard
from gui.teacher_dashboard import TeacherDashboard
from gui.admin_dashboard import AdminDashboard


class LoginApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Student Result Management System - Login")
        self.root.geometry("400x350")
        self.root.config(bg="#f4f6f7")

        self.user_model = UserModel()

        tk.Label(self.root, text="🔐 Login", font=("Helvetica", 20, "bold"), fg="#1A5276", bg="#f4f6f7").pack(pady=20)

        tk.Label(self.root, text="Username:", bg="#f4f6f7").pack(pady=5)
        self.username_entry = tk.Entry(self.root, width=30)
        self.username_entry.pack(pady=5)

        tk.Label(self.root, text="Password:", bg="#f4f6f7").pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*", width=30)
        self.password_entry.pack(pady=5)

        tk.Button(
            self.root, text="Login", bg="#2E86C1", fg="white",
            font=("Helvetica", 11, "bold"), command=self.login
        ).pack(pady=20)

        self.root.mainloop()

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not (username and password):
            messagebox.showwarning("Warning", "Please enter both username and password.")
            return

        user = self.user_model.validate_user(username, password)
        if user:
            role = user[2]  # Assuming (username, password, role)
            messagebox.showinfo("Success", f"Welcome {username}! Logged in as {role.capitalize()}.")
            self.root.destroy()

            if role == "admin":
                AdminDashboard()
            elif role == "teacher":
                TeacherDashboard(username)
            elif role == "student":
                StudentDashboard(username)
        else:
            messagebox.showerror("Error", "Invalid username or password!")


if __name__ == "__main__":
    LoginApp()
