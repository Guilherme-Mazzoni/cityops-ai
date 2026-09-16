import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("A variável de ambiente DATABASE_URL não foi encontrada. Verifique o arquivo .env.")

# Caminho para o dataset bruto
RAW_DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "nyc_311.csv")

def run_ingestion():
    print(f"Lendo os dados de {RAW_DATA_PATH}...")
    
    if not os.path.exists(RAW_DATA_PATH):
        raise FileNotFoundError(f"Arquivo não encontrado: {RAW_DATA_PATH}")

    # Leitura do CSV
    df = pd.read_csv(RAW_DATA_PATH)
    print(f"Dataset carregado com {len(df)} linhas e {len(df.columns)} colunas.")
    
    # Padronização básica das colunas
    df.columns = [c.lower().replace(' ', '_').replace('-', '_') for c in df.columns]
    
    print("Conectando ao banco de dados...")
    engine = create_engine(DATABASE_URL)
    
    table_name = "raw_311_requests"
    print(f"Inserindo os dados na tabela {table_name}...")
    
    # Escrevendo no PostgreSQL (pode demorar dependendo do tamanho)
    df.to_sql(table_name, engine, if_exists='replace', index=False, chunksize=10000)
    
    print("Ingestão concluída com sucesso!")

if __name__ == "__main__":
    run_ingestion()
