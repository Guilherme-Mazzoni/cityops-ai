import os
import mlflow
import pandas as pd
import xgboost as xgb
import numpy as np

# Configuração do MLflow
os.environ["MLFLOW_ALLOW_FILE_STORE"] = "true"
mlflow.set_tracking_uri("sqlite:///mlruns.db")

def predict_sla_delay(borough: str, agency: str, complaint_type: str):
    """
    Carrega o modelo XGBoost salvo no MLflow e gera uma predição real
    baseada nas features (One-Hot Encoded) recebidas do frontend.
    """
    try:
        experiment = mlflow.get_experiment_by_name("CityOps_SLA_Prediction")
        if not experiment:
            return {"error": "Experimento MLflow não encontrado."}
            
        runs = mlflow.search_runs(
            experiment_ids=[experiment.experiment_id],
            order_by=["metrics.roc_auc DESC"],
            max_results=1
        )
        
        if runs.empty:
            return {"error": "Nenhum modelo treinado encontrado."}
            
        best_run_id = runs.iloc[0].run_id
        best_auc = runs.iloc[0]["metrics.roc_auc"]
        model_name = runs.iloc[0]["tags.mlflow.runName"]
        
        # Leitura rápida do cabeçalho do dataset de treino para reconstruir as colunas exatas
        X_csv_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed", "X.csv")
        with open(X_csv_path, 'r', encoding='utf-8') as f:
            columns_str = f.readline().strip()
        columns = columns_str.split(',')
        
        # Criando o DataFrame 0-filled
        input_data = pd.DataFrame(0, index=[0], columns=columns)
        
        # Preenchendo os 1s para o One-Hot Encoding
        agency_col = f"agency_{agency.upper()}"
        # Preserva case sensivity do complaint_type, ou tenta match exato
        complaint_col = f"complaint_type_{complaint_type}"
        borough_col = f"borough_{borough.upper()}"
        
        if agency_col in columns:
            input_data[agency_col] = 1
        if complaint_col in columns:
            input_data[complaint_col] = 1
        if borough_col in columns:
            input_data[borough_col] = 1
            
        # Carregando a API nativa do XGBoost via MLflow
        model_uri = f"runs:/{best_run_id}/model"
        model = mlflow.xgboost.load_model(model_uri)
        
        # Predição Real (Retorna Probabilidade no objective binary:logistic)
        dmatrix = xgb.DMatrix(input_data)
        probability = float(model.predict(dmatrix)[0])
        
        return {
            "prediction": "DELAY_EXPECTED" if probability > 0.5 else "ON_TIME",
            "probability": probability,
            "model_used": model_name,
            "model_run_id": best_run_id,
            "model_roc_auc": best_auc,
            "note": "Predição Real via XGBoost nativo"
        }
        
    except Exception as e:
        return {"error": str(e)}
