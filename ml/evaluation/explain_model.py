import os
import mlflow
import pandas as pd
import shap
import matplotlib.pyplot as plt
import xgboost as xgb

# Configuração do MLflow
os.environ["MLFLOW_ALLOW_FILE_STORE"] = "true"
mlflow.set_tracking_uri("sqlite:///mlruns.db")

def explain_xgboost_model():
    print("Conectando ao MLflow...")
    experiment = mlflow.get_experiment_by_name("CityOps_SLA_Prediction")
    
    if not experiment:
        print("Erro: Experimento não encontrado.")
        return
        
    runs = mlflow.search_runs(
        experiment_ids=[experiment.experiment_id],
        filter_string="tags.mlflow.runName = 'XGBoost_Advanced'",
        order_by=["metrics.roc_auc DESC"],
        max_results=1
    )
    
    if runs.empty:
        print("Erro: Modelo XGBoost_Advanced não encontrado.")
        return
        
    best_run_id = runs.iloc[0].run_id
    print(f"Melhor modelo encontrado (Run ID: {best_run_id}). Carregando...")
    
    # Carregar modelo XGBoost puro logado no MLflow
    # O MLflow pyfunc carrega como um wrapper, mas o SHAP TreeExplainer precisa do modelo subjacente.
    # No train_xgboost.py nós provavelmente registramos com mlflow.xgboost.log_model ou sklearn
    # Vamos tentar carregar o modelo via pyfunc e extrair o modelo base se possível
    model_uri = f"runs:/{best_run_id}/model"
    model = mlflow.xgboost.load_model(model_uri)
    
    print("Carregando base de dados de validação (X_test)...")
    # Para o SHAP, precisamos de uma base de dados real
    X_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed", "X.csv")
    
    if not os.path.exists(X_path):
        print(f"Erro: Arquivo {X_path} não encontrado. Execute o feature_engineering.py primeiro.")
        return
        
    X = pd.read_csv(X_path)
    # Pegar apenas uma amostra de 1000 linhas para o SHAP não demorar muito
    X_sample = X.sample(n=min(1000, len(X)), random_state=42)
    
    print("Calculando SHAP values (isso pode levar alguns segundos)...")
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_sample)
    
    print("Gerando gráfico de explicação (Summary Plot)...")
    # Configurar matplotlib figure
    plt.figure(figsize=(10, 8))
    shap.summary_plot(shap_values, X_sample, show=False)
    
    # Salvar localmente
    output_path = os.path.join(os.path.dirname(__file__), "shap_summary.png")
    brain_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", ".gemini", "antigravity", "brain", "1e40f163-1f6b-4e99-a604-bcd92a9236f7", "shap_summary.png"))
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    
    try:
        # Também salva na pasta de artefatos do Gemini para visualização na UI
        plt.savefig(brain_path, dpi=300, bbox_inches='tight')
    except Exception as e:
        pass
        
    print(f"Gráfico salvo localmente em: {output_path}")
    
    # Salvar no MLflow
    print("Fazendo upload do gráfico para o MLflow...")
    with mlflow.start_run(run_id=best_run_id):
        mlflow.log_artifact(output_path, "explanations")
        
    print("Concluído! A Explicabilidade do Modelo (Fase 4) foi gerada com sucesso.")

if __name__ == "__main__":
    explain_xgboost_model()
