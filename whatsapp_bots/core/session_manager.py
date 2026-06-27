import time
import asyncio
from typing import Dict, Any, Optional
from whatsapp_bots.config.settings import settings
import motor.motor_asyncio

class Session:
    def __init__(self, phone: str):
        self.phone = phone
        self.bot: str = "faq_bot"
        self.step: str = "start"
        self.data: Dict[str, Any] = {}
        self.last_activity: float = time.time()

    def reset(self):
        self.step = "start"
        self.data = {}
        self.last_activity = time.time()

class SessionManager:
    SESSION_TTL = 1800  # 30 minutes

    def __init__(self):
        # In-memory session cache
        self.sessions: Dict[str, Session] = {}
        # Initialize MongoDB client for persistence (if URI is provided)
        if settings.MONGODB_URI:
            self.mongo_client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGODB_URI)
            # Use the default database from the connection string or fallback to "whatsapp_bots"
            try:
                self.mongo_db = self.mongo_client.get_default_database()
            except Exception:
                # If no default DB is specified, use a named DB
                self.mongo_db = self.mongo_client["whatsapp_bots"]
            self.mongo_collection = self.mongo_db["sessions"]
        else:
            self.mongo_client = None
            self.mongo_db = None
            self.mongo_collection = None

    def get(self, phone: str) -> Session:
        now = time.time()
        if phone in self.sessions:
            session = self.sessions[phone]
            if now - session.last_activity > self.SESSION_TTL:
                session.reset()
            session.last_activity = now
            return session
        
        session = Session(phone)
        self.sessions[phone] = session
        return session

    def clear(self, phone: str):
        if phone in self.sessions:
            del self.sessions[phone]
        # Also remove from MongoDB if persistence is enabled
        if self.mongo_collection:
            # Fire-and-forget deletion; schedule in background
            async def _delete():
                await self.mongo_collection.delete_one({"phone": phone})
            asyncio.create_task(_delete())

    def set_bot(self, phone: str, bot_name: str):
        session = self.get(phone)
        session.bot = bot_name
        session.reset()

    # ---------------------------------------------------------------------
    # Persistence helpers (MongoDB)
    # ---------------------------------------------------------------------
    async def save_to_db(self, session: Session) -> None:
        """Upsert the session document into MongoDB.

        The document schema follows the specification:
        {
            "phone": <str>,
            "bot": <str>,
            "step": <str>,
            "data": <dict>,
            "last_activity": <float>,
            "updated_at": <float>
        }
        """
        if not self.mongo_collection:
            return
        doc = {
            "phone": session.phone,
            "bot": session.bot,
            "step": session.step,
            "data": session.data,
            "last_activity": session.last_activity,
            "updated_at": time.time(),
        }
        await self.mongo_collection.update_one({"phone": session.phone}, {"$set": doc}, upsert=True)

    async def load_from_db(self, phone: str) -> Optional[Session]:
        """Load a session from MongoDB by phone number.

        Returns a ``Session`` instance if found, otherwise ``None``.
        """
        if not self.mongo_collection:
            return None
        doc = await self.mongo_collection.find_one({"phone": phone})
        if not doc:
            return None
        session = Session(phone)
        session.bot = doc.get("bot", "faq_bot")
        session.step = doc.get("step", "start")
        session.data = doc.get("data", {})
        session.last_activity = doc.get("last_activity", time.time())
        # Cache the loaded session in memory for faster subsequent access
        self.sessions[phone] = session
        return session
