
import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
from statistics import mean

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HISTORY_FILE = os.path.join(BASE_DIR, "prediction_history.csv")


class AnalyticsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Performance AI - Analytics")
        self.root.geometry("850x600")
        self.root.configure(bg="#101827")

        self.bg = "#101827"
        self.panel = "#1b2638"
        self.text = "#f3f4f6"
        self.muted = "#aab6c5"
        self.accent = "#8b5cf6"

        tk.Label(
            root,
            text="Performance Analytics",
            font=("Arial", 24, "bold"),
            bg=self.bg,
            fg=self.text
        ).pack(anchor="w", padx=25, pady=(22, 4))

        tk.Label(
            root,
            text="Summary of saved performance predictions",
            font=("Arial", 11),
            bg=self.bg,
            fg=self.muted
        ).pack(anchor="w", padx=25, pady=(0, 20))

        cards = tk.Frame(root, bg=self.bg)
        cards.pack(fill="x", padx=20)

        self.total_var = tk.StringVar(value="0")
        self.average_var = tk.StringVar(value="N/A")
        self.best_var = tk.StringVar(value="N/A")

        self.create_card(cards, "Total Predictions", self.total_var, 0)
        self.create_card(cards, "Average Grade", self.average_var, 1)
        self.create_card(cards, "Best Grade", self.best_var, 2)

        self.table = ttk.Treeview(
            root,
            columns=("Grade", "Percentage", "Category"),
            show="headings",
            height=12
        )

        for column in ("Grade", "Percentage", "Category"):
            self.table.heading(column, text=column)
            self.table.column(column, anchor="center", width=200)

        self.table.pack(fill="both", expand=True, padx=25, pady=20)

        tk.Button(
            root,
            text="Refresh Analytics",
            command=self.load_analytics,
            bg=self.accent,
            fg="white",
            activebackground="#7c3aed",
            activeforeground="white",
            font=("Arial", 11, "bold"),
            relief="flat",
            cursor="hand2",
            padx=16,
            pady=9
        ).pack(pady=(0, 20))

        self.load_analytics()

    def create_card(self, parent, title, variable, column):
        card = tk.Frame(parent, bg=self.panel, padx=20, pady=18)
        card.grid(row=0, column=column, sticky="ew", padx=5)
        parent.grid_columnconfigure(column, weight=1)

        tk.Label(
            card, text=title, bg=self.panel, fg=self.muted,
            font=("Arial", 10)
        ).pack(anchor="w")

        tk.Label(
            card, textvariable=variable, bg=self.panel, fg=self.text,
            font=("Arial", 21, "bold")
        ).pack(anchor="w", pady=(8, 0))

    def load_analytics(self):
        for item in self.table.get_children():
            self.table.delete(item)

        if not os.path.exists(HISTORY_FILE):
            self.total_var.set("0")
            self.average_var.set("N/A")
            self.best_var.set("N/A")
            return

        try:
            with open(HISTORY_FILE, "r", newline="", encoding="utf-8") as file:
                rows = list(csv.DictReader(file))
        except (OSError, csv.Error) as error:
            messagebox.showerror("File Error", str(error))
            return

        grades = []

        for row in rows:
            try:
                grade = float(row["Grade"])
                percentage = float(row["Percentage"])
                category = row.get("Category", "N/A")
            except (KeyError, TypeError, ValueError):
                continue

            grades.append(grade)
            self.table.insert(
                "",
                "end",
                values=(f"{grade:.2f}/20", f"{percentage:.1f}%", category)
            )

        self.total_var.set(str(len(grades)))

        if grades:
            self.average_var.set(f"{mean(grades):.2f}/20")
            self.best_var.set(f"{max(grades):.2f}/20")
        else:
            self.average_var.set("N/A")
            self.best_var.set("N/A")


def main():
    root = tk.Tk()
    AnalyticsApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
