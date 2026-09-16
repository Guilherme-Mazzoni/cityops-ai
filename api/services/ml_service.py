import os
import mlflow
import pandas as pd

# Configuração do MLflow
os.environ["MLFLOW_ALLOW_FILE_STORE"] = "true"
mlflow.set_tracking_uri("sqlite:///mlruns.db")

def predict_sla_delay(borough: str, agency: str, complaint_type: str):
    """
    Simula a predição de atraso de SLA.
    Em produção, esta função carregaria o TargetEncoder salvo no MLflow 
    e transformaria as strings de entrada nas features numéricas que o modelo XGBoost espera.
    """
    try:
        experiment = mlflow.get_experiment_by_name("CityOps_SLA_Prediction")
        if not experiment:
            return {"error": "Experimento MLflow não encontrado."}
            
        # Busca o melhor modelo (XGBoost) baseado na métrica ROC-AUC
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
        
        # Para carregar o modelo real e prever:
        # model_uri = f"runs:/{best_run_id}/model"
        # model = mlflow.pyfunc.load_model(model_uri)
        # return model.predict(encoded_data)
        
        # Retornamos uma predição simulada, mas comprovando que achamos o modelo no MLflow!
        return {
            "prediction": "DELAY_EXPECTED",
            "probability": 0.87,
            "model_used": model_name,
            "model_run_id": best_run_id,
            "model_roc_auc": best_auc,
            "note": "MVP: Para predição real, o TargetEncoder das categorias precisa ser serializado no treinamento."
        }
        
    except Exception as e:
        return {"error": str(e)}
