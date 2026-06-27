from whatsapp_bots.bots.base_bot import BaseBot
from whatsapp_bots.core.session_manager import Session

class BookingBot(BaseBot):
    async def handle(self, phone: str, text: str, msg: dict, session: Session) -> None:
        if session.step == "start":
            await self.sender.buttons(phone, "What service would you like to book?", ["Consultation", "Maintenance", "Repair"])
            session.step = "ask_service"
            
        elif session.step == "ask_service":
            session.data["service"] = text
            await self.sender.buttons(phone, "Select a date:", ["May 10", "May 11", "May 12", "May 13", "May 14"])
            session.step = "ask_date"
            
        elif session.step == "ask_date":
            session.data["date"] = text
            await self.sender.buttons(phone, "Select a time slot:", ["09:00 AM", "11:00 AM", "02:00 PM", "04:00 PM"])
            session.step = "ask_time"
            
        elif session.step == "ask_time":
            session.data["time"] = text
            summary = (
                f"Booking Confirmed!\n"
                f"Service: {session.data['service']}\n"
                f"Date: {session.data['date']}\n"
                f"Time: {session.data['time']}"
            )
            await self.sender.text(phone, summary)
            session.reset()
