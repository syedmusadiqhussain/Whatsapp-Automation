import random
import string
from whatsapp_bots.bots.base_bot import BaseBot
from whatsapp_bots.core.session_manager import Session

class SupportBot(BaseBot):
    async def handle(self, phone: str, text: str, msg: dict, session: Session) -> None:
        if session.step == "start":
            await self.sender.text(phone, "I'm here to help. Please provide your Order ID.")
            session.step = "ask_order"
            
        elif session.step == "ask_order":
            session.data["order_id"] = text
            await self.sender.buttons(phone, "What is the issue?", ["Delivery Delay", "Lost Package", "Damaged Item"])
            session.step = "ask_issue"
            
        elif session.step == "ask_issue":
            session.data["issue"] = text
            ticket_id = "TKT-" + "".join(random.choices(string.digits, k=6))
            await self.sender.text(phone, f"Support ticket created! Your Ticket ID is {ticket_id}. We will get back to you within 24 hours.")
            session.reset()
