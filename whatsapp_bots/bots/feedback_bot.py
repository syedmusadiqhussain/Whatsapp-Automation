from whatsapp_bots.bots.base_bot import BaseBot
from whatsapp_bots.core.session_manager import Session

class FeedbackBot(BaseBot):
    async def handle(self, phone: str, text: str, msg: dict, session: Session) -> None:
        if session.step == "start":
            await self.sender.text(phone, "We value your feedback! On a scale of 1 to 5, how would you rate our service?")
            session.step = "ask_rating"
            
        elif session.step == "ask_rating":
            if text.isdigit() and 1 <= int(text) <= 5:
                session.data["rating"] = int(text)
                await self.sender.text(phone, "Thank you! Any comments? (Type 'skip' to skip)")
                session.step = "ask_comment"
            else:
                await self.sender.text(phone, "Please provide a valid rating between 1 and 5.")
                
        elif session.step == "ask_comment":
            session.data["comment"] = text if text.lower() != "skip" else None
            await self.sender.buttons(phone, "Would you recommend us to a friend?", ["Yes", "Maybe", "No"])
            session.step = "ask_recommend"
            
        elif session.step == "ask_recommend":
            session.data["recommend"] = text
            rating = session.data["rating"]
            if rating >= 4:
                code = "THANKS10" if rating == 4 else "LOYAL15"
                await self.sender.text(phone, f"Thanks for the great rating! Use code {code} for your next order.")
            else:
                await self.sender.text(phone, "Thank you for your feedback. We will work to improve!")
            session.reset()
