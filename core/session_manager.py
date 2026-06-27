"""Compatibility shim for ``core.session_manager``.

The original project stores the session manager implementation in
``whatsapp_bots/core/session_manager.py``.  The test suite (and the ``app``
module) import it using a top‑level ``core`` package, e.g. ``from core.session_manager
import SessionManager``.  To keep the existing import statements unchanged we
re‑export the concrete classes from the actual location.
"""

from whatsapp_bots.core.session_manager import Session, SessionManager

__all__ = ["Session", "SessionManager"]
