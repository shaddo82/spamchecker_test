import random

import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient

from app.config import (
    CANARY_ENABLED,
    CANARY_RATIO,
    CHALLENGER_MODEL_URI,
    CHAMPION_MODEL_URI,
    MLFLOW_TRACKING_URI,
    MODEL_CACHE_ENABLED,
)

_champion_model = None
_challenger_model = None


def _load_model_from_uri(model_uri: str):
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    return mlflow.sklearn.load_model(model_uri)


def load_champion_model():
    global _champion_model
    if MODEL_CACHE_ENABLED and _champion_model is not None:
        return _champion_model

    model = _load_model_from_uri(CHAMPION_MODEL_URI)
    if MODEL_CACHE_ENABLED:
        _champion_model = model
    return model


def load_challenger_model():
    global _challenger_model
    if MODEL_CACHE_ENABLED and _challenger_model is not None:
        return _challenger_model

    model = _load_model_from_uri(CHALLENGER_MODEL_URI)
    if MODEL_CACHE_ENABLED:
        _challenger_model = model
    return model


def select_serving_model():
    if CANARY_ENABLED and random.random() < CANARY_RATIO:
        return load_challenger_model(), "challenger"
    return load_champion_model(), "champion"


def get_model_info(serving_model: str):
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    try:
        model_uri = CHAMPION_MODEL_URI if serving_model == "champion" else CHALLENGER_MODEL_URI
        info = mlflow.models.get_model_info(model_uri)
        run = MlflowClient().get_run(info.run_id)
        return {
            "run_id": info.run_id,
            "model_type": run.data.params.get("model_type"),
            "test_accuracy": run.data.metrics.get("test_accuracy"),
        }
    except Exception:
        return {
            "run_id": "unknown",
            "model_type": None,
            "test_accuracy": None,
        }
