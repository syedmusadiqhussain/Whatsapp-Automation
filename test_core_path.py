import sys
import os
sys.path.insert(0, '.')
print("Before import, sys.path contains whatsapp_bots?", any('whatsapp_bots' in p for p in sys.path))
import core
print("core.__path__:", core.__path__)
print("core.__file__:", core.__file__)
print("sys.path after core import:", [p for p in sys.path if 'WhatsApp' in p or 'whatsapp' in p])
