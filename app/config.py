import os

MODEL_MODE = "ml" # "rules"
# LOCAL_MODEL_PATH = "ml/artifacts/spam_model.joblib"
MLFLOW_TRACKING_URI = "sqlite:///mlflow.db"
# MODEL_URI = "runs:/ff834da846d94fdc858c14d00aa89064/model"
# MODEL_URI = "models:/spam-model/1"
MODEL_URI = "models:/spam-model@champion"
