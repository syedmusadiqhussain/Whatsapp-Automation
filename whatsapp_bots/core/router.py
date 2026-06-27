from whatsapp_bots.core.sender import Sender
from whatsapp_bots.core.session_manager import SessionManager, Session
from whatsapp_bots.bots.lead_bot import LeadBot
from whatsapp_bots.bots.support_bot import SupportBot
from whatsapp_bots.bots.order_bot import OrderBot
from whatsapp_bots.bots.booking_bot import BookingBot
from whatsapp_bots.bots.faq_bot import FAQBot
from whatsapp_bots.bots.payment_bot import PaymentBot
from whatsapp_bots.bots.feedback_bot import FeedbackBot
from whatsapp_bots.bots.onboarding_bot import OnboardingBot
from whatsapp_bots.bots.notify_bot import NotifyBot
from whatsapp_bots.bots.hr_bot import HRBot

TRIGGER_KEYWORDS = {
    "interested": "lead_bot",
    "enquire": "lead_bot",
    "problem": "support_bot",
    "issue": "support_bot",
    "track": "order_bot",
    "order": "order_bot",
    "book": "booking_bot",
    "appointment": "booking_bot",
    "pay": "payment_bot",
    "invoice": "payment_bot",
    "feedback": "feedback_bot",
    "register": "onboarding_bot",
    "signup": "onboarding_bot",
    "leave": "hr_bot",
    "hr": "hr_bot"
}

class Router:
    def __init__(self, sender: Sender, session_manager: SessionManager):
        self.sender = sender
        self.session_manager = session_manager
        
        # Instantiate all bots
        self.bots = {
            "lead_bot": LeadBot(sender, session_manager),
            "support_bot": SupportBot(sender, session_manager),
            "order_bot": OrderBot(sender, session_manager),
            "booking_bot": BookingBot(sender, session_manager),
            "faq_bot": FAQBot(sender, session_manager),
            "payment_bot": PaymentBot(sender, session_manager),
            "feedback_bot": FeedbackBot(sender, session_manager),
            "onboarding_bot": OnboardingBot(sender, session_manager),
            "notify_bot": NotifyBot(sender, session_manager),
            "hr_bot": HRBot(sender, session_manager)
        }

    async def route(self, phone: str, text: str, msg: dict) -> None:
        session = self.session_manager.get(phone)
        lower_text = text.lower().strip()

        # Handle Menu/Start
        if lower_text in ["hi", "hello", "start", "menu"]:
            session.reset()
            sections = [
                {
                    "title": "Main Menu",
                    "rows": [
                        {"id": "lead", "title": "Inquiry", "description": "Business Enquiry"},
                        {"id": "support", "title": "Support", "description": "Report an issue"},
                        {"id": "order", "title": "Track", "description": "Track your order"},
                        {"id": "booking", "title": "Book", "description": "Schedule appointment"},
                        {"id": "payment", "title": "Pay", "description": "Pay an invoice"},
                        {"id": "feedback", "title": "Feedback", "description": "Rate our service"},
                        {"id": "onboarding", "title": "Register", "description": "New user signup"},
                        {"id": "hr", "title": "HR", "description": "Employee services"},
                        {"id": "faq", "title": "FAQ", "description": "General questions"}
                    ]
                }
            ]
            await self.sender.list_message(phone, "How can I help you today?", "Select Option", sections)
            return

        # Handle Cancel
        if lower_text in ["stop", "cancel"]:
            session.reset()
            await self.sender.text(phone, "Operation cancelled. Type 'menu' to start over.")
            return

        # Route by keyword if session is at 'start'
        if session.step == "start":
            for keyword, bot_name in TRIGGER_KEYWORDS.items():
                if keyword in lower_text:
                    session.bot = bot_name
                    break
            else:
                # Default to FAQ bot if no keyword matches
                session.bot = "faq_bot"

        # Dispatch to the assigned bot
        bot = self.bots.get(session.bot, self.bots["faq_bot"])
        await bot.handle(phone, text, msg, session)
