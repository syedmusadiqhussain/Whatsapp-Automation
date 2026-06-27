from whatsapp_bots.bots.base_bot import BaseBot
from whatsapp_bots.core.session_manager import Session
from whatsapp_bots.core.llm_client import llm_client

FAQ_DB = {
    "pricing": "Our plans start at $29/month. Check our website for details.",
    "location": "We are based in San Francisco, CA.",
    "hours": "We are open Monday to Friday, 9 AM to 6 PM PST.",
    "refund": "We offer a 30-day money-back guarantee.",
    "security": "Your data is encrypted using AES-256 standards.",
    "integration": "We integrate with Zapier, Slack, and HubSpot.",
    "api": "Our API documentation is available at developers.example.com.",
    "support": "You can reach support by typing 'issue' or emailing support@example.com.",
    "careers": "We are always looking for talent! Check example.com/careers.",
    "demo": "You can book a live demo via the 'book' command."
}

class FAQBot(BaseBot):
    async def handle(self, phone: str, text: str, msg: dict, session: Session) -> None:
        query = text.lower()
        found = False
        
        for keyword, answer in FAQ_DB.items():
            if keyword in query:
                await self.sender.text(phone, answer)
                found = True
                break
        
        if not found:
            # Use LLM as fallback for FAQ
            messages = [
                {"role": "system", "content": "You are a helpful customer support assistant for our WhatsApp Bot Suite. Use the provided knowledge base to answer questions. If the answer is not in the knowledge base, answer politely based on general knowledge but stay professional."},
                {"role": "user", "content": f"Knowledge Base: {FAQ_DB}\n\nUser Question: {text}"}
            ]
            llm_response = await llm_client.chat_completion(messages)
            
            if llm_response:
                await self.sender.text(phone, llm_response)
            else:
                await self.sender.text(phone, "I'm sorry, I don't have an answer for that. Type 'menu' to see what I can help you with.")
        
        session.reset()
