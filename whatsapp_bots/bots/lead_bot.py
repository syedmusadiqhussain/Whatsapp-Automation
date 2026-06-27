from whatsapp_bots.bots.base_bot import BaseBot
from whatsapp_bots.core.session_manager import Session

class LeadBot(BaseBot):
    async def handle(self, phone: str, text: str, msg: dict, session: Session) -> None:
        if session.step == "start":
            await self.sender.text(phone, "Welcome! Let's get you started. What is your full name?")
            session.step = "ask_name"
        
        elif session.step == "ask_name":
            session.data["name"] = text
            await self.sender.text(phone, f"Thanks {text}! What is your email address?")
            session.step = "ask_email"
            
        elif session.step == "ask_email":
            session.data["email"] = text
            await self.sender.buttons(phone, "Which product are you interested in?", ["SaaS Platform", "Mobile App", "Web Design"])
            session.step = "ask_product"
            
        elif session.step == "ask_product":
            session.data["product"] = text
            # Log lead data (hook point for CRM API)
            print(f"NEW LEAD: {session.data}")
            await self.sender.text(phone, "Thank you! Our team will contact you soon.")
            session.reset()
