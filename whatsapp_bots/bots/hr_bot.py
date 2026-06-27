import random
import string
from whatsapp_bots.bots.base_bot import BaseBot
from whatsapp_bots.core.session_manager import Session

LEAVE_BALANCE = {
    "Annual": 15,
    "Sick": 10,
    "Casual": 5,
    "Maternity/Paternity": 90
}

HR_FAQ = {
    "salary": "Salaries are credited on the last working day of each month.",
    "insurance": "Our health insurance is provided by BlueCross. Policy details are on the portal.",
    "policy": "The full company policy handbook is available on the internal HR portal.",
    "holiday": "You can find the 2024 holiday calendar on the HR portal under 'Documents'.",
    "referral": "We offer a $1000 bonus for successful employee referrals.",
    "appraisal": "Performance appraisals happen twice a year, in June and December.",
    "probation": "The standard probation period is 3 to 6 months depending on the role."
}

class HRBot(BaseBot):
    async def handle(self, phone: str, text: str, msg: dict, session: Session) -> None:
        if session.step == "start":
            await self.sender.buttons(phone, "Welcome to HR. How can I help?", ["Apply Leave", "Check Balance", "HR FAQ"])
            session.step = "main_menu"
            
        elif session.step == "main_menu":
            choice = text.lower()
            if "leave" in choice:
                await self.sender.buttons(phone, "Select leave type:", ["Annual", "Sick", "Casual"])
                session.step = "ask_leave_type"
            elif "balance" in choice:
                balance_str = "\n".join([f"{k}: {v} days" for k, v in LEAVE_BALANCE.items()])
                await self.sender.text(phone, f"Your Leave Balances:\n{balance_str}")
                session.reset()
            elif "faq" in choice:
                await self.sender.text(phone, "Ask me anything about HR (e.g., salary, insurance, policy).")
                session.step = "faq_branch"
            else:
                await self.sender.text(phone, "Invalid choice. Please select from the buttons.")
                
        elif session.step == "ask_leave_type":
            session.data["leave_type"] = text
            await self.sender.text(phone, "Enter start date (YYYY-MM-DD):")
            session.step = "ask_from"
            
        elif session.step == "ask_from":
            session.data["from"] = text
            await self.sender.text(phone, "Enter end date (YYYY-MM-DD):")
            session.step = "ask_to"
            
        elif session.step == "ask_to":
            session.data["to"] = text
            ref = "LV-" + "".join(random.choices(string.digits, k=5))
            await self.sender.text(phone, f"Leave application submitted! Ref: {ref}")
            session.reset()
            
        elif session.step == "faq_branch":
            query = text.lower()
            found = False
            for k, v in HR_FAQ.items():
                if k in query:
                    await self.sender.text(phone, v)
                    found = True
                    break
            if not found:
                await self.sender.text(phone, "I don't have information on that HR topic. Contact hr@example.com.")
            session.reset()
