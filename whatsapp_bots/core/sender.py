import httpx
from whatsapp_bots.config.settings import settings

class Sender:
    def __init__(self):
        self.url = f"{settings.META_API_URL}/{settings.META_PHONE_NUMBER_ID}/messages"
        self.headers = {
            "Authorization": f"Bearer {settings.META_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }

    async def _send(self, payload: dict):
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(self.url, headers=self.headers, json=payload)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                print(f"Error sending message: {e}")
                return None

    async def text(self, to: str, body: str):
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "text",
            "text": {"body": body}
        }
        return await self._send(payload)

    async def buttons(self, to: str, body: str, options: list):
        # Meta allows max 3 buttons
        buttons = []
        for i, opt in enumerate(options[:3]):
            buttons.append({
                "type": "reply",
                "reply": {
                    "id": f"btn_{i}",
                    "title": opt[:20] # Max 20 chars
                }
            })
        
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {"text": body},
                "action": {"buttons": buttons}
            }
        }
        return await self._send(payload)

    async def list_message(self, to: str, body: str, button_label: str, sections: list):
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "body": {"text": body},
                "action": {
                    "button": button_label,
                    "sections": sections
                }
            }
        }
        return await self._send(payload)

    async def template(self, to: str, name: str, lang: str = "en_US", components: list = None):
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "template",
            "template": {
                "name": name,
                "language": {"code": lang},
                "components": components or []
            }
        }
        return await self._send(payload)
