"""Top-level ``core`` package shim.

The original project places the core modules (``session_manager``, ``sender``,
``router`` and ``llm_client``) inside the ``whatsapp_bots/core`` package.  The
application code and the test suite import these modules using the top‑level
``core`` package name, e.g. ``from core.session_manager import SessionManager``.

When the project is executed from the repository root, Python's import system
does not find a top‑level ``core`` package because the directory hierarchy is
``whatsapp_bots/core``.  To maintain compatibility without altering the source
files, we provide a lightweight shim package named ``core`` at the repository
root.  The shim extends its ``__path__`` to include the actual core package
location, effectively making ``core`` a namespace that forwards imports to
``whatsapp_bots.core``.

This approach avoids duplicating the core modules and ensures that both the
application (``app.py``) and the test suite can import ``core.*`` successfully.
"""

import os
import sys

# Resolve the absolute path to the repository root (the directory containing this file).
_repo_root = os.path.abspath(os.path.dirname(__file__))

# Path to the real core package inside ``whatsapp_bots``.
_inner_core_path = os.path.join(_repo_root, "whatsapp_bots", "core")

if os.path.isdir(_inner_core_path):
    __path__.insert(0, _inner_core_path)

_whatsapp_path = os.path.join(_repo_root, "whatsapp_bots")
if _whatsapp_path not in sys.path:
    sys.path.insert(0, _whatsapp_path)

# The shim does not expose any symbols directly; submodules are imported on
# demand from the underlying package.
