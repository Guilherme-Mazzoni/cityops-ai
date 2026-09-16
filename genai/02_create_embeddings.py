import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from openai import OpenAI
import time

env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv("DATABASE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL não configurada.")
if not OPENAI_API_KEY:
    print("AVISO: OPENAI_API_KEY não configurada. A extração vai abortar se não mockada.")

client = OpenAI(api_key=OPENAI_API_KEY)
engine = create_engine(DATABASE_URL)

def get_embeddings(texts):
    if not OPENAI_API_KEY:
        # Fallback/Mock para testes sem chave
        return [[0.0] * 1536 for _ in texts]
        
    try:
        response = client.embeddings.create(
            input=texts,
            model="text-embedding-3-small"
        )
        return [data.embedding for data in response.data]
    except Exception as e:
        print(f"Erro na OpenAI API: {e}")
        return []

def main():
    # Extrair uma pequena amostra para não estourar tokens e testar o conceito
    print("Extraindo amostra de chamados do banco...")
    query = """
        SELECT unique_key, complaint_type, descriptor, resolution_description 
        FROM public.raw_311_requests 
        WHERE descriptor IS NOT NULL AND resolution_description IS NOT NULL
        LIMIT 100
    """
    
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
    
    if df.empty:
        print("Nenhum dado encontrado para gerar embeddings.")
        return
        
    print(f"{len(df)} registros encontrados. Gerando textos compostos...")
    
    # Criar o texto que a IA vai "ler" e transformar em vetor
    df['text_to_embed'] = df.apply(
        lambda row: f"Tipo: {row['complaint_type']} | Descrição: {row['descriptor']} | Resolução: {row['resolution_description']}", 
        axis=1
    )
    
    print("Chamando a API de Embeddings da OpenAI...")
    # Em um ambiente real, você faria isso em batches (ex: 50 por vez)
    embeddings = get_embeddings(df['text_to_embed'].tolist())
    
    if not embeddings:
        print("Falha ao gerar embeddings.")
        return
        
    df['embedding'] = embeddings
    
    print("Salvando vetores no banco de dados...")
    with engine.begin() as conn:
        for _, row in df.iterrows():
            # Inserir o registro com o vetor usando parametrização para evitar injeção
            conn.execute(
                text("""
                    INSERT INTO complaint_embeddings 
                    (unique_key, complaint_type, descriptor, resolution_description, embedding)
                    VALUES (:unique_key, :complaint_type, :descriptor, :resolution_description, :embedding)
                """),
                {
                    "unique_key": row['unique_key'],
                    "complaint_type": row['complaint_type'],
                    "descriptor": row['descriptor'],
                    "resolution_description": row['resolution_description'],
                    "embedding": str(row['embedding']) # cast para string no formato pgvector '[0.1, 0.2, ...]'
                }
            )
            
    print("Sucesso! Embeddings salvos no pgvector.")

if __name__ == "__main__":
    main()
