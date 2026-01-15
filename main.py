import uvicorn
from fastapi import FastAPI, Request
from pydantic import BaseModel
import httpx
import os

# ==========================================
# CONFIGURACIÓN
# ==========================================
app = FastAPI(title="Servidor de Orquestación de Voz IA")

# Webhook de Make.com (Pégalo aquí si ya lo tienes, si no, déjalo así por ahora)
MAKE_WEBHOOK_URL = "https://hook.eu2.make.com/wvkmaeg5w1vekjy5xk5do8j4kdn60v3q"

# ==========================================
# ENDPOINTS
# ==========================================
@app.get("/")
def health_check():
    return {"status": "online", "service": "Voice AI Orchestrator"}

@app.post("/voice-webhook")
async def handle_voice_event(request: Request):
    payload = await request.json()
    print(f"📡 Evento Recibido: {payload.get('message', 'No message')}")
    
    # Aquí iría tu lógica de conexión con Make
    return {"status": "received"}

# ==========================================
# EJECUCIÓN
# ==========================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
