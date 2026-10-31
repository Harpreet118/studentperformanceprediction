
import csv
import os
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HISTORY_FILE = os.path.join(BASE_DIR, "prediction_history.csv")

BG = "#0b1020"
SIDEBAR = "#10172b"
CARD = "#151f36"
TEXT = "#f3f6ff"
MUTED = "#9aa8c7"
PURPLE = "#8b5cf6"
CYAN = "#35d5f2"
GREEN = "#35d39a"
ORANGE = "#ffb86b"
RED = "#ff6b81"


class Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("NEXUS | Student Performance AI")
        self.root.geometry("1150x740")
        self.root.minsize(950, 620)
        self.root.configure(bg=BG)
        self.root.option_add("*Font", ("Segoe UI", 10))

        self.stats = {}
        self.create_ui()
        self.refresh_stats()

    def create_ui(self):
        sidebar = tk.Frame(self.root, bg=SIDEBAR, width=215)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(
            sidebar, text="◈  NEXUS", bg=SIDEBAR, fg=CYAN,
            font=("Segoe UI", 22, "bold")
        ).pack(anchor="w", padx=22, pady=(28, 35))

        tk.Label(
            sidebar, text="WORKSPACE", bg=SIDEBAR, fg="#68799f",
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", padx=22, pady=(0, 10))

        self.side_button(sidebar, "▦   Overview", self.refresh_stats, True)
        self.side_button(
            sidebar, "◈   Predict Performance",
            lambda: self.open_module("main.py")
        )
        self.side_button(
            sidebar, "♙   Student Records",
            lambda: self.open_module("student_management.py")
        )
        self.side_button(
            sidebar, "▥   Analytics",
            lambda: self.open_module("analytics.py")
        )
        self.side_button(
            sidebar, "⌁   Performance Graph",
            lambda: self.open_module("performance_graph.py")
        )
        self.side_button(
            sidebar, "⇩   Export PDF",
            lambda: self.open_module("export_report.py")
        )

        tk.Frame(sidebar, bg=SIDEBAR).pack(fill="both", expand=True)

        tk.Label(
            sidebar, text="● SYSTEM READY", bg=SIDEBAR, fg=GREEN,
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", padx=22, pady=(0, 5))

        tk.Label(
            sidebar, text="Student AI Suite  •  v2.0",
            bg=SIDEBAR, fg=MUTED, font=("Segoe UI", 8)
        ).pack(anchor="w", padx=22, pady=(0, 20))

        content = tk.Frame(self.root, bg=BG)
        content.pack(side="left", fill="both", expand=True)

        header = tk.Frame(content, bg=BG)
        header.pack(fill="x", padx=28, pady=(25, 18))

        tk.Label(
            header, text="STUDENT PERFORMANCE / OVERVIEW",
            bg=BG, fg=CYAN, font=("Segoe UI", 9, "bold")
        ).pack(anchor="w")

        tk.Label(
            header, text="Your learning command center",
            bg=BG, fg=TEXT, font=("Segoe UI", 25, "bold")
        ).pack(anchor="w", pady=(5, 2))

        tk.Label(
            header,
            text="Predict, explore, and track student performance in one place.",
            bg=BG, fg=MUTED, font=("Segoe UI", 10)
        ).pack(anchor="w")

        hero = tk.Frame(
            content, bg="#171d3a",
            highlightbackground="#393366", highlightthickness=1
        )
        hero.pack(fill="x", padx=28, pady=(0, 18))

        hero_left = tk.Frame(hero, bg="#171d3a")
        hero_left.pack(side="left", fill="both", expand=True, padx=22, pady=22)

        tk.Label(
            hero_left, text="✦ AI-POWERED INSIGHTS",
            bg="#171d3a", fg=CYAN, font=("Segoe UI", 9, "bold")
        ).pack(anchor="w")

        tk.Label(
            hero_left, text="Turn student data into\nclearer decisions.",
            bg="#171d3a", fg=TEXT,
            font=("Segoe UI", 21, "bold"), justify="left"
        ).pack(anchor="w", pady=(10, 7))

        tk.Label(
            hero_left,
            text="Estimate performance using study patterns and assessment scores.\nReview predictions and monitor student results.",
            bg="#171d3a", fg="#b7c3e2",
            font=("Segoe UI", 9), justify="left"
        ).pack(anchor="w")

        tk.Button(
            hero_left, text="  Open Prediction Studio  →",
            command=lambda: self.open_module("main.py"),
            bg=PURPLE, fg="white", activebackground="#7045d4",
            activeforeground="white", relief="flat", bd=0,
            padx=14, pady=10, cursor="hand2",
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", pady=(17, 0))

        art = tk.Canvas(
            hero, width=190, height=175,
            bg="#171d3a", highlightthickness=0
        )
        art.pack(side="right", padx=18, pady=8)
        self.draw_ai_art(art)

        tk.Label(
            content, text="PERFORMANCE SNAPSHOT",
            bg=BG, fg="#8292b5", font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", padx=29, pady=(0, 10))

        stat_row = tk.Frame(content, bg=BG)
        stat_row.pack(fill="x", padx=28)

        self.stat_card(
            stat_row, "PREDICTIONS SAVED", "0",
            "Total saved records", PURPLE, 0
        )
        self.stat_card(
            stat_row, "AVERAGE SCORE", "—",
            "Average percentage", CYAN, 1
        )
        self.stat_card(
            stat_row, "TOP SCORE", "—",
            "Highest percentage", GREEN, 2
        )

        tk.Label(
            content, text="QUICK ACCESS",
            bg=BG, fg="#8292b5", font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", padx=29, pady=(20, 10))

        modules = tk.Frame(content, bg=BG)
        modules.pack(fill="both", expand=True, padx=28, pady=(0, 10))

        items = [
            ("01", "Predict Performance", "main.py",
             "Estimate student scores", PURPLE),
            ("02", "Student Management", "student_management.py",
             "Manage student records", CYAN),
            ("03", "Analytics Overview", "analytics.py",
             "Explore saved statistics", GREEN),
            ("04", "Performance Graph", "performance_graph.py",
             "Visualize grade trends", ORANGE),
            ("05", "Export PDF Report", "export_report.py",
             "Generate a report", RED),
        ]

        for i, item in enumerate(items):
            self.module_card(modules, i, *item)

        tk.Label(
            content,
            text="NEXUS  •  STUDENT PERFORMANCE AI     |     Predictions are estimates",
            bg=BG, fg="#7181a3", font=("Segoe UI", 8)
        ).pack(anchor="w", padx=28, pady=(0, 14))

    def side_button(self, parent, text, command, active=False):
        tk.Button(
            parent, text="  " + text, command=command, anchor="w",
            bg="#24244b" if active else SIDEBAR,
            fg=CYAN if active else "#a8b5d2",
            activebackground="#24244b", activeforeground=TEXT,
            relief="flat", bd=0, padx=13, pady=12,
            cursor="hand2", font=("Segoe UI", 9, "bold" if active else "normal")
        ).pack(fill="x", padx=10, pady=3)

    def draw_ai_art(self, canvas):
        points = [
            (25, 35), (70, 22), (120, 40), (165, 23),
            (45, 80), (95, 75), (145, 100), (25, 135),
            (78, 140), (130, 150), (175, 132)
        ]
        edges = [
            (0, 1), (1, 2), (2, 3), (0, 4), (1, 5),
            (2, 5), (2, 6), (4, 5), (4, 7), (5, 6),
            (5, 8), (6, 9), (6, 10), (7, 8), (8, 9), (9, 10)
        ]

        for a, b in edges:
            canvas.create_line(
                *points[a], *points[b], fill="#3a4774", width=1
            )

        for i, (x, y) in enumerate(points):
            r = 5 if i in (2, 5, 8) else 3
            color = CYAN if i in (2, 5, 8) else PURPLE
            canvas.create_oval(
                x-r, y-r, x+r, y+r, fill=color, outline=""
            )

        canvas.create_oval(63, 47, 129, 113, outline="#5144a2", width=2)
        canvas.create_text(
            96, 80, text="AI", fill=TEXT,
            font=("Segoe UI", 20, "bold")
        )

    def stat_card(self, parent, title, value, hint, accent, column):
        card = tk.Frame(
            parent, bg=CARD,
            highlightbackground="#263653", highlightthickness=1
        )
        card.grid(
            row=0, column=column, sticky="nsew",
            padx=(0 if column == 0 else 9, 0)
        )
        parent.grid_columnconfigure(column, weight=1, uniform="stats")

        tk.Frame(card, bg=accent, height=3).pack(fill="x")
        inner = tk.Frame(card, bg=CARD)
        inner.pack(fill="both", expand=True, padx=14, pady=12)

        tk.Label(
            inner, text=title, bg=CARD, fg=MUTED,
            font=("Segoe UI", 8, "bold")
        ).pack(anchor="w")

        number = tk.Label(
            inner, text=value, bg=CARD, fg=TEXT,
            font=("Segoe UI", 22, "bold")
        )
        number.pack(anchor="w", pady=(5, 1))

        tk.Label(
            inner, text=hint, bg=CARD, fg="#7484a6",
            font=("Segoe UI", 8)
        ).pack(anchor="w")

        self.stats[title] = number

    def module_card(self, parent, index, number, title, filename, description, accent):
        card = tk.Frame(
            parent, bg=CARD,
            highlightbackground="#263653", highlightthickness=1
        )
        row, column = divmod(index, 3)
        card.grid(
            row=row, column=column, sticky="nsew",
            padx=(0 if column == 0 else 9, 0), pady=(0, 9)
        )
        parent.grid_columnconfigure(column, weight=1, uniform="modules")
        parent.grid_rowconfigure(row, weight=1, uniform="module_rows")

        tk.Label(
            card, text=number, bg=CARD, fg=accent,
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", padx=12, pady=(10, 3))

        tk.Label(
            card, text=title, bg=CARD, fg=TEXT,
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", padx=12)

        tk.Label(
            card, text=description, bg=CARD, fg=MUTED,
            font=("Segoe UI", 8), wraplength=200, justify="left"
        ).pack(anchor="w", padx=12, pady=(5, 8))

        tk.Button(
            card, text="Open module  →",
            command=lambda f=filename: self.open_module(f),
            bg="#202d49", fg=accent,
            activebackground="#293b5e", activeforeground=TEXT,
            relief="flat", bd=0, padx=9, pady=6,
            cursor="hand2", font=("Segoe UI", 8, "bold")
        ).pack(anchor="w", padx=12, pady=(0, 10))

    def refresh_stats(self):
        try:
            with open(HISTORY_FILE, newline="", encoding="utf-8") as file:
                rows = list(csv.DictReader(file))
        except FileNotFoundError:
            rows = []
        except Exception as error:
            messagebox.showwarning(
                "History file", f"Could not read prediction history:\\n{error}"
            )
            rows = []

        percentages = []
        for row in rows:
            try:
                percentages.append(float(row.get("Percentage", "")))
            except (TypeError, ValueError):
                pass

        average = sum(percentages) / len(percentages) if percentages else None
        highest = max(percentages) if percentages else None

        self.stats["PREDICTIONS SAVED"].config(text=str(len(rows)))
        self.stats["AVERAGE SCORE"].config(
            text=f"{average:.1f}%" if average is not None else "—"
        )
        self.stats["TOP SCORE"].config(
            text=f"{highest:.1f}%" if highest is not None else "—"
        )

    def open_module(self, filename):
        path = os.path.join(BASE_DIR, filename)
        if not os.path.isfile(path):
            messagebox.showerror(
                "Module not found",
                f"Could not find {filename}.\\n\\n"
                "Keep dashboard.py in the same folder as your other project files."
            )
            return

        try:
            subprocess.Popen([sys.executable, path], cwd=BASE_DIR)
        except Exception as error:
            messagebox.showerror("Could not open module", str(error))


if __name__ == "__main__":
    root = tk.Tk()
    Dashboard(root)
    root.mainloop()
