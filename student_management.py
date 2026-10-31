import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

APP_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(APP_DIR, "students.csv")

FIELDS = ["Student ID", "Name", "Class", "Study Time", "Absences"]


class StudentManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Performance AI - Student Management")
        self.root.geometry("1000x650")
        self.root.minsize(850, 550)
        self.root.configure(bg="#101827")

        self.colors = {
            "bg": "#101827",
            "panel": "#1b2638",
            "field": "#263449",
            "text": "#f3f4f6",
            "muted": "#aab6c5",
            "accent": "#8b5cf6",
            "accent_hover": "#7c3aed",
            "danger": "#dc2626",
            "border": "#344256",
        }

        self.students = []
        self.build_ui()
        self.load_students()
        self.refresh_table()

    def build_ui(self):
        header = tk.Frame(self.root, bg=self.colors["bg"])
        header.pack(fill="x", padx=24, pady=(20, 12))

        tk.Label(
            header,
            text="Student Management",
            font=("Arial", 22, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["text"],
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Add, search, view and remove student records",
            font=("Arial", 10),
            bg=self.colors["bg"],
            fg=self.colors["muted"],
        ).pack(anchor="w", pady=(5, 0))

        form = tk.LabelFrame(
            self.root,
            text=" Student Details ",
            font=("Arial", 11, "bold"),
            bg=self.colors["panel"],
            fg=self.colors["text"],
            bd=1,
            relief="solid",
            padx=14,
            pady=12,
        )
        form.pack(fill="x", padx=24, pady=8)

        self.entries = {}
        labels = [
            ("Student ID", "e.g. STU001"),
            ("Name", "Enter full name"),
            ("Class", "e.g. MCA 1"),
            ("Study Time", "1 to 4 hours category"),
            ("Absences", "Number of absences"),
        ]

        for index, (field, placeholder) in enumerate(labels):
            row, col = divmod(index, 3)
            cell = tk.Frame(form, bg=self.colors["panel"])
            cell.grid(row=row, column=col, sticky="ew", padx=8, pady=7)
            tk.Label(
                cell,
                text=field,
                font=("Arial", 9, "bold"),
                bg=self.colors["panel"],
                fg=self.colors["muted"],
            ).pack(anchor="w", pady=(0, 5))

            entry = tk.Entry(
                cell,
                font=("Arial", 11),
                bg=self.colors["field"],
                fg=self.colors["text"],
                insertbackground=self.colors["text"],
                relief="flat",
                highlightthickness=1,
                         highlightbackground=self.colors["border"],
                highlightcolor=self.colors["accent"],
            )
            entry.pack(fill="x", ipady=7)
            entry.insert(0, "")
            self.entries[field] = entry

        for col in range(3):
            form.grid_columnconfigure(col, weight=1)

        button_row = tk.Frame(self.root, bg=self.colors["bg"])
        button_row.pack(fill="x", padx=24, pady=(6, 12))

        self.make_button(button_row, "Add Student", self.add_student).pack(side="left", padx=(0, 8))
        self.make_button(button_row, "Update Selected", self.update_student).pack(side="left", padx=8)
        self.make_button(
            button_row, "Delete Selected", self.delete_student, danger=True
        ).pack(side="left", padx=8)
        self.make_button(button_row, "Clear Fields", self.clear_fields).pack(side="left", padx=8)

        search_row = tk.Frame(self.root, bg=self.colors["bg"])
        search_row.pack(fill="x", padx=24, pady=(0, 8))

        tk.Label(
            search_row,
            text="Search by ID or name:",
            font=("Arial", 10, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["text"],
        ).pack(side="left", padx=(0, 10))

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_: self.refresh_table())
        search_entry = tk.Entry(
            search_row,
            textvariable=self.search_var,
            font=("Arial", 11),
            bg=self.colors["field"],
            fg=self.colors["text"],
            insertbackground=self.colors["text"],
            relief="flat",
        )
        search_entry.pack(side="left", fill="x", expand=True, ipady=7)

        table_frame = tk.Frame(self.root, bg=self.colors["panel"])
        table_frame.pack(fill="both", expand=True, padx=24, pady=(0, 12))

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            background=self.colors["panel"],
            foreground=self.colors["text"],
            fieldbackground=self.colors["panel"],
            rowheight=30,
            borderwidth=0,
            font=("Arial", 10),
        )
        style.configure(
            "Treeview.Heading",
            background=self.colors["field"],
            foreground=self.colors["text"],
            font=("Arial", 10, "bold"),
                     relief="flat",
        )
        style.map("Treeview", background=[("selected", self.colors["accent"])])

        self.tree = ttk.Treeview(table_frame, columns=FIELDS, show="headings", selectmode="browse")
        widths = {
            "Student ID": 110,
            "Name": 220,
            "Class": 120,
            "Study Time": 150,
            "Absences": 120,
        }
        for field in FIELDS:
            self.tree.heading(field, text=field)
            self.tree.column(field, width=widths[field], anchor="center")

        y_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        x_scroll = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        self.status_var = tk.StringVar(value="Ready")
        tk.Label(
            self.root,
            textvariable=self.status_var,
            anchor="w",
            font=("Arial", 9),
            bg=self.colors["bg"],
            fg=self.colors["muted"],
        ).pack(fill="x", padx=24, pady=(0, 12))

    def make_button(self, parent, text, command, danger=False):
        return tk.Button(
            parent,
            text=text,
            command=command,
            font=("Arial", 10, "bold"),
            bg=self.colors["danger"] if danger else self.colors["accent"],
            fg="white",
            activebackground=self.colors["accent_hover"],
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=8,
        )

    def load_students(self):
        if not os.path.exists(DATA_FILE):
            self.students = []
            return

        try:
            with open(DATA_FILE, "r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                self.students = [
                    {field: row.get(field, "") for field in FIELDS}
                    for row in reader
                ]
        except (OSError, csv.Error) as error:
            messagebox.showerror("File Error", f"Could not load student records:\n{os.error}")
            self.students = []

    def save_students(self):
        try:
            with open(DATA_FILE, "w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=FIELDS)
                writer.writeheader()
                writer.writerows(self.students)
            return True
        except OSError as error:
            messagebox.showerror("Save Error", f"Could not save student records:\n{error}")
            return False

    def get_form_data(self):
        data = {field: self.entries[field].get().strip() for field in FIELDS}
        if any(not value for value in data.values()):
            messagebox.showwarning("Missing Details", "Please fill in all fields.")
            return None

        try:
            study_time = int(data["Study Time"])
            absences = int(data["Absences"])
        except ValueError:
            messagebox.showwarning("Invalid Input", "Study Time and Absences must be whole numbers.")
            return None

        if study_time not in (1, 2, 3, 4):
            messagebox.showwarning("Invalid Study Time", "Enter a Study Time category from 1 to 4.")
            return None
        if absences < 0:
            messagebox.showwarning("Invalid Absences", "Absences cannot be negative.")
            return None

        data["Study Time"] = str(study_time)
        data["Absences"] = str(absences)
        return data

    def add_student(self):
        data = self.get_form_data()
        if data is None:
            return

        if any(student["Student ID"].casefold() == data["Student ID"].casefold()
               for student in self.students):
            messagebox.showwarning("Duplicate ID", "This Student ID already exists.")
            return

        self.students.append(data)
        if self.save_students():
            self.refresh_table()
            self.clear_fields()
            self.status_var.set(f"Student added. Total records: {len(self.students)}")

    def update_student(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Select Student", "Select a student row to update.")
            return

        data = self.get_form_data()
        if data is None:
           return

        old_id = selected[0]
        if data["Student ID"] != old_id and any(
            student["Student ID"].casefold() == data["Student ID"].casefold()
            for student in self.students
        ):
            messagebox.showwarning("Duplicate ID", "Another student already uses this Student ID.")
            return

        for index, student in enumerate(self.students):
            if student["Student ID"] == old_id:
                self.students[index] = data
                break

        if self.save_students():
            self.refresh_table()
            self.clear_fields()
            self.status_var.set("Student record updated.")

    def delete_student(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Select Student", "Select a student row to delete.")
            return

        student_id = selected[0]
        confirmed = messagebox.askyesno(
            "Confirm Delete",
            f"Delete student record {student_id}?",
        )
        if not confirmed:
            return

        self.students = [student for student in self.students if student["Student ID"] != student_id]
        if self.save_students():
            self.refresh_table()
            self.clear_fields()
            self.status_var.set("Student record deleted.")

    def clear_fields(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.tree.selection_remove(self.tree.selection())
        self.status_var.set("Fields cleared.")

    def on_select(self, _event=None):
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0], "values")
        for field, value in zip(FIELDS, values):
            self.entries[field].delete(0, tk.END)
            self.entries[field].insert(0, value)

    def refresh_table(self):
        if not hasattr(self, "tree"):
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        query = self.search_var.get().strip().casefold() if hasattr(self, "search_var") else ""
        visible_count = 0

        for student in self.students:
            searchable = f'{student["Student ID"]} {student["Name"]}'.casefold()
            if query and query not in searchable:
                continue
            self.tree.insert(
                "",
                "end",
                iid=student["Student ID"],
                values=tuple(student[field] for field in FIELDS),
            )
            visible_count += 1

        if hasattr(self, "status_var"):
            self.status_var.set(f"Showing {visible_count} of {len(self.students)} student records.")

def main():
    root = tk.Tk()
    StudentManagementApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()  

