import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL não configurada.")

def get_data():
    engine = create_engine(DATABASE_URL)
    # Ler a tabela analítica do dbt (assumindo que o schema é analytics)
    # Para demonstração, faremos uma leitura robusta caso as views/tabelas existam.
    query = """
        SELECT 
            agency,
            complaint_type,
            borough,
            status,
            is_sla_violated,
            resolution_time_hours,
            sla_target_hours
        FROM analytics.mart_sla
        WHERE is_sla_violated IS NOT NULL
    """
    try:
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        print(f"Erro ao ler os dados: {e}")
        # Retornar um dataframe vazio mockado se o dbt ainda não rodou no banco
        return pd.DataFrame(columns=["agency", "complaint_type", "borough", "status", "is_sla_violated"])

def prepare_features(df):
    if df.empty:
        print("Dataset vazio. Abortando feature engineering.")
        return None, None

    # Filtrar classes muito raras ou nulas para estabilidade
    df = df.dropna(subset=['agency', 'complaint_type', 'borough'])
    
    # Separar Target e Features
    X = df[['agency', 'complaint_type', 'borough']]
    y = df['is_sla_violated'].astype(int)
    
    # One-Hot Encoding das variáveis categóricas
    X_encoded = pd.get_dummies(X, columns=['agency', 'complaint_type', 'borough'])
    
    # Salvar o dataset transformado localmente para o ML
    os.makedirs(os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed"), exist_ok=True)
    X_encoded.to_csv(os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed", "X.csv"), index=False)
    y.to_csv(os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed", "y.csv"), index=False)
    
    print(f"Features geradas com sucesso! Shape: {X_encoded.shape}")
    return X_encoded, y

if __name__ == "__main__":
    df_raw = get_data()
    X, y = prepare_features(df_raw)
