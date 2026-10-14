"""Recreates employee_productivity_model.pkl exactly as in your notebook.
Run this ONLY if you don't have your own .pkl:   python train_model.py
It trains inside your current venv, so the scikit-learn version always matches.
"""
import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("06_employee_productivity_digital_twin.csv")
X = df.drop(columns=["Employee_ID", "Productivity_Level"])
y = df["Productivity_Level"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

model = Pipeline([
    ("scaler", StandardScaler()),
    ("classifier", LogisticRegression(class_weight="balanced", max_iter=2000, random_state=42)),
])
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print(f"Test accuracy: {accuracy_score(y_test, y_pred):.4f}")
print(classification_report(y_test, y_pred, labels=["High", "Moderate", "Low"], zero_division=0))

joblib.dump(model, "employee_productivity_model.pkl")
print("Saved employee_productivity_model.pkl")
