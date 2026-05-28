# app/feedback.py
import csv
from datetime import datetime
from pathlib import Path

FEEDBACK_PATH = Path("logs/feedback.csv")
FEEDBACK_PATH.parent.mkdir(exist_ok=True)


def save_feedback(
    text: str,
    prediction: str,
    correct_label: str,
    score: float,
    serving_model: str,
):
    is_new = not FEEDBACK_PATH.exists()
    with open(FEEDBACK_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if is_new:
            writer.writerow(
                [
                    "time",
                    "text",
                    "prediction",
                    "correct_label",
                    "score",
                    "serving_model",
                ]
            )
        writer.writerow(
            [
                datetime.now().isoformat(timespec="seconds"),
                text,
                prediction,
                correct_label,
                round(float(score), 4),
                serving_model,
            ]
        )
