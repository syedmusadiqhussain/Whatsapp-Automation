"""Compatibility shim for ``core.sender``.

The real implementation lives in ``whatsapp_bots.core.sender``.  The test suite
and the application import ``core.sender`` directly, so we provide a thin
wrapper that re‑exports the original ``Sender`` class.
"""

from whatsapp_bots.core.sender import Sender

__all__ = ["Sender"]
