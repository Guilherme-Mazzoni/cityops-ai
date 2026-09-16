import os
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, precision_score, recall_score, roc_auc_score
import mlflow
import mlflow.xgboost

def train_xgboost():
    data_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed")
    
    try:
        X = pd.read_csv(os.path.join(data_dir, "X.csv"))
        y = pd.read_csv(os.path.join(data_dir, "y.csv"))['is_sla_violated']
    except FileNotFoundError:
        print("Dados processados não encontrados. Execute o feature_engineering.py primeiro.")
        return

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "file://" + os.path.join(os.path.dirname(__file__), "..", "..", "mlruns")))
    mlflow.set_experiment("CityOps_SLA_Prediction")
    
    with mlflow.start_run(run_name="XGBoost_Advanced"):
        print("Treinando modelo XGBoost (Avançado)...")
        
        # Parâmetros básicos
        params = {
            "objective": "binary:logistic",
            "eval_metric": "auc",
            "max_depth": 5,
            "learning_rate": 0.1,
            "n_estimators": 100
        }
        
        model = xgb.XGBClassifier(**params, use_label_encoder=False)
        model.fit(X_train, y_train)
        
        y_pred = model.predict(X_test)
        y_proba = model.predict_proba(X_test)[:, 1]
        
        f1 = f1_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        roc_auc = roc_auc_score(y_test, y_proba)
        
        print(f"Resultados XGBoost: F1={f1:.4f}, Precision={precision:.4f}, Recall={recall:.4f}, ROC-AUC={roc_auc:.4f}")
        
        mlflow.log_params(params)
        mlflow.log_param("model_type", "XGBoost")
        mlflow.log_metric("f1_score", f1)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        mlflow.log_metric("roc_auc", roc_auc)
        
        mlflow.xgboost.log_model(model, "model")
        print("Modelo XGBoost registrado no MLflow.")

if __name__ == "__main__":
    train_xgboost()
