import os

MODEL_MODE = os.getenv("MODEL_MODE", "ml")  # "ml" or "rules"
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "https://barn-monoxide-marshland.ngrok-free.dev")
MODEL_URI = os.getenv("MODEL_URI", "models:/spam-model-new@challenger")
# MODEL_URI = "models:/spam-model-new@champion"
CANARY_ENABLED = os.getenv("CANARY_ENABLED", "true").lower() == "true"
CANARY_RATIO = float(os.getenv("CANARY_RATIO", "0.5"))  # 본래는 0.1 권장
CHAMPION_MODEL_URI = os.getenv("CHAMPION_MODEL_URI", "models:/spam-model-new@champion")
CHALLENGER_MODEL_URI = os.getenv("CHALLENGER_MODEL_URI", "models:/spam-model-new@challenger")
MODEL_CACHE_ENABLED = os.getenv("MODEL_CACHE_ENABLED", "false").lower() == "true"
TRAIN_FILE_NAME = os.getenv("TRAIN_FILE_NAME", "train.csv")
TEST_FILE_NAME = os.getenv("TEST_FILE_NAME", "test.csv")
MODEL_NAME = os.getenv("MODEL_NAME", "spam_model.joblib")
ARTIFACT_DIR_NAME = os.getenv("ARTIFACT_DIR_NAME", "artifacts")
DATA_DIR_NAME = os.getenv("DATA_DIR_NAME", "data")
# drift / retrain issue report
LOW_CONFIDENCE_THRESHOLD = 0.65
LOW_CONFIDENCE_LIMIT = 5
