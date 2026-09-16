import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL não configurada.")

def setup_vector_db():
    print(f"Conectando ao banco de dados: {DATABASE_URL}")
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as conn:
        print("Habilitando extensão pgvector...")
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        
        print("Limpando tabela antiga (se existir)...")
        conn.execute(text("DROP TABLE IF EXISTS complaint_embeddings;"))
        
        # Reduzimos a dimensão do VECTOR de 1536 (OpenAI) para 384 (sentence-transformers: all-MiniLM-L6-v2)
        print("Criando tabela complaint_embeddings (VECTOR 384D)...")
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS complaint_embeddings (
                id SERIAL PRIMARY KEY,
                unique_key BIGINT NOT NULL,
                complaint_type VARCHAR(255),
                descriptor TEXT,
                resolution_description TEXT,
                embedding VECTOR(384)
            );
        """))
        
        print("Criando índice HNSW para buscas rápidas...")
        try:
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS embedding_idx ON complaint_embeddings 
                USING hnsw (embedding vector_cosine_ops);
            """))
        except Exception as e:
            print(f"Aviso ao criar o índice: {e}. (Opcional, continuaremos sem ele).")
            
        conn.commit()
    
    print("Setup do Banco de Dados Vetorial concluído com sucesso!")

if __name__ == "__main__":
    setup_vector_db()
