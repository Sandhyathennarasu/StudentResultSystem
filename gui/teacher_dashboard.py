import tkinter as tk
from tkinter import ttk, messagebox
from models.marks_model import MarksModel
from models.user_model import UserModel
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

class TeacherDashboard:
    def __init__(self, username):  # ✅ accept username
        self.username = username
        self.root = tk.Tk()
        self.root.title(f"Teacher Dashboard - {self.username}")
        self.root.geometry("900x550")
        self.root.config(bg="#f4f6f7")

        self.marks_model = MarksModel()
        self.user_model = UserModel()

        self.create_ui()
        self.load_results()

        self.root.mainloop()

    def create_ui(self):
        # --- Header ---
        header_frame = tk.Frame(self.root, bg="#f4f6f7")
        header_frame.pack(pady=10, fill=tk.X)

        tk.Label(
            header_frame,
            text=f"📘 Welcome, {self.username}",
            font=("Helvetica", 20, "bold"),
            fg="#1A5276",
            bg="#f4f6f7"
        ).pack(side=tk.LEFT, padx=20)

        tk.Button(
            header_frame, text="Logout", bg="#E74C3C", fg="white",
            command=self.logout
        ).pack(side=tk.RIGHT, padx=20)

        # --- Search Bar ---
        search_frame = tk.Frame(self.root, bg="#f4f6f7")
        search_frame.pack(pady=10)

        tk.Label(search_frame, text="Search by Student Username:", bg="#f4f6f7").pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)

        tk.Button(
            search_frame, text="Search", bg="#27AE60", fg="white",
            command=self.search_student
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            search_frame, text="Show All", bg="#2E86C1", fg="white",
            command=self.load_results
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            search_frame, text="Export PDF", bg="#AF7AC5", fg="white",
            command=self.export_pdf
        ).pack(side=tk.LEFT, padx=5)

        # --- Results Table ---
        columns = ("username", "subject", "marks")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=10)
        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)

        self.tree.heading("username", text="Student Username")
        self.tree.heading("subject", text="Subject")
        self.tree.heading("marks", text="Marks")

        self.tree.column("username", anchor=tk.CENTER, width=150)
        self.tree.column("subject", anchor=tk.CENTER, width=150)
        self.tree.column("marks", anchor=tk.CENTER, width=100)

        # --- Add/Update Marks Section ---
        form_frame = tk.Frame(self.root, bg="#f4f6f7")
        form_frame.pack(pady=15)

        tk.Label(form_frame, text="Student Username:", bg="#f4f6f7").grid(row=0, column=0, padx=10, pady=5)
        self.username_entry = tk.Entry(form_frame)
        self.username_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Subject:", bg="#f4f6f7").grid(row=0, column=2, padx=10, pady=5)
        self.subject_entry = tk.Entry(form_frame)
        self.subject_entry.grid(row=0, column=3, padx=10, pady=5)

        tk.Label(form_frame, text="Marks:", bg="#f4f6f7").grid(row=0, column=4, padx=10, pady=5)
        self.marks_entry = tk.Entry(form_frame)
        self.marks_entry.grid(row=0, column=5, padx=10, pady=5)

        tk.Button(
            form_frame, text="Add Result", bg="#28B463", fg="white",
            command=self.add_result
        ).grid(row=0, column=6, padx=10)

    def load_results(self):
        """Load all results into the table"""
        for row in self.tree.get_children():
            self.tree.delete(row)

        query = "SELECT username, subject, marks FROM results"
        self.marks_model.cursor.execute(query)
        for row in self.marks_model.cursor.fetchall():
            self.tree.insert("", tk.END, values=row)

    def search_student(self):
        """Search results for specific student"""
        username = self.search_entry.get().strip()
        if not username:
            messagebox.showwarning("Warning", "Please enter a student username!")
            return

        for row in self.tree.get_children():
            self.tree.delete(row)

        results = self.marks_model.get_student_results(username)
        if results:
            for r in results:
                self.tree.insert("", tk.END, values=(username, r[0], r[1]))
        else:
            messagebox.showinfo("Info", f"No records found for {username}")

    def add_result(self):
        """Add or update student result"""
        username = self.username_entry.get().strip()
        subject = self.subject_entry.get().strip()
        marks = self.marks_entry.get().strip()

        if not (username and subject and marks):
            messagebox.showwarning("Warning", "All fields are required!")
            return

        self.marks_model.cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        student_exists = self.marks_model.cursor.fetchone()

        if not student_exists:
            messagebox.showerror("Error", "Student not found!")
            return

        try:
            marks = int(marks)
            self.marks_model.add_result(username, subject, marks)
            messagebox.showinfo("Success", f"Marks added for {username}")
            self.load_results()
        except ValueError:
            messagebox.showerror("Error", "Marks must be a number!")

    def export_pdf(self):
        """Export all results to a PDF file"""
        results = []
        for child in self.tree.get_children():
            results.append(self.tree.item(child)["values"])

        if not results:
            messagebox.showwarning("Warning", "No data available to export!")
            return

        pdf_file = "student_results.pdf"
        c = canvas.Canvas(pdf_file, pagesize=letter)
        width, height = letter

        c.setFont("Helvetica-Bold", 16)
        c.drawString(200, height - 50, "Student Results Report")

        c.setFont("Helvetica", 12)
        y = height - 100
        c.drawString(50, y, "Username")
        c.drawString(250, y, "Subject")
        c.drawString(450, y, "Marks")

        c.line(45, y - 5, 550, y - 5)
        y -= 20

        for row in results:
            if y < 100:
                c.showPage()
                c.setFont("Helvetica", 12)
                y = height - 100

            c.drawString(50, y, str(row[0]))
            c.drawString(250, y, str(row[1]))
            c.drawString(450, y, str(row[2]))
            y -= 20

        c.save()
        messagebox.showinfo("Success", f"PDF exported successfully!\nSaved as {os.path.abspath(pdf_file)}")

    def logout(self):
        """Close the dashboard"""
        self.root.destroy()


if __name__ == "__main__":
    TeacherDashboard("teacher1")  # test with a dummy username
