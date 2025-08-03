from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from app.supabase_client import get_supabase_client
from app.rag_processor import generate_embedding, store_document_embedding, query_documents_by_embedding
import uuid # Para gerar IDs únicos para documentos

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

app = FastAPI(
    title="Maḥbūb The Ai Software Engineer Backend",
    description="API for advanced AI algorithms, focusing on Natural Language Processing.",
    version="0.1.0"
)

# CORS configuration
origins = [
    "http://localhost:3000",  # React default port
    "http://127.0.0.1:3000",
    "http://www.aigronovatec.com.br",
    "https://www.aigronovatec.com.br",
    "http://www.aigronovatech.com.br",
    "https://www.aigronovatech.com.br",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DocumentUpload(BaseModel):
    content: str

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    response: str
    retrieved_chunks: List[str]

# Mock Generation Logic (same as before)
def mock_generate(query: str, retrieved_chunks: List[str]) -> str:
    """Generates a more conversational response based on retrieved chunks and query."""
    if not retrieved_chunks:
        return f"Não encontrei informações relevantes para '{query}' nos documentos carregados. Por favor, carregue documentos relevantes para obter uma resposta mais precisa."
    
    combined_content = " ".join([chunk.get("content", "") for chunk in retrieved_chunks])
    
    if "visão geral" in query.lower() or "o que é" in query.lower():
        return f"Com base nas informações que encontrei sobre '{query}', a visão geral é: {combined_content[:500]}..."
    elif "como" in query.lower():
        return f"Para responder à sua pergunta sobre '{query}', o processo é: {combined_content[:500]}..."
    else:
        return f"Analisando os documentos relacionados a '{query}', a resposta é: {combined_content[:500]}..." # Truncate for brevity

# --- API Endpoints ---

@app.post("/upload-document", summary="Upload a text document for RAG processing")
async def upload_document(doc: DocumentUpload):
    try:
        supabase = get_supabase_client()
        doc_id = str(uuid.uuid4())
        embedding = await generate_embedding(doc.content)
        await store_document_embedding(supabase, doc_id, doc.content, embedding)
        return {"message": "Documento carregado e processado com sucesso!", "document_id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar documento: {e}")

@app.post("/query-rag", response_model=QueryResponse, summary="Query the RAG system with a natural language question")
async def query_rag(request: QueryRequest):
    try:
        supabase = get_supabase_client()
        query_embedding = await generate_embedding(request.query)
        retrieved_docs = await query_documents_by_embedding(supabase, query_embedding)
        
        # Extrair apenas o conteúdo dos documentos recuperados para a mock_generate
        retrieved_chunks_content = [doc.get("content", "") for doc in retrieved_docs]

        response_text = mock_generate(request.query, retrieved_chunks_content)
        
        return QueryResponse(response=response_text, retrieved_chunks=retrieved_chunks_content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao consultar RAG: {e}")

@app.get("/", summary="Root endpoint for API health check")
async def read_root():
    return {"message": "Maḥbūb The Ai Software Engineer Backend is running!"}



# To run: uvicorn main:app --reload