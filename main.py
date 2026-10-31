
import tkinter as tk
from tkinter import messagebox
import joblib
import pandas as pd
import os

# Load the trained ML model
MODEL_PATH = "models/student_model.pkl"
HISTORY_FILE = "prediction_history.csv"

saved_data = joblib.load(MODEL_PATH)
model = saved_data["model"]
features = saved_data["features"]

# CSV history columns
history_columns = [
    "Study Time",
    "Absences",
    "MST1",
    "MST2",
    "Grade",
    "Percentage",
    "Category"
]

# Load existing prediction history
if os.path.exists(HISTORY_FILE):
    try:
        prediction_history = pd.read_csv(
            HISTORY_FILE
        ).to_dict("records")
    except (OSError, pd.errors.EmptyDataError):
        prediction_history = []
else:
    prediction_history = []

# Main application window
root = tk.Tk()
root.title("Student Performance Prediction System")
root.geometry("850x720")
root.configure(bg="#0B1120")

# Heading
tk.Label(
    root,
    text="Student Performance AI",
    font=("Arial", 24, "bold"),
    bg="#0B1120",
    fg="#C4B5FD"
).pack(pady=(20, 5))

tk.Label(
    root,
    text="ML-Powered Academic Performance Analyzer",
    font=("Arial", 12),
    bg="#0B1120",
    fg="#CBD5E1"
).pack(pady=(0, 20))

# Input section
form = tk.Frame(root, bg="#1E293B", padx=25, pady=15)
form.pack(padx=40, fill="x")

fields = [
    ("Study Time Category (1-4)", "studytime"),
    ("School Absences (0 or more)", "absences"),
    ("MST1 Marks (0-20)", "G1"),
    ("MST2 Marks (0-20)", "G2"),
]

entries = {}

for label_text, key in fields:
    row = tk.Frame(form, bg="#1E293B")
    row.pack(fill="x", pady=8)

    tk.Label(
        row,
        text=label_text,
        font=("Arial", 11),
        bg="#1E293B",
        fg="white",
        width=30,
        anchor="w"
    ).pack(side="left")

    entry = tk.Entry(
        row,
        font=("Arial", 12),
        bg="#334155",
        fg="white",
        insertbackground="white",
        relief="flat"
    )
    entry.pack(side="left", fill="x", expand=True, ipady=6)
    entries[key] = entry


# Predict student performance
def predict_performance():
    try:
        studytime = int(entries["studytime"].get())
        absences = int(entries["absences"].get())
        g1 = float(entries["G1"].get())
        g2 = float(entries["G2"].get())

        if studytime not in (1, 2, 3, 4):
            raise ValueError(
                "Study time category must be 1, 2, 3, or 4."
            )

        if absences < 0:
            raise ValueError("Absences cannot be negative.")

        if not (0 <= g1 <= 20 and 0 <= g2 <= 20):
            raise ValueError(
                "MST1 and MST2 marks must be between 0 and 20."
            )

        # Prepare input for the trained model
        input_data = pd.DataFrame(
            [[studytime, absences, g1, g2]],
            columns=features
        )

        # Predict final grade
        predicted_grade = float(model.predict(input_data)[0])
        predicted_grade = max(0, min(20, predicted_grade))
        percentage = predicted_grade / 20 * 100

        # Performance category
        if percentage >= 80:
            category = "Excellent"
        elif percentage >= 60:
            category = "Good"
        elif percentage >= 40:
            category = "Average"
        else:
            category = "Needs Improvement"

        # Prepare prediction record
        record = {
            "Study Time": studytime,
            "Absences": absences,
            "MST1": g1,
            "MST2": g2,
            "Grade": round(predicted_grade, 1),
            "Percentage": round(percentage, 1),
            "Category": category
        }

        # Save to CSV before updating the in-memory history
        history_df = pd.DataFrame(
            [record],
            columns=history_columns
        )

        file_exists = (
            os.path.exists(HISTORY_FILE)
            and os.path.getsize(HISTORY_FILE) > 0
        )

        history_df.to_csv(
            HISTORY_FILE,
            mode="a",
            header=not file_exists,
            index=False
        )

        prediction_history.append(record)

        # Display result
        result_label.config(
            text=(
                f"Predicted Final Grade: {predicted_grade:.1f} / 20\n"
                f"Predicted Final Marks: {percentage:.1f}%\n"
                f"Performance: {category}"
            ),
            fg="#A5B4FC"
        )

    except (ValueError, TypeError) as error:
        messagebox.showerror(
            "Invalid Input",
            f"Please check your entries.\n{error}"
        )
    except OSError as error:
        messagebox.showerror(
            "File Error",
            f"Could not save prediction history.\n{error}"
        )


