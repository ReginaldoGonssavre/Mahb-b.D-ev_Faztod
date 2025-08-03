from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api.v1.endpoints import api_router
from backend.app.core.config import settings
from backend.app.db.base import Base
from backend.app.db.session import engine, connect_to_mongo, close_mongo_connection

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    openapi_url=f"/openapi.json",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ajuste para domínios específicos em produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Eventos de inicialização e desligamento
@app.on_event("startup")
async def startup_event():
    # Cria tabelas no PostgreSQL
    Base.metadata.create_all(bind=engine)
    # Conecta ao MongoDB
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_event():
    # Fecha conexão com MongoDB
    await close_mongo_connection()

# Inclui rotas da API
app.include_router(api_router, prefix="/api/v1")

# WebSocket Endpoint (Placeholder)
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")

# gRPC Placeholder (Conceptual - requer geração de código gRPC)
# Para gRPC, você precisaria de arquivos .proto e código gerado.
# Isso seria implementado como um serviço separado ou integrado via um gateway gRPC.
# Ex: from backend.app.grpc_server import serve_grpc_async
# @app.on_event("startup")
# async def start_grpc_server():
#     await serve_grpc_async()

@app.get("/")
async def root():
    return {"message": "CompassAI Platform Backend is running!"}
