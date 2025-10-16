import tkinter as tk
from tkinter import ttk, messagebox
from models.user_model import UserModel
from models.marks_model import MarksModel
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

class AdminDashboard:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Admin Dashboard - Student Result Management System")
        self.root.geometry("900x550")
        self.root.config(bg="#f4f6f7")

        self.user_model = UserModel()
        self.marks_model = MarksModel()

        self.create_ui()
        self.load_users()
        self.load_results()

        self.root.mainloop()

    def create_ui(self):
        # --- Header ---
        tk.Label(
            self.root,
            text="⚙️ Admin Dashboard",
            font=("Helvetica", 22, "bold"),
            fg="#1A5276",
            bg="#f4f6f7"
        ).pack(pady=15)

        # --- Tabs ---
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Create frames for tabs
        self.user_frame = tk.Frame(notebook, bg="#f4f6f7")
        self.result_frame = tk.Frame(notebook, bg="#f4f6f7")

        notebook.add(self.user_frame, text="👥 Manage Users")
        notebook.add(self.result_frame, text="📊 View All Results")

        # === Manage Users Tab ===
        self.create_user_tab()

        # === View All Results Tab ===
        self.create_results_tab()

    # -------------------- USERS TAB --------------------
    def create_user_tab(self):
        # --- User Table ---
        columns = ("Username", "Password", "Role")
        self.user_tree = ttk.Treeview(self.user_frame, columns=columns, show="headings", height=10)
        for col in columns:
            self.user_tree.heading(col, text=col)
            self.user_tree.column(col, anchor=tk.CENTER, width=180)
        self.user_tree.pack(fill=tk.BOTH, expand=True, pady=10)

        # --- Form to Add User ---
        form_frame = tk.Frame(self.user_frame, bg="#f4f6f7")
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Username:", bg="#f4f6f7").grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = tk.Entry(form_frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Password:", bg="#f4f6f7").grid(row=0, column=2, padx=5, pady=5)
        self.password_entry = tk.Entry(form_frame, show="*")
        self.password_entry.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(form_frame, text="Role:", bg="#f4f6f7").grid(row=0, column=4, padx=5, pady=5)
        self.role_box = ttk.Combobox(form_frame, values=["admin", "teacher", "student"], state="readonly", width=10)
        self.role_box.grid(row=0, column=5, padx=5, pady=5)
        self.role_box.set("student")

        tk.Button(
            form_frame, text="Add User", bg="#27AE60", fg="white",
            font=("Helvetica", 10, "bold"), command=self.add_user
        ).grid(row=0, column=6, padx=10)

        tk.Button(
            form_frame, text="Delete User", bg="#E74C3C", fg="white",
            font=("Helvetica", 10, "bold"), command=self.delete_user
        ).grid(row=0, column=7, padx=10)

    def load_users(self):
        """Load users into the table"""
        for row in self.user_tree.get_children():
            self.user_tree.delete(row)

        for user in self.user_model.get_all_users():
            self.user_tree.insert("", tk.END, values=user)

    def add_user(self):
        """Add a new user"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        role = self.role_box.get()

        if not (username and password and role):
            messagebox.showwarning("Warning", "All fields are required!")
            return

        success = self.user_model.add_user(username, password, role)
        if success:
            messagebox.showinfo("Success", f"User '{username}' added successfully!")
            self.load_users()
        else:
            messagebox.showerror("Error", "Username already exists or failed to add user.")

    def delete_user(self):
        """Delete selected user"""
        selected = self.user_tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a user to delete!")
            return

        username = self.user_tree.item(selected, "values")[0]
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure to delete '{username}'?")
        if confirm:
            self.user_model.delete_user(username)
            self.load_users()
            messagebox.showinfo("Deleted", f"User '{username}' deleted successfully!")

    # -------------------- RESULTS TAB --------------------
    def create_results_tab(self):
        # --- Results Table ---
        columns = ("Username", "Subject", "Marks")
        self.result_tree = ttk.Treeview(self.result_frame, columns=columns, show="headings", height=10)
        for col in columns:
            self.result_tree.heading(col, text=col)
            self.result_tree.column(col, anchor=tk.CENTER, width=200)
        self.result_tree.pack(fill=tk.BOTH, expand=True, pady=10)

        # --- Export PDF Button ---
        tk.Button(
            self.result_frame, text="📄 Export All Results to PDF",
            bg="#8E44AD", fg="white", font=("Helvetica", 11, "bold"),
            command=self.export_all_results_pdf
        ).pack(pady=10)

    def load_results(self):
        """Load all student results"""
        for row in self.result_tree.get_children():
            self.result_tree.delete(row)

        results = self.marks_model.get_all_results()
        if results:
            for r in results:
                self.result_tree.insert("", tk.END, values=r)

    def export_all_results_pdf(self):
        """Export all results to PDF"""
        results = self.marks_model.get_all_results()
        if not results:
            messagebox.showwarning("Warning", "No results to export!")
            return

        pdf_file = "All_Student_Results.pdf"
        c = canvas.Canvas(pdf_file, pagesize=letter)
        width, height = letter

        c.setFont("Helvetica-Bold", 16)
        c.drawString(200, height - 50, "All Student Results Report")

        c.setFont("Helvetica", 12)
        y = height - 100
        c.drawString(100, y, "Username")
        c.drawString(300, y, "Subject")
        c.drawString(480, y, "Marks")

        c.line(90, y - 5, 520, y - 5)
        y -= 20

        for username, subject, marks in results:
            if y < 100:
                c.showPage()
                c.setFont("Helvetica", 12)
                y = height - 100

            c.drawString(100, y, str(username))
            c.drawString(300, y, str(subject))
            c.drawString(480, y, str(marks))
            y -= 20

        c.save()
        messagebox.showinfo("Success", f"All student results exported to:\n{os.path.abspath(pdf_file)}")


if __name__ == "__main__":
    AdminDashboard()
