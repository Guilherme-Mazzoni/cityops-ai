import os
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, precision_score, recall_score, roc_auc_score
import mlflow
import mlflow.sklearn

def train_baseline():
    data_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed")
    
    try:
        X = pd.read_csv(os.path.join(data_dir, "X.csv"))
        y = pd.read_csv(os.path.join(data_dir, "y.csv"))['is_sla_violated']
    except FileNotFoundError:
        print("Dados processados não encontrados. Execute o feature_engineering.py primeiro.")
        return

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    os.environ["MLFLOW_ALLOW_FILE_STORE"] = "true"
    mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "sqlite:///mlruns.db"))
    mlflow.set_experiment("CityOps_SLA_Prediction")
    
    with mlflow.start_run(run_name="Logistic_Regression_Baseline"):
        print("Treinando modelo de Regressão Logística (Baseline)...")
        model = LogisticRegression(max_iter=1000)
        model.fit(X_train, y_train)
        
        y_pred = model.predict(X_test)
        y_proba = model.predict_proba(X_test)[:, 1]
        
        f1 = f1_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        roc_auc = roc_auc_score(y_test, y_proba)
        
        print(f"Resultados: F1={f1:.4f}, Precision={precision:.4f}, Recall={recall:.4f}, ROC-AUC={roc_auc:.4f}")
        
        mlflow.log_param("model_type", "LogisticRegression")
        mlflow.log_metric("f1_score", f1)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        mlflow.log_metric("roc_auc", roc_auc)
        
        mlflow.sklearn.log_model(model, "model")
        print("Modelo registrado no MLflow.")

if __name__ == "__main__":
    train_baseline()
