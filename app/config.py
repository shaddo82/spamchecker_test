import os

MODEL_MODE = os.getenv("MODEL_MODE", "ml")  # "ml" or "rules"
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "https://barn-monoxide-marshland.ngrok-free.dev")
MODEL_URI = os.getenv("MODEL_URI", "models:/spam-model@challenger")
TRAIN_FILE_NAME = os.getenv("TRAIN_FILE_NAME", "train.csv")
TEST_FILE_NAME = os.getenv("TEST_FILE_NAME", "test.csv")
MODEL_NAME = os.getenv("MODEL_NAME", "spam_model.joblib")
ARTIFACT_DIR_NAME = os.getenv("ARTIFACT_DIR_NAME", "artifacts")
DATA_DIR_NAME = os.getenv("DATA_DIR_NAME", "data")
