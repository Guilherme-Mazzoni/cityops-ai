import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL não configurada.")

engine = create_engine(DATABASE_URL)

def get_embeddings(texts):
    # Carrega o modelo super leve que roda na CPU localmente
    print("Carregando o modelo 'all-MiniLM-L6-v2'...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    print(f"Gerando embeddings para {len(texts)} textos (isso vai rodar 100% no seu PC)...")
    embeddings = model.encode(texts, show_progress_bar=True)
    
    # model.encode retorna um array NumPy, convertemos para lista de floats
    return [embedding.tolist() for embedding in embeddings]

def main():
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
    
    df['text_to_embed'] = df.apply(
        lambda row: f"Tipo: {row['complaint_type']} | Descrição: {row['descriptor']} | Resolução: {row['resolution_description']}", 
        axis=1
    )
    
    embeddings = get_embeddings(df['text_to_embed'].tolist())
    
    if not embeddings:
        print("Falha ao gerar embeddings.")
        return
        
    df['embedding'] = embeddings
    
    print("Salvando vetores no banco de dados...")
    with engine.begin() as conn:
        for _, row in df.iterrows():
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
                    "embedding": str(row['embedding'])
                }
            )
            
    print("Sucesso! Embeddings 100% locais salvos no pgvector.")

if __name__ == "__main__":
    main()
