from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_classify_api_contract():
    r = client.post("/classify", json={"text": "hello"})
    print(r.json())
    assert r.status_code == 200
    data = r.json()
    assert "label" in data and "score" in data