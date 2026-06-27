import sys
import os

# Add the project root to sys.path
sys.path.append(os.getcwd())

try:
    from config.settings import settings
    print("Configuration Mapping: SUCCESS")
    print(f"Loaded ENV: {settings.ENV}")
    print(f"Loaded META_APP_ID: {settings.META_APP_ID}")
    # Verify all required fields are present
    required_fields = [
        "META_APP_ID", "META_APP_SECRET", "META_VERIFY_TOKEN", 
        "META_ACCESS_TOKEN", "META_PHONE_NUMBER_ID"
    ]
    for field in required_fields:
        val = getattr(settings, field)
        if not val:
            print(f"Mapping Warning: {field} is empty!")
except Exception as e:
    print(f"Configuration Mapping: FAILED")
    print(f"Error: {e}")
