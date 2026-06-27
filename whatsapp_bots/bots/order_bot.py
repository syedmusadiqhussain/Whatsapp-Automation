from whatsapp_bots.bots.base_bot import BaseBot
from whatsapp_bots.core.session_manager import Session

MOCK_ORDERS = {
    "ORD-123": {"status": "In Transit", "eta": "2024-05-15", "carrier": "DHL", "tracking": "DHL987654"},
    "ORD-456": {"status": "Delivered", "eta": "2024-05-08", "carrier": "FedEx", "tracking": "FEDEX12345"},
    "ORD-789": {"status": "Processing", "eta": "2024-05-20", "carrier": "UPS", "tracking": "UPS445566"}
}

class OrderBot(BaseBot):
    async def handle(self, phone: str, text: str, msg: dict, session: Session) -> None:
        if session.step == "start":
            await self.sender.text(phone, "Please enter your Order ID to track your shipment.")
            session.step = "ask_order"
            
        elif session.step == "ask_order":
            order_id = text.upper()
            if order_id in MOCK_ORDERS:
                order = MOCK_ORDERS[order_id]
                msg_body = (
                    f"Order: {order_id}\n"
                    f"Status: {order['status']}\n"
                    f"ETA: {order['eta']}\n"
                    f"Carrier: {order['carrier']}\n"
                    f"Tracking: {order['tracking']}"
                )
                await self.sender.buttons(phone, msg_body, ["Return/Refund", "Contact Support", "All Good"])
                session.step = "ask_action"
            else:
                await self.sender.text(phone, "Order not found. Please check the ID and try again.")
                # Stay in ask_order step
            
        elif session.step == "ask_action":
            await self.sender.text(phone, "Thank you for using our service!")
            session.reset()
