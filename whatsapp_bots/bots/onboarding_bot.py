from whatsapp_bots.bots.base_bot import BaseBot
from whatsapp_bots.core.session_manager import Session

class OnboardingBot(BaseBot):
    async def handle(self, phone: str, text: str, msg: dict, session: Session) -> None:
        if session.step == "start":
            await self.sender.text(phone, "Welcome! Let's set up your profile. What is your name?")
            session.step = "ask_name"
            
        elif session.step == "ask_name":
            session.data["name"] = text
            await self.sender.text(phone, "Great! What is your email address?")
            session.step = "ask_email"
            
        elif session.step == "ask_email":
            session.data["email"] = text
            await self.sender.text(phone, "Which city are you located in?")
            session.step = "ask_city"
            
        elif session.step == "ask_city":
            session.data["city"] = text
            await self.sender.buttons(phone, "How should we contact you?", ["WhatsApp Only", "Email Only", "Both"])
            session.step = "ask_pref"
            
        elif session.step == "ask_pref":
            session.data["preference"] = text
            await self.sender.text(phone, f"Registration complete! Welcome aboard, {session.data['name']}!")
            session.reset()
