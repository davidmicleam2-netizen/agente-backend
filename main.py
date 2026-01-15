import uvicorn
from fastapi import FastAPI, Request
import httpx
import os

# ==========================================
# CONFIGURACIÓN
# ==========================================
app = FastAPI(title="Servidor de Orquestación de Voz IA")

# Tu URL de Make (Ya la he incluido aquí)
MAKE_WEBHOOK_URL = "https://hook.eu2.make.com/wvkmaeg5w1vekjy5xk5do8j4kdn60v3q"

# ==========================================
# ENDPOINTS
# ==========================================
@app.get("/")
def health_check():
    return {"status": "online", "service": "Voice AI Orchestrator"}

@app.post("/voice-webhook")
async def handle_voice_event(request: Request):
    # 1. Recibimos el paquete de datos de Vapi
    payload = await request.json()
    
    # 2. Averiguamos qué tipo de mensaje es
    message_type = payload.get('message', {}).get('type')
    
    # Imprimimos para que lo veas en los logs (opcional)
    print(f"📡 Evento Recibido: {message_type}")

    # 3. FILTRO: Solo nos interesa cuando la llamada TERMINA
    if message_type == "end-of-call-report":
        print(f"🚀 LLAMADA FINALIZADA. Enviando datos a Make...")
        
        try:
            # 4. AQUÍ ESTÁ LA MAGIA: Enviamos los datos a Make
            async with httpx.AsyncClient() as client:
                response = await client.post(MAKE_WEBHOOK_URL, json=payload, timeout=10.0)
                print(f"✅ Make respondió: {response.status_code}")
        except Exception as e:
            print(f"❌ Error conectando con Make: {e}")

    return {"status": "received"}

# ==========================================
# EJECUCIÓN
# ==========================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
