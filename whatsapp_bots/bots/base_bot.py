from abc import ABC, abstractmethod
from whatsapp_bots.core.sender import Sender
from whatsapp_bots.core.session_manager import SessionManager, Session

class BaseBot(ABC):
    def __init__(self, sender: Sender, session_manager: SessionManager):
        self.sender = sender
        self.session_manager = session_manager

    @abstractmethod
    async def handle(self, phone: str, text: str, msg: dict, session: Session) -> None:
        pass
