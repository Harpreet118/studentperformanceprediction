import csv
import os
import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HISTORY_FILE = os.path.join(BASE_DIR, "prediction_history.csv")


def read_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def create_pdf():
    try:
        rows = read_history()
    except (OSError, csv.Error) as error:
        messagebox.showerror("Read Error", f"Could not read prediction history:\n{error}")
        return

    valid_rows = []
    grades = []
    for row in rows:
        try:
            grade = float(row["Grade"])
            percentage = float(row["Percentage"])
            category = row.get("Category", "N/A")
            valid_rows.append((row, grade, percentage, category))
            grades.append(grade)
        except (KeyError, TypeError, ValueError):
            continue

    if not valid_rows:
        messagebox.showinfo(
            "No History",
            "No valid prediction history found. Make predictions in main.py first."
        )
        return

    default_name = f"student_performance_report_{datetime.now():%Y%m%d_%H%M%S}.pdf"
    output_path = filedialog.asksaveasfilename(
        title="Save Performance Report",
        defaultextension=".pdf",
        initialfile=default_name,
        filetypes=[("PDF files", "*.pdf")]
    )
    if not output_path:
        return

    try:
        doc = SimpleDocTemplate(
            output_path, pagesize=landscape(A4),
            rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30
        )
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            "ReportTitle", parent=styles["Title"],
            alignment=TA_CENTER, textColor=colors.HexColor("#5B21B6"),
            spaceAfter=8
        )

        story = [
            Paragraph("Student Performance AI", title_style),
            Paragraph("Prediction History Report", styles["Heading2"]),
            Spacer(1, 8),
            Paragraph(f"Generated on: {datetime.now():%d %B %Y, %I:%M %p}", styles["Normal"]),
            Spacer(1, 12),
            Paragraph(f"Total valid predictions: {len(grades)}", styles["Normal"]),
            Paragraph(f"Average predicted grade: {sum(grades) / len(grades):.2f}/20", styles["Normal"]),
            Paragraph(f"Best predicted grade: {max(grades):.2f}/20", styles["Normal"]),
            Spacer(1, 16),
        ]

        table_data = [[
            "Study Time", "Absences", "MST1", "MST2",
            "Grade (/20)", "Percentage", "Category"
        ]]
        for row, grade, percentage, category in valid_rows:
            table_data.append([
                row.get("Study Time", "N/A"),
                row.get("Absences", "N/A"),
                row.get("MST1", "N/A"),
                row.get("MST2", "N/A"),
                f"{grade:.2f}", f"{percentage:.1f}%", str(category)
            ])

        table = Table(
            table_data, repeatRows=1,
            colWidths=[75, 65, 55, 55, 80, 80, 100]
        )
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#5B21B6")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1),
             [colors.white, colors.HexColor("#F3F4F6")]),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ]))
        story.extend([
            table, Spacer(1, 12),
            Paragraph(
                "Note: Grades are model estimates for educational use and are not guaranteed results.",
                styles["Italic"]
            )
        ])
        doc.build(story)
        messagebox.showinfo("Report Created", f"PDF report saved successfully:\n{output_path}")
    except (OSError, ValueError) as error:
        messagebox.showerror("PDF Error", f"Could not create PDF report:\n{error}")


def main():
    root = tk.Tk()
    root.title("Student Performance AI - PDF Report")
    root.geometry("520x300")
    root.configure(bg="#101827")
    root.resizable(False, False)

    tk.Label(
        root, text="Export Performance Report",
        font=("Arial", 21, "bold"), bg="#101827", fg="white"
    ).pack(pady=(35, 10))
    tk.Label(
        root, text="Create a PDF from your saved prediction history.",
        font=("Arial", 10), bg="#101827", fg="#aab6c5"
    ).pack(pady=5)
    tk.Button(
        root, text="Export PDF Report", command=create_pdf,
        font=("Arial", 12, "bold"), bg="#8b5cf6", fg="white",
        activebackground="#7c3aed", activeforeground="white",
        relief="flat", cursor="hand2", padx=20, pady=11
    ).pack(pady=25)
    root.mainloop()


if __name__ == "__main__":
    main()