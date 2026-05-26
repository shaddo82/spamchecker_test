import os
import joblib
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score # 성능 지표 저장을 위해
import mlflow.sklearn # mlflow 형태로 저장
from mlflow.tracking import MlflowClient
from ml.model_promoter import promote_if_better

#
BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "data", "spam.csv")
ARTIFACT_DIR = os.path.join(BASE_DIR, "artifacts")
MODEL_PATH = os.path.join(ARTIFACT_DIR, "spam_model.joblib")
os.makedirs(ARTIFACT_DIR, exist_ok=True)
# 실험 세팅
from app.config import *
BASE_DIR = os.path.dirname(__file__)
TRAIN_DATA_PATH = os.path.join(BASE_DIR, DATA_DIR_NAME,TRAIN_FILE_NAME)
TEST_DATA_PATH = os.path.join(BASE_DIR, DATA_DIR_NAME, TEST_FILE_NAME)
ARTIFACT_DIR = os.path.join(BASE_DIR, ARTIFACT_DIR_NAME)
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
mlflow.set_registry_uri(MLFLOW_TRACKING_URI)
mlflow.set_experiment("spam-classification-server")
train_df = pd.read_csv(TRAIN_DATA_PATH)
test_df = pd.read_csv(TEST_DATA_PATH)
X_train = train_df["text"]
y_train = train_df["label"]
X_test = test_df["text"]
y_test = test_df["label"]
models = {
"LogisticRegression": LogisticRegression(max_iter=200),
"NaiveBayes": MultinomialNB(),
"RandomForestClassifier": RandomForestClassifier(n_estimators=100, random_state=42)
}
client = MlflowClient()
best_test_acc = -1.0
best_version = None
# 실험 기록 시작
for model_name, model in models.items():
    with mlflow.start_run():
        # 실험 설정 기록
        pipeline = Pipeline([
            ("vectorizer", CountVectorizer()),
            ("classifier", model)
        ])
        mlflow.log_param("train_data_path", TRAIN_DATA_PATH)
        mlflow.log_param("test_train_data_path", TEST_DATA_PATH)
        mlflow.log_param("train_row_count"
                         , len(train_df))
        mlflow.log_param("test_row_count"
                         , len(test_df))
        mlflow.log_param("model_type", model_name)
        mlflow.log_param("vectorizer", "CountVectorizer")
        pipeline.fit(X_train, y_train)
        # 간단한 metric 저장 (train accuracy)
        train_preds = pipeline.predict(X_train)
        test_preds = pipeline.predict(X_test)
        train_acc = accuracy_score(y_train, train_preds)
        test_acc = accuracy_score(y_test, test_preds)
        mlflow.log_metric("train_accuracy"
                          , train_acc)
        mlflow.log_metric("test_accuracy"
                          , test_acc)
        joblib.dump(pipeline, MODEL_PATH)
        # artifact 기록
        mlflow.log_artifact(TRAIN_DATA_PATH)  # 데이터
        mlflow.log_artifact(TEST_DATA_PATH)  # 데이터
        mlflow.log_artifact(MODEL_PATH)  # 모델 파일
        # MLflow 모델 형식으로도 저장
        try:
            mlflow.sklearn.log_model(
                pipeline,
                artifact_path="model",
                registered_model_name=os.getenv("REGISTERED_MODEL_NAME", "spam-model-new"),
            )
        except Exception:
            mlflow.sklearn.log_model(pipeline, artifact_path="model")
        print(f"Model saved to: {MODEL_PATH}")
        print(f"train_accuracy: {train_acc:.4f}")
        print(f"test_accuracy: {test_acc:.4f}")
        latest_versions = client.search_model_versions("name='spam-model-new'")
        latest_version = max(latest_versions, key=lambda v: int(v.version)).version
        if test_acc > best_test_acc:
            best_test_acc = test_acc
        best_version = latest_version

    if best_version is not None:
        promote_if_better(best_version, best_test_acc)
