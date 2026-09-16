import os
import mlflow
import pandas as pd

def compare_models():
    os.environ["MLFLOW_ALLOW_FILE_STORE"] = "true"
    mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "sqlite:///mlruns.db"))
    experiment = mlflow.get_experiment_by_name("CityOps_SLA_Prediction")
    
    if not experiment:
        print("Nenhum experimento encontrado. Por favor rode os treinamentos primeiro.")
        return

    runs = mlflow.search_runs(experiment_ids=[experiment.experiment_id])
    
    if runs.empty:
        print("Nenhuma rodada de teste (run) encontrada.")
        return

    print("--- Relatório de Comparação de Modelos ---")
    
    # Exibir métricas principais ordenadas pelo melhor f1_score
    results = runs[['tags.mlflow.runName', 'metrics.f1_score', 'metrics.precision', 'metrics.recall', 'metrics.roc_auc']]
    results = results.sort_values(by='metrics.f1_score', ascending=False)
    
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)
    print(results.to_string(index=False))
    
    print("\nMelhor modelo com base no F1-Score:")
    best_run = results.iloc[0]
    print(best_run)

if __name__ == "__main__":
    compare_models()
