import mlflow
import mlflow.sklearn
import joblib
from mlflow.tracking import MlflowClient

from app.config import MODEL_URI, MLFLOW_TRACKING_URI

_model = None
_model_info = None

def _parse_model_alias_uri(uri: str):
    if not uri.startswith("models:/") or "@" not in uri:
        return None, None
    target = uri[len("models:/"):]
    model_name, alias = target.split("@", 1)
    return model_name, alias


def load_model():
    global _model

    if _model is None:
        mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
        if MODEL_URI.startswith("models:/") or MODEL_URI.startswith("runs:/"):
            model_name, alias = _parse_model_alias_uri(MODEL_URI)
            if model_name and alias:
                try:
                    MlflowClient().get_model_version_by_alias(model_name, alias)
                except Exception as e:
                    raise RuntimeError(
                        f"MLflow alias lookup failed for {MODEL_URI} "
                        f"(tracking_uri={MLFLOW_TRACKING_URI}): {e}"
                    ) from e
            _model = mlflow.sklearn.load_model(MODEL_URI)
        else:
            _model = joblib.load(MODEL_URI)

    return _model


def get_model_info():
    global _model_info

    if _model_info is None:
        mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

        try:
            info = mlflow.models.get_model_info(MODEL_URI)
            run = MlflowClient().get_run(info.run_id)

            _model_info = {
                "run_id": info.run_id,
                "model_type": run.data.params.get("model_type"),
                "test_accuracy": run.data.metrics.get("test_accuracy"),
            }

        except Exception:
            _model_info = {
                "run_id": "unknown",
                "model_type": None,
                "test_accuracy": None,
            }

    return _model_info
