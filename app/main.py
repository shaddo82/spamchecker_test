from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from app.issue import *
import logging
import traceback
from app.config import MODEL_MODE
from app.spam import check_spam_rules, check_spam_ml_canary
from app.model_loader import get_model_info
from app.retrain_issue import update_issue_state
from app.config import LOW_CONFIDENCE_THRESHOLD

# 1) 로그 포맷: 시간 + 레벨 + 메시지
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | "
        "%(filename)s:%(lineno)d (%(funcName)s) | "
        "%(message)s"
)
logger = logging.getLogger("spamcheck")

app = FastAPI()

class ClassifyRequest(BaseModel):
    text: str

@app.post("/classify")
async def classify(payload: ClassifyRequest):
    text = payload.text
    logger.info(f"CALL /classify | text='{text}' | len={len(text)}")
    try:
        serving_model = "rules"
        if MODEL_MODE == "ml":
            label, score, serving_model = check_spam_ml_canary(text)
            update_issue_state(text, label, score, LOW_CONFIDENCE_THRESHOLD)
            model_info = get_model_info(serving_model)
        else:
            label, score = check_spam_rules(text)
            model_info = {
                "run_id": "rules",
                "model_type": "rules",
                "test_accuracy": None,
            }
        logger.info(
            f"OK /classify | label={label} score={score} "
            f"serving_model={serving_model} model_info={model_info}"
        )
        return {
            "label": label,
            "score": score,
            "serving_model": serving_model,
            "model_info": model_info,
        }
    except Exception as e:
        logger.exception(
            f"FAIL /classify | text='{text}' | error={type(e).__name__}: {e}"
        )
        tb = traceback.format_exc()
        title = f"[Prod Error] /classify failed: {type(e).__name__}"
        body = (
            "## Summary\n"
            "- endpoint: /classify\n"
            f"- input(text, short): `{text}`\n"
            f"- input length: {len(text)}\n\n"
            "## Exception\n"
            f"- type: {type(e).__name__}\n"
            f"- message: {str(e)}\n\n"
            "## Traceback (line info)\n"
            f"```text\n{tb}\n```"
        )
        create_github_issue(title, body, logger)
        return {
            "label": f"Model Load Error: {type(e).__name__}",
            "score": -1,
            "model_info": {
                "run_id": "unknown",
                "model_type": None,
                "test_accuracy": None,
            },
            "error": str(e),
        }



app.mount("/", StaticFiles(directory="static", html=True), name="static")
