from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from api.services.ml_service import predict_sla_delay
from api.services.rag_service import ask_analyst

app = FastAPI(
    title="CityOps AI API",
    description="API central do CityOps AI para predição de SLA (Machine Learning) e Chatbot de RAG (GenAI)",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SLAPredictionRequest(BaseModel):
    borough: str
    agency: str
    complaint_type: str

class ChatRequest(BaseModel):
    question: str

@app.get("/")
def read_root():
    return {"status": "ok", "message": "CityOps AI API está online! Acesse /docs para testar os endpoints."}

@app.post("/predict-sla")
def predict_sla(request: SLAPredictionRequest):
    """
    Prediz a probabilidade de um chamado estourar o SLA.
    """
    result = predict_sla_delay(request.borough, request.agency, request.complaint_type)
    return result

@app.post("/ask-analyst")
def ask_analyst_endpoint(request: ChatRequest):
    """
    Faz uma pergunta ao AI Analyst. 
    A inteligência fará a busca no PostgreSQL pgvector e usará o Groq Llama/Mixtral para responder.
    """
    answer = ask_analyst(request.question)
    return {"question": request.question, "answer": answer}

if __name__ == "__main__":
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
