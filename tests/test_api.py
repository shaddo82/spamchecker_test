from fastapi.testclient import TestClient
import app.main as main_module

client = TestClient(main_module.app)

def test_classify_api_contract():
    main_module.MODEL_MODE = "rules"
    r = client.post("/classify", json={"text": "hello"})
    assert r.status_code == 200
    data = r.json()
    assert "label" in data and "score" in data
    assert "model_info" in data
    assert "model_type" in data["model_info"]
