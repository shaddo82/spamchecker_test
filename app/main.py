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
    # (A) 요청 들어온 것 자체를 기록: 언제(로그시간) / 무엇(endpoint) / 어떤 입력
    logger.info(f"CALL /classify | text='{text}' | len={len(text)}")
    try:
        if text =="crash":
            raise RuntimeError("의도적 장애 추가")
        label, score = check_spam(text)
        # (B) 정상 처리 결과도 짧게 기록
        logger.info(f"OK /classify | label={label} score={score}")
    except Exception as e:
        # (C) 디버깅 핵심: 에러 종류/메시지 + 스택트레이스(파일/라인 포함)
        # logger.exception은 현재 예외의 traceback을 자동으로 찍어줍니다.
        logger.exception(
            f"FAIL /classify | text='{text}' | error={type(e).__name__}: {e}"
        )

        # (D) GitHub Issue 자동 생성
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

        # (D) 사용자 응답은 심플하게
        return {"label": "Internal Server Error", "score": -1}


app.mount("/", StaticFiles(directory="static", html=True), name="static")