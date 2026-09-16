import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from groq import Groq
from sentence_transformers import SentenceTransformer

env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv("DATABASE_URL")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL não configurada no .env")

if not GROQ_API_KEY:
    print("AVISO: GROQ_API_KEY não encontrada no .env. A geração de texto com Llama 3 irá falhar.")

# Cliente Groq
if GROQ_API_KEY:
    groq_client = Groq(api_key=GROQ_API_KEY)
else:
    groq_client = None

engine = create_engine(DATABASE_URL)

# Carregamento preguiçoso do modelo de embeddings local
embedding_model = None

def get_query_embedding(query_text):
    """Converte a pergunta do usuário em vetor usando o modelo local (sentence-transformers)."""
    global embedding_model
    if embedding_model is None:
        print("Carregando modelo local de embeddings na memória...")
        embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    
    embedding = embedding_model.encode([query_text])
    return embedding[0].tolist()

def search_similar_complaints(query_embedding, limit=5):
    """Busca no PostgreSQL (pgvector) os chamados mais semanticamente parecidos"""
    embedding_str = str(query_embedding)
    
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
        result = conn.execute(query, {"query_embedding": embedding_str, "limit": limit})
        return result.fetchall()

def ask_ai_analyst(user_question):
    print(f"\nUsuário: {user_question}")
    print("AI Analyst: Pensando e buscando dados...")
    
    # 1. Converter pergunta em vetor localmente
    query_emb = get_query_embedding(user_question)
    
    # 2. Buscar contexto similar no banco
    similar_records = search_similar_complaints(query_emb)
    
    if not similar_records:
        return "Não encontrei chamados similares na base de dados para te responder."
        
    # 3. Montar o Prompt com o Contexto
    context_text = "\n".join([
        f"- Tipo: {r[0]} | Detalhe: {r[1]} | Resolução: {r[2]} (Score: {r[3]:.2f})"
        for r in similar_records
    ])
    
    prompt = f"""Você é o CityOps AI Analyst, um assistente inteligente de gestão urbana da cidade de Nova York.
Use APENAS o contexto abaixo de chamados reais (311) para responder à pergunta do usuário.
Se a resposta não estiver no contexto, diga que não tem dados suficientes. Seja claro, direto e profissional.
Responda em português.

CONTEXTO DOS CHAMADOS MAIS RELEVANTES:
{context_text}

PERGUNTA DO USUÁRIO: {user_question}
"""
    
    # 4. Enviar para o Groq (Llama 3 8B) responder de graça e super rápido!
    if not groq_client:
        return f"ERRO: Chave do Groq ausente. O contexto recuperado foi:\n{context_text}"
        
    try:
        completion = groq_client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "Você é um analista de dados especialista em gestão pública."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Erro ao gerar resposta com Groq: {e}"

if __name__ == "__main__":
    pergunta = "Quais são as reclamações mais comuns sobre entulho e lixo nas ruas, e como elas são geralmente resolvidas?"
    resposta = ask_ai_analyst(pergunta)
    print(f"\n================ RESPOSTA ================\n{resposta}\n==========================================\n")