# Clear all inputs and result
def clear_fields():
    for entry in entries.values():
        entry.delete(0, tk.END)

    result_label.config(
        text="Your prediction will appear here.",
        fg="#A5B4FC"
    )
    entries["studytime"].focus_set()


# Show prediction history
def show_history():
    history_window = tk.Toplevel(root)
    history_window.title("Prediction History")
    history_window.geometry("760x450")
    history_window.configure(bg="#0B1120")

    tk.Label(
        history_window,
        text="Prediction History",
        font=("Arial", 20, "bold"),
        bg="#0B1120",
        fg="#C4B5FD"
    ).pack(pady=15)

    if not prediction_history:
        tk.Label(
            history_window,
            text="No predictions yet. Make a prediction first.",
            font=("Arial", 12),
            bg="#0B1120",
            fg="white"
        ).pack(pady=25)
        return

    text_box = tk.Text(
        history_window,
        font=("Arial", 10),
        bg="#1E293B",
        fg="white",
        insertbackground="white",
        wrap="word",
        width=85,
        height=17,
        relief="flat"
    )
    text_box.pack(
        padx=15,
        pady=10,
        fill="both",
        expand=True
    )

    for number, record in enumerate(prediction_history, start=1):
        text_box.insert(
            tk.END,
            f"Prediction {number}\n"
            f"Study Time: {record['Study Time']} | "
            f"Absences: {record['Absences']}\n"
            f"MST1: {record['MST1']} | MST2: {record['MST2']}\n"
            f"Predicted Grade: {record['Grade']}/20 | "
            f"Marks: {record['Percentage']}%\n"
            f"Category: {record['Category']}\n"
            f"{'-' * 55}\n"
        )

    text_box.config(state="disabled")


# Buttons section
button_frame = tk.Frame(root, bg="#0B1120")
button_frame.pack(pady=18)

tk.Button(
    button_frame,
    text="Predict Performance",
    command=predict_performance,
    font=("Arial", 11, "bold"),
    bg="#7C3AED",
    fg="white",
    activebackground="#6D28D9",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    padx=15,
    pady=10
).pack(side="left", padx=5)

tk.Button(
    button_frame,
    text="Clear Fields",
    command=clear_fields,
    font=("Arial", 11, "bold"),
    bg="#334155",
    fg="white",
    activebackground="#475569",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    padx=15,
    pady=10
).pack(side="left", padx=5)

tk.Button(
    button_frame,
    text="View History",
    command=show_history,
    font=("Arial", 11, "bold"),
    bg="#0F766E",
    fg="white",
    activebackground="#115E59",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    padx=15,
    pady=10
).pack(side="left", padx=5)

# Prediction result
result_label = tk.Label(
    root,
    text="Your prediction will appear here.",
    font=("Arial", 13, "bold"),
    bg="#0B1120",
    fg="#A5B4FC",
    justify="center"
)
result_label.pack(pady=10)

# Footer note
tk.Label(
    root,
    text=(
        "Educational estimate based on the Student Performance dataset. "
        "Predictions are not guaranteed results."
    ),
    font=("Arial", 9),
    bg="#0B1120",
    fg="#94A3B8",
    wraplength=750
).pack(pady=8)

root.mainloop()
