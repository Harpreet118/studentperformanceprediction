# 🎓 Student Performance Prediction System

A Python-based Machine Learning application that predicts students' academic performance using their study habits, attendance, and internal examination marks.

The project provides an interactive graphical user interface (GUI) to help analyze student performance and identify areas where academic improvement is needed.

## 🚀 Features

- **Student Performance Prediction:** Predicts students' final marks using Machine Learning.
- **Student Management:** Manage student information.
- **Machine Learning Model:** Uses Random Forest Regression.
- **Analytics Dashboard:** Analyze student performance.
- **Performance Graphs:** Visualize academic performance using graphs.
- **PDF Report Export:** Generate and export student performance reports.
- **Interactive GUI:** User-friendly interface developed using Tkinter.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Tkinter | Graphical User Interface |
| Pandas | Data processing |
| NumPy | Numerical operations |
| Scikit-learn | Machine Learning |
| Matplotlib | Data visualization |
| ReportLab | PDF report generation |
| Joblib | Model serialization |

## 🤖 Machine Learning Model

The system uses **Random Forest Regression** to predict students' final academic marks.

### Input Features

- Study Time
- School Absences
- MST 1 Marks
- MST 2 Marks

### Output

- Predicted Final Marks
- Predicted Percentage
- Performance Category

### Performance Categories

- Excellent: 80% and above
- Good: 60%–79%
- Average: 40%–59%
- Needs Improvement: Below 40%

## 📂 Project Structure

```text
Student-Performance-Prediction-System/
│
├── main.py
├── dashboard.py
├── train_model.py
│
├── student_management.py
├── analytics.py
├── performance_graph.py
├── export_report.py
│
├── data/
│   └── student-mat.csv
│
├── models/
│   └── student_model.pkl
│
├── .gitignore
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/Student-Performance-Prediction-System.git
```

### 2. Open Project Folder

```bash
cd Student-Performance-Prediction-System
```

### 3. Create Virtual Environment

```bash
python -m venv .venv
```

### 4. Activate Virtual Environment

Linux / Kali Linux:

```bash
source .venv/bin/activate
```

### 5. Install Required Libraries

```bash
pip install pandas numpy scikit-learn matplotlib reportlab joblib
```

On Kali Linux, if Tkinter is missing:

```bash
sudo apt install python3-tk
```

### 6. Run the Application

Open the project in VS Code and run the appropriate application entry file:

```bash
python dashboard.py
```

## 📊 Project Objective

The main objective of this project is to use Machine Learning techniques to predict students' academic performance based on their previous academic information and study habits.

It helps in understanding student performance, identifying academic weaknesses, and supporting better educational planning.

## 🎯 Future Scope

- Integration of advanced Machine Learning algorithms.
- Student performance comparison.
- Attendance tracking system.
- AI-based personalized study recommendations.
- Online student performance dashboard.

## 👩‍💻 Developed By

**Harpreet Kaur**

Master of Computer Applications (MCA)

Chandigarh University

## 📜 License

This project is developed for educational and academic purposes.
