import hashlib
import hmac
import json
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException, Query, Response
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
# Adjust import to use absolute package path when running as a module
from whatsapp_bots.config.settings import settings
from whatsapp_bots.core.sender import Sender
from whatsapp_bots.core.session_manager import SessionManager
from whatsapp_bots.core.router import Router

# Initialize core components
sender = Sender()
session_manager = SessionManager()
router = Router(sender, session_manager)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("WhatsApp Chatbot Suite starting up...")
    yield
    # Shutdown
    print("WhatsApp Chatbot Suite shutting down...")

app = FastAPI(title="WhatsApp Chatbot Suite", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def verify_signature(payload: bytes, signature: str):
    if not settings.META_APP_SECRET:
        return True # Skip if secret not set for dev
    
    expected_signature = "sha256=" + hmac.new(
        settings.META_APP_SECRET.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected_signature, signature)

@app.get("/")
async def root():
    return {
        "message": "Welcome to the WhatsApp Chatbot Suite API",
        "docs": "/docs",
        "health": "/health",
        "status": "online"
    }

@app.get("/webhook")
async def verify_webhook(
    mode: str = Query(None, alias="hub.mode"),
    token: str = Query(None, alias="hub.verify_token"),
    challenge: str = Query(None, alias="hub.challenge")
):
    print(f"Verification attempt: mode={mode}, token={token}")
    if mode == "subscribe" and token == settings.META_VERIFY_TOKEN:
        print("Verification successful!")
        return PlainTextResponse(content=challenge)
    
    print("Verification failed: Token mismatch or invalid mode.")
    raise HTTPException(status_code=403, detail="Verification failed")

@app.post("/webhook")
async def handle_webhook(request: Request):
    payload = await request.body()
    signature = request.headers.get("X-Hub-Signature-256")
    
    if not verify_signature(payload, signature):
        raise HTTPException(status_code=403, detail="Invalid signature")
    
    data = json.loads(payload)
    
    # Process WhatsApp message
    try:
        if "entry" in data:
            for entry in data["entry"]:
                for change in entry.get("changes", []):
                    value = change.get("value", {})
                    if "messages" in value:
                        for msg in value["messages"]:
                            phone = msg["from"]
                            text = ""
                            
                            if msg["type"] == "text":
                                text = msg["text"]["body"]
                            elif msg["type"] == "interactive":
                                if msg["interactive"]["type"] == "button_reply":
                                    text = msg["interactive"]["button_reply"]["title"]
                                elif msg["interactive"]["type"] == "list_reply":
                                    text = msg["interactive"]["list_reply"]["title"]
                            
                            if text:
                                await router.route(phone, text, msg)
                                
    except Exception as e:
        print(f"Error processing webhook: {e}")
        
    return {"status": "ok"}

@app.post("/api/broadcast")
async def broadcast_notification(template: str, recipients: list):
    notify_bot = router.bots["notify_bot"]
    result = await notify_bot.broadcast(template, recipients)
    return result

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "bots": len(router.bots),
        "env": settings.ENV
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.PORT)
