from fastapi import FastAPI
from pydantic import BaseModel
from app.spam import check_spam

app = FastAPI()

class ClassifyRequest(BaseModel):
    text: str

@app.post("/classify")
async def classify(payload: ClassifyRequest):
    text = payload.text
    label, score = check_spam(text)
    return {
        "label": label,
        "score": score
    }