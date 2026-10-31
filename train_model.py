
import os
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# Dataset location
DATA_PATH = "data/student-mat.csv"
MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "student_model.pkl")

# Load dataset: this CSV uses semicolons
data = pd.read_csv(DATA_PATH, sep=";")

# Features available in the actual dataset
features = ["studytime", "absences", "G1", "G2"]
target = "G3"

# Ensure the required columns contain numeric values
for column in features + [target]:
    data[column] = pd.to_numeric(data[column], errors="coerce")

data = data.dropna(subset=features + [target])

X = data[features]
y = data[target]

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

# Train the regression model
model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)

# Evaluate on unseen test records
predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

# Save model and its feature names
os.makedirs(MODEL_DIR, exist_ok=True)

joblib.dump(
    {
        "model": model,
        "features": features
    },
    MODEL_PATH
)

print("Model training completed!")
print(f"Dataset records used: {len(data)}")
print(f"Training records: {len(X_train)}")
print(f"Testing records: {len(X_test)}")
print(f"Mean Absolute Error: {mae:.2f} grade points")
print(f"Approximate MAE as percentage: {mae / 20 * 100:.2f}%")
print(f"R² score: {r2:.3f}")
print(f"Saved model to: {MODEL_PATH}")
