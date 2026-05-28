# app/prediction_logger.py
import csv
from datetime import datetime
from pathlib import Path

PREDICTION_LOG_PATH = Path("logs/predictions.csv")
PREDICTION_LOG_PATH.parent.mkdir(exist_ok=True)


def save_prediction_log(text: str, label: str, score: float, serving_model: str):
    is_new = not PREDICTION_LOG_PATH.exists()
    with open(PREDICTION_LOG_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if is_new:
            writer.writerow(
                [
                    "time",
                    "text",
                    "label",
                    "score",
                    "serving_model",
                ]
            )
        writer.writerow(
            [
                datetime.now().isoformat(timespec="seconds"),
                text,
                label,
                round(float(score), 4),
                serving_model,
            ]
        )
