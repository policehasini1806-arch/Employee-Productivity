"""Loads the trained Logistic Regression model and the dataset, and predicts.

Handles the common ways the model may have been saved:
  * a bare sklearn model                      -> features come from feature_names_in_
  * a sklearn Pipeline (scaler + model)       -> preprocessing is automatic
  * a dict {"model", "scaler", "features", "label_encoder"}
"""
import pickle
from functools import lru_cache

import pandas as pd
from django.conf import settings

TARGET = "Productivity_Level"
LEVEL_ORDER = ["High", "Moderate", "Low"]

# (field name, label, step)
FIELDS = [
    ("Age", "Age", 1),
    ("Experience_Years", "Experience (years)", 1),
    ("Attendance", "Attendance (%)", 0.1),
    ("Working_Hours", "Working hours / week", 0.5),
    ("Tasks_Completed", "Tasks completed", 1),
    ("Task_Delay_Count", "Task delay count", 1),
    ("Training_Hours", "Training hours", 0.5),
    ("Meeting_Hours", "Meeting hours", 0.5),
    ("Project_Count", "Project count", 1),
    ("Performance_Score", "Performance score", 0.1),
    ("Job_Satisfaction", "Job satisfaction", 0.1),
]
FEATURES = [f[0] for f in FIELDS]


@lru_cache(maxsize=1)
def _bundle():
    try:
        import joblib
        obj = joblib.load(settings.MODEL_PATH)
    except Exception:
        with open(settings.MODEL_PATH, "rb") as fh:
            obj = pickle.load(fh)

    scaler = encoder = features = None
    if isinstance(obj, dict):
        model = obj.get("model") or obj.get("pipeline") or obj.get("clf")
        scaler = obj.get("scaler")
        encoder = obj.get("label_encoder") or obj.get("encoder")
        features = obj.get("features") or obj.get("feature_names")
    else:
        model = obj

    if features is None:
        names = getattr(model, "feature_names_in_", None)
        features = list(names) if names is not None else list(FEATURES)
    return model, scaler, encoder, list(features)


@lru_cache(maxsize=1)
def dataset():
    return pd.read_csv(settings.DATASET_PATH)


def predict(values):
    """values: dict of feature -> number. Returns level + class probabilities."""
    model, scaler, encoder, features = _bundle()
    row = {}
    for name in features:
        row[name] = float(values.get(name, 0) or 0)  # e.g. Employee_ID -> 0
    X = pd.DataFrame([row], columns=features)
    if scaler is not None:
        X = scaler.transform(X)

    probs = model.predict_proba(X)[0]
    classes = encoder.classes_ if encoder is not None else model.classes_
    probabilities = {str(c): round(float(p), 4) for c, p in zip(classes, probs)}
    level = max(probabilities, key=probabilities.get)
    ordered = {k: probabilities[k] for k in LEVEL_ORDER if k in probabilities}
    for k, v in probabilities.items():
        ordered.setdefault(k, v)
    return {"level": level, "probabilities": ordered}


def summary():
    df = dataset()
    counts = df[TARGET].value_counts().to_dict()
    total = int(len(df))
    metrics = ["Tasks_Completed", "Training_Hours", "Meeting_Hours",
               "Task_Delay_Count", "Job_Satisfaction", "Performance_Score"]
    by_level = (
        df.groupby(TARGET)[metrics].mean().round(2).to_dict("index")
    )
    ranges = {
        f: {"min": float(df[f].min()), "max": float(df[f].max())}
        for f in FEATURES if f in df.columns
    }
    return {
        "total": total,
        "counts": {k: int(counts.get(k, 0)) for k in LEVEL_ORDER},
        "avg_tasks": round(float(df["Tasks_Completed"].mean()), 1),
        "avg_satisfaction": round(float(df["Job_Satisfaction"].mean()), 2),
        "avg_attendance": round(float(df["Attendance"].mean()), 1),
        "metrics": metrics,
        "by_level": by_level,
        "ranges": ranges,
    }


def employees():
    df = dataset()
    cols = [c for c in ["Employee_ID"] + FEATURES + [TARGET] if c in df.columns]
    return df[cols].to_dict("records")


def medians():
    df = dataset()
    return {f: round(float(df[f].median()), 1) for f in FEATURES}
