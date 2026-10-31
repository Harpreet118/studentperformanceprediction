
import tkinter as tk
from tkinter import messagebox
import csv
import os
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HISTORY_FILE = os.path.join(BASE_DIR, "prediction_history.csv")


def show_graph():
    if not os.path.exists(HISTORY_FILE):
        messagebox.showinfo(
            "No Data",
            "Pehle main.py mein kuch predictions save karo."
        )
        return

    grades = []

    try:
        with open(HISTORY_FILE, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                try:
                    grades.append(float(row["Grade"]))
                except (KeyError, TypeError, ValueError):
                    continue

    except (OSError, csv.Error) as error:
        messagebox.showerror("File Error", str(error))
        return

    if not grades:
        messagebox.showinfo(
            "No Data",
            "CSV file mein valid prediction grades nahi hain."
        )
        return

    numbers = list(range(1, len(grades) + 1))

    plt.figure(figsize=(9, 5))
    plt.plot(numbers, grades, marker="o", label="Predicted Grade")
    plt.axhline(10, linestyle="--", label="Midpoint (10/20)")
    plt.ylim(0, 20)
    plt.xticks(numbers)
    plt.xlabel("Prediction Number")
    plt.ylabel("Predicted Grade (out of 20)")
    plt.title("Student Performance Prediction History")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()


root = tk.Tk()
root.title("Student Performance AI - Graph")
root.geometry("500x260")
root.configure(bg="#101827")

tk.Label(
    root,
    text="Performance Graph",
    font=("Arial", 22, "bold"),
    bg="#101827",
    fg="white"
).pack(pady=(35, 10))

tk.Label(
    root,
    text="Visualize saved prediction grades",
    font=("Arial", 11),
    bg="#101827",
    fg="#aab6c5"
).pack(pady=5)

tk.Button(
    root,
    text="Show Performance Graph",
    command=show_graph,
    font=("Arial", 12, "bold"),
    bg="#8b5cf6",
    fg="white",
    activebackground="#7c3aed",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    padx=18,
    pady=10
).pack(pady=22)

root.mainloop()
