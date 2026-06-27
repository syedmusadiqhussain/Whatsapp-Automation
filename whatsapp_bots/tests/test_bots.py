import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from core.session_manager import SessionManager, Session
from bots.lead_bot import LeadBot
from bots.support_bot import SupportBot
from bots.order_bot import OrderBot
from bots.booking_bot import BookingBot
from bots.faq_bot import FAQBot
from bots.payment_bot import PaymentBot
from bots.feedback_bot import FeedbackBot
from bots.onboarding_bot import OnboardingBot
from bots.hr_bot import HRBot

# Helpers
def make_session(phone="1234567890"):
    return Session(phone)

def make_sender():
    sender = MagicMock()
    sender.text = AsyncMock()
    sender.buttons = AsyncMock()
    sender.list_message = AsyncMock()
    sender.template = AsyncMock()
    return sender

@pytest.mark.asyncio
async def test_lead_bot_start():
    sender = make_sender()
    session_manager = SessionManager()
    bot = LeadBot(sender, session_manager)
    session = make_session()
    
    await bot.handle(session.phone, "interested", {}, session)
    sender.text.assert_called_with(session.phone, "Welcome! Let's get you started. What is your full name?")
    assert session.step == "ask_name"

@pytest.mark.asyncio
async def test_lead_bot_full_flow():
    sender = make_sender()
    session_manager = SessionManager()
    bot = LeadBot(sender, session_manager)
    session = make_session()
    
    await bot.handle(session.phone, "interested", {}, session)
    await bot.handle(session.phone, "John Doe", {}, session)
    await bot.handle(session.phone, "john@example.com", {}, session)
    await bot.handle(session.phone, "SaaS Platform", {}, session)
    
    assert session.step == "start" # Reset after done
    assert sender.text.call_count == 3
    assert sender.buttons.call_count == 1

@pytest.mark.asyncio
async def test_support_bot_start():
    sender = make_sender()
    bot = SupportBot(sender, SessionManager())
    session = make_session()
    
    await bot.handle(session.phone, "issue", {}, session)
    sender.text.assert_called_with(session.phone, "I'm here to help. Please provide your Order ID.")
    assert session.step == "ask_order"

@pytest.mark.asyncio
async def test_support_bot_ticket_created():
    sender = make_sender()
    bot = SupportBot(sender, SessionManager())
    session = make_session()
    
    await bot.handle(session.phone, "issue", {}, session)
    await bot.handle(session.phone, "ORD-123", {}, session)
    await bot.handle(session.phone, "Lost Package", {}, session)
    
    assert session.step == "start"
    last_call = sender.text.call_args[0][1]
    assert "Support ticket created!" in last_call
    assert "TKT-" in last_call

@pytest.mark.asyncio
async def test_order_bot_found():
    sender = make_sender()
    bot = OrderBot(sender, SessionManager())
    session = make_session()
    
    await bot.handle(session.phone, "track", {}, session)
    await bot.handle(session.phone, "ORD-123", {}, session)
    
    assert session.step == "ask_action"
    args = sender.buttons.call_args[0]
    assert "In Transit" in args[1]

@pytest.mark.asyncio
async def test_order_bot_not_found():
    sender = make_sender()
    bot = OrderBot(sender, SessionManager())
    session = make_session()
    
    await bot.handle(session.phone, "track", {}, session)
    await bot.handle(session.phone, "ORD-999", {}, session)
    
    assert session.step == "ask_order"
    sender.text.assert_called_with(session.phone, "Order not found. Please check the ID and try again.")

@pytest.mark.asyncio
async def test_booking_bot_start():
    sender = make_sender()
    bot = BookingBot(sender, SessionManager())
    session = make_session()
    
    await bot.handle(session.phone, "book", {}, session)
    sender.buttons.assert_called()
    assert session.step == "ask_service"

@pytest.mark.asyncio
async def test_faq_bot_known_question():
    sender = make_sender()
    bot = FAQBot(sender, SessionManager())
    session = make_session()
    
    await bot.handle(session.phone, "What is your pricing?", {}, session)
    sender.text.assert_called_with(session.phone, "Our plans start at $29/month. Check our website for details.")

@pytest.mark.asyncio
async def test_faq_bot_unknown_question():
    sender = make_sender()
    bot = FAQBot(sender, SessionManager())
    session = make_session()
    
    with patch("bots.faq_bot.llm_client.chat_completion", new_callable=AsyncMock) as mock_llm:
        mock_llm.return_value = "This is an AI response."
        await bot.handle(session.phone, "Who is the CEO?", {}, session)
        sender.text.assert_called_with(session.phone, "This is an AI response.")

@pytest.mark.asyncio
async def test_payment_bot_found():
    sender = make_sender()
    bot = PaymentBot(sender, SessionManager())
    session = make_session()
    
    await bot.handle(session.phone, "pay", {}, session)
    await bot.handle(session.phone, "INV-001", {}, session)
    
    assert session.step == "show_payment"
    assert "https://stripe.com/pay/INV-001" in sender.buttons.call_args[0][1]

@pytest.mark.asyncio
async def test_payment_bot_already_paid():
    sender = make_sender()
    bot = PaymentBot(sender, SessionManager())
    session = make_session()
    
    await bot.handle(session.phone, "pay", {}, session)
    await bot.handle(session.phone, "INV-003", {}, session)
    
    assert session.step == "start"
    assert "already paid" in sender.text.call_args[0][1]

@pytest.mark.asyncio
async def test_feedback_bot_rating():
    sender = make_sender()
    bot = FeedbackBot(sender, SessionManager())
    session = make_session()
    
    await bot.handle(session.phone, "feedback", {}, session)
    await bot.handle(session.phone, "5", {}, session)
    
    assert session.step == "ask_comment"
    assert session.data["rating"] == 5

@pytest.mark.asyncio
async def test_feedback_bot_invalid_rating():
    sender = make_sender()
    bot = FeedbackBot(sender, SessionManager())
    session = make_session()
    
    await bot.handle(session.phone, "feedback", {}, session)
    await bot.handle(session.phone, "6", {}, session)
    
    assert session.step == "ask_rating"
    assert "valid rating" in sender.text.call_args[0][1]

@pytest.mark.asyncio
async def test_onboarding_full_flow():
    sender = make_sender()
    bot = OnboardingBot(sender, SessionManager())
    session = make_session()
    
    await bot.handle(session.phone, "register", {}, session)
    await bot.handle(session.phone, "Alice", {}, session)
    await bot.handle(session.phone, "alice@example.com", {}, session)
    await bot.handle(session.phone, "London", {}, session)
    await bot.handle(session.phone, "Both", {}, session)
    
    assert session.step == "start"
    assert "Registration complete" in sender.text.call_args[0][1]

@pytest.mark.asyncio
async def test_hr_bot_leave_balance():
    sender = make_sender()
    bot = HRBot(sender, SessionManager())
    session = make_session()
    
    await bot.handle(session.phone, "hr", {}, session)
    await bot.handle(session.phone, "Check Balance", {}, session)
    
    assert session.step == "start"
    assert "Annual: 15 days" in sender.text.call_args[0][1]

@pytest.mark.asyncio
async def test_hr_bot_faq_salary():
    sender = make_sender()
    bot = HRBot(sender, SessionManager())
    session = make_session()
    
    await bot.handle(session.phone, "hr", {}, session)
    await bot.handle(session.phone, "HR FAQ", {}, session)
    await bot.handle(session.phone, "When is salary credited?", {}, session)
    
    assert session.step == "start"
    assert "last working day" in sender.text.call_args[0][1]
