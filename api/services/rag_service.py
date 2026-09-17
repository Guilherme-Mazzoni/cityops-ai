import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from groq import Groq
from sentence_transformers import SentenceTransformer

env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))
load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv("DATABASE_URL")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

engine = create_engine(DATABASE_URL)
groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

embedding_model = None

def get_query_embedding(query_text):
    global embedding_model
    if embedding_model is None:
        embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    return embedding_model.encode([query_text])[0].tolist()

def search_similar_complaints(query_embedding, limit=5):
    query = text("""
        SELECT 
            complaint_type, 
            descriptor, 
            resolution_description,
            1 - (embedding <=> CAST(:query_embedding AS vector)) as similarity_score
        FROM complaint_embeddings
        ORDER BY embedding <=> CAST(:query_embedding AS vector)
        LIMIT :limit
    """)
    
    with engine.connect() as conn:
        result = conn.execute(query, {"query_embedding": str(query_embedding), "limit": limit})
        return result.fetchall()

def ask_analyst(user_question: str):
    if not groq_client:
        return "ERRO: GROQ_API_KEY não configurada no servidor."
        
    try:
        query_emb = get_query_embedding(user_question)
        similar_records = search_similar_complaints(query_emb)
        
        if not similar_records:
            return "Não encontrei chamados similares na base."
            
        context_text = "\n".join([
            f"- Tipo: {r[0]} | Detalhe: {r[1]} | Resolução: {r[2]} (Score: {r[3]:.2f})"
            for r in similar_records
        ])
        
        prompt = f"""Você é o CityOps AI Analyst, um assistente inteligente de gestão urbana da cidade de Nova York.
Use APENAS o contexto abaixo de chamados reais para responder à pergunta do usuário.
Responda em português.

CONTEXTO:
{context_text}

PERGUNTA: {user_question}
"""
        
        completion = groq_client.chat.completions.create(
            model="qwen/qwen3.8-27b",
            messages=[
                {"role": "system", "content": "Você é um analista de dados especialista em gestão pública."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=800
        )
        return completion.choices[0].message.content
        
    except Exception as e:
        return f"Erro interno do RAG: {e}"
