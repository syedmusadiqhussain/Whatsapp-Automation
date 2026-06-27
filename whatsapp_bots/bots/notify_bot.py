import asyncio
from whatsapp_bots.bots.base_bot import BaseBot
from whatsapp_bots.core.session_manager import Session

class NotifyBot(BaseBot):
    async def handle(self, phone: str, text: str, msg: dict, session: Session) -> None:
        if text.upper() in ["STOP", "UNSUBSCRIBE"]:
            await self.sender.text(phone, "You have been unsubscribed from notifications.")
            session.reset()
        else:
            # Default behavior for NotifyBot when reached via keyword
            await self.sender.text(phone, "This channel is used for notifications. Reply STOP to unsubscribe.")
            session.reset()

    async def broadcast(self, template_name: str, recipients: list, language: str = "en_US"):
        sent = 0
        failed = 0
        
        for phone in recipients:
            try:
                # In a real scenario, components would be passed here
                res = await self.sender.template(phone, template_name, lang=language)
                if res:
                    sent += 1
                else:
                    failed += 1
                
                # Rate limit: ~80/sec
                await asyncio.sleep(0.013)
            except Exception:
                failed += 1
                
        return {
            "template": template_name,
            "sent": sent,
            "failed": failed
        }
