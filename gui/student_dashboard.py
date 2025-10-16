import tkinter as tk
from tkinter import ttk, messagebox
from models.marks_model import MarksModel
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

class StudentDashboard:
    def __init__(self, username):
        self.username = username
        self.root = tk.Tk()
        self.root.title("Student Dashboard - Student Result Management System")
        self.root.geometry("800x500")
        self.root.config(bg="#f4f6f7")

        self.marks_model = MarksModel()

        self.create_ui()
        self.load_my_results()

        self.root.mainloop()

    def create_ui(self):
        # --- Header ---
        tk.Label(
            self.root,
            text=f"🎓 Welcome, {self.username}",
            font=("Helvetica", 20, "bold"),
            fg="#1A5276",
            bg="#f4f6f7"
        ).pack(pady=20)

        # --- Table for Student Results ---
        columns = ("subject", "marks")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=10)
        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)

        self.tree.heading("subject", text="Subject")
        self.tree.heading("marks", text="Marks")

        self.tree.column("subject", anchor=tk.CENTER, width=200)
        self.tree.column("marks", anchor=tk.CENTER, width=100)

        # --- PDF Export Button ---
        tk.Button(
            self.root, text="📄 Download My Report", bg="#AF7AC5", fg="white",
            font=("Helvetica", 11, "bold"),
            command=self.export_pdf
        ).pack(pady=15)

    def load_my_results(self):
        """Load only the logged-in student's results"""
        for row in self.tree.get_children():
            self.tree.delete(row)

        results = self.marks_model.get_student_results(self.username)
        if results:
            for r in results:
                self.tree.insert("", tk.END, values=(r[0], r[1]))
        else:
            messagebox.showinfo("Info", "No results found for your account.")

    def export_pdf(self):
        """Generate PDF for logged-in student's marks"""
        results = self.marks_model.get_student_results(self.username)
        if not results:
            messagebox.showwarning("Warning", "No results to export!")
            return

        pdf_file = f"{self.username}_report.pdf"
        c = canvas.Canvas(pdf_file, pagesize=letter)
        width, height = letter

        c.setFont("Helvetica-Bold", 16)
        c.drawString(200, height - 50, f"Student Report: {self.username}")

        c.setFont("Helvetica", 12)
        y = height - 100
        c.drawString(100, y, "Subject")
        c.drawString(350, y, "Marks")

        c.line(90, y - 5, 500, y - 5)
        y -= 20

        for subject, marks in results:
            if y < 100:
                c.showPage()
                c.setFont("Helvetica", 12)
                y = height - 100

            c.drawString(100, y, str(subject))
            c.drawString(350, y, str(marks))
            y -= 20

        c.save()
        messagebox.showinfo("Success", f"PDF report saved as:\n{os.path.abspath(pdf_file)}")


if __name__ == "__main__":
    # For testing purposes only
    StudentDashboard("student1")
