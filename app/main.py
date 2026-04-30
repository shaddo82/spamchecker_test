from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from app.spam import check_spam
from app.issue import *
import logging
import traceback

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
        if text == "crash":
            raise RuntimeError("의도적 장애 추가")
        label, score = check_spam(text)
        logger.info(f"OK /classify | label={label} score={score}")
        return {"label": label, "score": score}   # <- 이 줄 추가
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
        return {"label": "Internal Server Error", "score": -1}



app.mount("/", StaticFiles(directory="static", html=True), name="static")