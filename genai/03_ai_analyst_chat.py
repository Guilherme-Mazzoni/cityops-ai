import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from openai import OpenAI

env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv("DATABASE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not DATABASE_URL or not OPENAI_API_KEY:
    raise ValueError("DATABASE_URL ou OPENAI_API_KEY não configuradas no .env")

client = OpenAI(api_key=OPENAI_API_KEY)
engine = create_engine(DATABASE_URL)

def get_query_embedding(query_text):
    """Converte a pergunta do usuário em vetor usando OpenAI."""
    try:
        response = client.embeddings.create(
            input=[query_text],
            model="text-embedding-3-small"
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Erro ao gerar embedding da pergunta: {e}")
        return None

def search_similar_complaints(query_embedding, limit=5):
    """Busca no PostgreSQL (pgvector) os chamados mais semanticamente parecidos usando Distância de Cosseno (<=>)"""
    embedding_str = str(query_embedding)
    
    query = text("""
        SELECT 
            complaint_type, 
            descriptor, 
            resolution_description,
            1 - (embedding <=> :query_embedding::vector) as similarity_score
        FROM complaint_embeddings
        ORDER BY embedding <=> :query_embedding::vector
        LIMIT :limit
    """)
    
    with engine.connect() as conn:
        result = conn.execute(query, {"query_embedding": embedding_str, "limit": limit})
        return result.fetchall()

def ask_ai_analyst(user_question):
    print(f"\nUsuário: {user_question}")
    print("AI Analyst: Pensando e buscando dados...")
    
    # 1. Converter pergunta em vetor
    query_emb = get_query_embedding(user_question)
    if not query_emb:
        return "Desculpe, não consegui converter sua pergunta."
        
    # 2. Buscar contexto similar no banco
    similar_records = search_similar_complaints(query_emb)
    
    if not similar_records:
        return "Não encontrei chamados similares na base de dados para te responder."
        
    # 3. Montar o Prompt com o Contexto (RAG - Retrieval Augmented Generation)
    context_text = "\n".join([
        f"- Tipo: {r[0]} | Detalhe: {r[1]} | Resolução: {r[2]} (Score Semântico: {r[3]:.2f})"
        for r in similar_records
    ])
    
    prompt = f"""Você é o CityOps AI Analyst, um assistente inteligente de gestão urbana da cidade de Nova York.
Use APENAS o contexto abaixo de chamados reais (311) para responder à pergunta do usuário.
Se a resposta não estiver no contexto, diga que não tem dados suficientes. Seja claro, direto e profissional.

CONTEXTO DOS CHAMADOS MAIS RELEVANTES:
{context_text}

PERGUNTA DO USUÁRIO: {user_question}
"""
    
    # 4. Enviar para o GPT-4o-mini ou GPT-3.5 responder
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Você é um analista de dados especialista em gestão pública e zeladoria urbana."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Erro ao gerar resposta com LLM: {e}"

if __name__ == "__main__":
    # Exemplo de teste da Busca Vetorial + IA
    pergunta = "Quais são as reclamações mais comuns sobre entulho e lixo nas ruas, e como elas são geralmente resolvidas?"
    resposta = ask_ai_analyst(pergunta)
    print(f"\n================ RESPOSTA ================\n{resposta}\n==========================================\n")
