import tkinter as tk
from tkinter import ttk, messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from models.marks_model import MarksModel

class StudentDashboard:
    def __init__(self, username):
        self.username = username
        self.window = tk.Tk()
        self.window.title("Student Dashboard")
        self.window.geometry("650x500")
        self.window.config(bg="#f7f9fb")

        self.model = MarksModel()

        # Heading
        tk.Label(self.window, text=f"Welcome, {self.username}",
                 font=("Arial", 18, "bold"), bg="#f7f9fb").pack(pady=10)

        tk.Label(self.window, text="Your Results",
                 font=("Arial", 16, "bold"), fg="blue", bg="#f7f9fb").pack(pady=5)

        # Results table
        self.tree = ttk.Treeview(self.window, columns=("subject", "marks"), show="headings", height=10)
        self.tree.heading("subject", text="Subject")
        self.tree.heading("marks", text="Marks")
        self.tree.column("subject", width=250)
        self.tree.column("marks", width=100, anchor="center")
        self.tree.pack(pady=10)

        # Buttons
        btn_frame = tk.Frame(self.window, bg="#f7f9fb")
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Download PDF", command=self.generate_pdf,
                  font=("Arial", 12), bg="green", fg="white", width=15).grid(row=0, column=0, padx=10)

        tk.Button(btn_frame, text="Logout", command=self.logout,
                  font=("Arial", 12), bg="red", fg="white", width=15).grid(row=0, column=1, padx=10)

        self.load_results()
        self.window.mainloop()

    # --- Load student results ---
    def load_results(self):
        self.tree.delete(*self.tree.get_children())
        results = self.model.get_student_results(self.username)

        if not results:
            messagebox.showinfo("Info", "No results found!")
            return

        for row in results:
            self.tree.insert("", "end", values=row)

    # --- PDF Generation ---
    def generate_pdf(self):
        results = self.model.get_student_results(self.username)
        if not results:
            messagebox.showwarning("No Data", "No results available to generate PDF!")
            return

        pdf_filename = f"{self.username}_results.pdf"
        c = canvas.Canvas(pdf_filename, pagesize=letter)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(200, 750, "Student Result Report")

        c.setFont("Helvetica", 12)
        c.drawString(50, 710, f"Student Name: {self.username}")

        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, 680, "Subject")
        c.drawString(300, 680, "Marks")
        c.line(50, 675, 550, 675)

        y = 650
        for subject, marks in results:
            c.setFont("Helvetica", 12)
            c.drawString(50, y, str(subject))
            c.drawString(300, y, str(marks))
            y -= 25

        c.save()
        messagebox.showinfo("Success", f"PDF saved as {pdf_filename}")

    def logout(self):
        self.window.destroy()


if __name__ == "__main__":
    StudentDashboard("student1")
