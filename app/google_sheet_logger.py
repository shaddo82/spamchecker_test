# app/google_sheet_logger.py
import json
import os
from datetime import datetime

import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

_sheet_client = None
_spreadsheet = None


def get_spreadsheet():
    global _sheet_client, _spreadsheet

    if _spreadsheet is not None:
        return _spreadsheet

    sheet_name = os.getenv("GOOGLE_SHEET_NAME")
    service_account_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")

    if not sheet_name:
        raise RuntimeError("GOOGLE_SHEET_NAME is not set")
    if not service_account_json:
        raise RuntimeError("GOOGLE_SERVICE_ACCOUNT_JSON is not set")

    info = json.loads(service_account_json)
    credentials = Credentials.from_service_account_info(info, scopes=SCOPE)

    _sheet_client = gspread.authorize(credentials)
    _spreadsheet = _sheet_client.open(sheet_name)
    return _spreadsheet


def append_prediction_log(text: str, label: str, score: float, serving_model: str):
    spreadsheet = get_spreadsheet()
    worksheet = spreadsheet.worksheet("prediction_logs")
    worksheet.append_row(
        [
            datetime.now().isoformat(timespec="seconds"),
            text,
            label,
            round(float(score), 4),
            serving_model,
        ]
    )


def append_feedback_log(
    text: str,
    prediction: str,
    correct_label: str,
    score: float,
    serving_model: str,
):
    spreadsheet = get_spreadsheet()
    worksheet = spreadsheet.worksheet("feedback_logs")
    worksheet.append_row(
        [
            datetime.now().isoformat(timespec="seconds"),
            text,
            prediction,
            correct_label,
            round(float(score), 4),
            serving_model,
        ]
    )
