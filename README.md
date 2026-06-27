# WhatsApp Chatbot Suite

A complete, production-ready WhatsApp chatbot suite with 10 specialized bots built using FastAPI.

## Features

- **10 Specialized Bots**:
  - 📝 **Lead Bot**: Collect customer information and generate leads
  - 🛟 **Support Bot**: Handle customer support inquiries and create tickets
  - 📦 **Order Bot**: Track orders and provide order status updates
  - 📅 **Booking Bot**: Schedule appointments and bookings
  - ❓ **FAQ Bot**: Answer frequently asked questions (with LLM fallback)
  - 💳 **Payment Bot**: Process payments and send invoices
  - ⭐ **Feedback Bot**: Collect customer feedback and ratings
  - 🚀 **Onboarding Bot**: Guide new users through the setup process
  - 📢 **Notify Bot**: Send broadcast notifications to users
  - 💼 **HR Bot**: Handle employee leave requests and HR inquiries

- **Core Features**:
  - FastAPI backend with automatic API docs
  - Session management with optional MongoDB persistence
  - LLM integration via OpenRouter (Google Gemini, DeepSeek, etc.)
  - Webhook integration for Meta WhatsApp Business API
  - CORS enabled for frontend integration

## Project Structure

```
WhatsApp chatbot development guide/
├── core/                          # Compatibility shim
│   ├── __init__.py
│   ├── sender.py
│   └── session_manager.py
├── whatsapp_bots/                 # Main application
│   ├── __pycache__/
│   ├── .env.example               # Environment variables template
│   ├── app.py                     # FastAPI entry point
│   ├── bots/                      # Bot implementations
│   │   ├── __init__.py
│   │   ├── base_bot.py            # Base bot class
│   │   ├── booking_bot.py
│   │   ├── faq_bot.py
│   │   ├── feedback_bot.py
│   │   ├── hr_bot.py
│   │   ├── lead_bot.py
│   │   ├── notify_bot.py
│   │   ├── onboarding_bot.py
│   │   ├── order_bot.py
│   │   ├── payment_bot.py
│   │   └── support_bot.py
│   ├── config/                    # Configuration
│   │   ├── __init__.py
│   │   └── settings.py
│   ├── core/                      # Core modules
│   │   ├── __init__.py
│   │   ├── llm_client.py
│   │   ├── router.py
│   │   ├── sender.py
│   │   └── session_manager.py
│   ├── tests/                     # Test files
│   │   ├── __pycache__/
│   │   └── test_bots.py
│   ├── config_check.py
│   ├── diagnostics.py
│   └── requirements.txt
└── .gitignore
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/syedmusadiqhussain/Whatsapp-Automation.git
   cd Whatsapp-Automation
   ```

2. **Create and activate a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   cd whatsapp_bots
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   - Copy the `.env.example` file to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Edit the `.env` file and fill in your actual credentials (see Configuration section below)

## Configuration

The application uses the following environment variables (configure in `.env`):

| Variable | Description | Example |
|----------|-------------|---------|
| `ENV` | Environment mode | `development` or `production` |
| `PORT` | Server port | `3000` |
| `META_APP_ID` | Meta App ID | Your Meta App ID |
| `META_APP_SECRET` | Meta App Secret | Your Meta App Secret |
| `META_VERIFY_TOKEN` | Webhook verification token | Choose any string |
| `META_ACCESS_TOKEN` | Meta API access token | Your access token |
| `META_PHONE_NUMBER_ID` | WhatsApp Phone Number ID | Your phone number ID |
| `META_API_URL` | Meta Graph API URL | `https://graph.facebook.com/v19.0` |
| `MONGODB_URI` | (Optional) MongoDB connection string | Leave empty for in-memory |
| `REDIS_URL` | (Optional) Redis connection URL | Leave empty |
| `OPENROUTER_API_KEY` | OpenRouter API key for LLM | Your OpenRouter key |
| `OPENROUTER_BASE_URL` | OpenRouter base URL | `https://openrouter.ai/api/v1` |
| `DEFAULT_MODEL` | Default LLM model | `google/gemini-2.0-flash-exp:free` |
| `FALLBACK_MODEL` | Fallback LLM model | `deepseek/deepseek-r1:free` |
| `HUBSPOT_API_KEY` | (Optional) HubSpot API key | Your HubSpot key |
| `STRIPE_SECRET_KEY` | (Optional) Stripe secret key | Your Stripe key |
| `SMTP_HOST` | (Optional) SMTP host | `smtp.gmail.com` |
| `SMTP_PORT` | (Optional) SMTP port | `587` |
| `SMTP_USER` | (Optional) SMTP username | Your email |
| `SMTP_PASS` | (Optional) SMTP password | Your app password |

## Running the Application

### Development Mode

```bash
# From the project root directory:
python -m whatsapp_bots.app
```

Or with Uvicorn directly:

```bash
cd whatsapp_bots
uvicorn app:app --reload --host 0.0.0.0 --port 3000
```

### Production Mode

```bash
cd whatsapp_bots
uvicorn app:app --host 0.0.0.0 --port 3000 --workers 4
```

## API Documentation

Once the server is running, you can access the API documentation at:

- **Swagger UI**: http://localhost:3000/docs
- **ReDoc**: http://localhost:3000/redoc
- **Health check**: http://localhost:3000/health

## Webhook Setup

To receive messages from WhatsApp, you need to set up a webhook in your Meta for Developers dashboard:

1. Go to your Meta App dashboard
2. Navigate to WhatsApp > Configuration
3. Under Webhooks, click "Edit"
4. Set the **Callback URL** to your server's public URL + `/webhook` (e.g., `https://your-domain.com/webhook`)
5. Set the **Verify Token** to the same value as your `META_VERIFY_TOKEN` in `.env`
6. Verify and save the webhook
7. Subscribe to the `messages` webhook field

## Usage

Users can interact with the chatbot using natural language or by selecting options from the menu.

### Main Menu
Send "hi", "hello", "start", or "menu" to see the main menu with all available bots.

### Trigger Keywords
Each bot can also be triggered directly using keywords:
- "interested", "enquire" → Lead Bot
- "problem", "issue" → Support Bot
- "track", "order" → Order Bot
- "book", "appointment" → Booking Bot
- "pay", "invoice" → Payment Bot
- "feedback" → Feedback Bot
- "register", "signup" → Onboarding Bot
- "leave", "hr" → HR Bot

### Cancel/Reset
Send "stop" or "cancel" to reset the conversation.

## Running Tests

To run the test suite:

```bash
cd whatsapp_bots
pytest tests/ -v
```

## Technologies Used

- **FastAPI**: Modern, fast web framework for building APIs
- **Uvicorn**: ASGI server for running the application
- **Pydantic**: Data validation using Python type annotations
- **Motor**: Async MongoDB driver
- **Redis**: In-memory data structure store (optional)
- **OpenRouter**: LLM API gateway for accessing multiple models
- **httpx**: Async HTTP client for API calls
- **Pytest**: Testing framework

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
