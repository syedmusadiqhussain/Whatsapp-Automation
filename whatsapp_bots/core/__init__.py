"""Package initializer for the ``core`` modules.

The original project placed the core utilities (``session_manager``, ``sender``,
``router`` and ``llm_client``) inside ``whatsapp_bots/core`` but the test suite
imports them using a top‑level ``core`` package (e.g. ``from core.session_manager
import SessionManager``).  When ``pytest`` runs, the ``whatsapp_bots`` directory
is added to ``sys.path`` before the repository root, so a ``core`` package that
exists directly under ``whatsapp_bots`` will be discovered first.  Adding this
``__init__`` file turns the directory into a proper package, allowing the test
imports to resolve correctly without modifying the test code.

The file does not need to expose any symbols; the submodules are imported on
demand.  An ``__all__`` list is provided for clarity.
"""

__all__ = [
    "session_manager",
    "sender",
    "router",
    "llm_client",
]
