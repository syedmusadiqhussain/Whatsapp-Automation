from whatsapp_bots.bots.base_bot import BaseBot
from whatsapp_bots.core.session_manager import Session

MOCK_INVOICES = {
    "INV-001": {"amount": "$150.00", "due_date": "2024-05-20", "status": "unpaid"},
    "INV-002": {"amount": "$320.50", "due_date": "2024-05-15", "status": "unpaid"},
    "INV-003": {"amount": "$75.00", "due_date": "2024-05-01", "status": "paid"}
}

class PaymentBot(BaseBot):
    async def handle(self, phone: str, text: str, msg: dict, session: Session) -> None:
        if session.step == "start":
            await self.sender.text(phone, "Please enter your Invoice ID.")
            session.step = "ask_invoice"
            
        elif session.step == "ask_invoice":
            inv_id = text.upper()
            if inv_id in MOCK_INVOICES:
                inv = MOCK_INVOICES[inv_id]
                if inv["status"] == "paid":
                    await self.sender.text(phone, f"Invoice {inv_id} is already paid. Thank you!")
                    session.reset()
                else:
                    msg_body = (
                        f"Invoice: {inv_id}\n"
                        f"Amount: {inv['amount']}\n"
                        f"Due Date: {inv['due_date']}\n\n"
                        f"Pay here: https://stripe.com/pay/{inv_id}"
                    )
                    await self.sender.buttons(phone, msg_body, ["I've Paid", "Bank Transfer", "Need Help"])
                    session.step = "show_payment"
            else:
                await self.sender.text(phone, "Invoice not found. Please try again.")
                
        elif session.step == "show_payment":
            await self.sender.text(phone, "Got it. We will verify your payment shortly.")
            session.reset()
