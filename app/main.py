from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from app.spam import check_spam

app = FastAPI()

class ClassifyRequest(BaseModel):
    text: str

@app.post("/classify")
async def classify(payload: ClassifyRequest):
    label, score = check_spam(payload.text)
    return {"label": label, "score": score}

app.mount("/", StaticFiles(directory="static", html=True), name="static")