import os
import re
import asyncio
import httpx
from pymongo import MongoClient
from redis import Redis
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class Diagnostics:
    def __init__(self):
        self.results = {}
        self.errors = {}

    def check_syntax(self):
        print("Checking .env syntax...")
        try:
            with open(".env", "r") as f:
                lines = f.readlines()
                for i, line in enumerate(lines):
                    line = line.strip()
                    if line and not line.startswith("#") and "=" not in line:
                        raise ValueError(f"Syntax error at line {i+1}: '{line}' (missing '=')")
            self.results["Syntax Check"] = "PASSED"
        except Exception as e:
            self.results["Syntax Check"] = "FAILED"
            self.errors["Syntax Check"] = str(e)

    def validate_api_formats(self):
        print("Validating API key formats...")
        patterns = {
            "META_ACCESS_TOKEN": r"^EA[A-Za-z0-9]+$",
            "STRIPE_SECRET_KEY": r"^sk_(test|live)_[a-zA-Z0-9]+$",
            "HUBSPOT_API_KEY": r"^[a-zA-Z0-9\-_]+$"
        }
        
        for key, pattern in patterns.items():
            value = os.getenv(key)
            if not value:
                self.results[f"{key} Format"] = "MISSING"
            elif re.match(pattern, value):
                self.results[f"{key} Format"] = "PASSED"
            else:
                self.results[f"{key} Format"] = "FAILED"
                self.errors[f"{key} Format"] = f"Value '{value[:10]}...' does not match expected pattern."

    def test_mongodb(self):
        print("Testing MongoDB connection...")
        uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
        try:
            # For mongodb+srv://, the client handles the connection string automatically
            client = MongoClient(uri, serverSelectionTimeoutMS=5000)
            client.admin.command('ping')
            self.results["MongoDB"] = "CONNECTED"
        except Exception as e:
            self.results["MongoDB"] = "FAILED"
            self.errors["MongoDB"] = str(e)

    async def test_redis(self):
        print("Testing Redis (Upstash REST) connection...")
        url = os.getenv("UPSTASH_REDIS_REST_URL")
        token = os.getenv("UPSTASH_REDIS_REST_TOKEN")
        
        if not url or not token:
            self.results["Redis"] = "FAILED"
            self.errors["Redis"] = "Upstash REST URL or Token missing."
            return

        headers = {"Authorization": f"Bearer {token}"}
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{url}/ping", headers=headers, timeout=5.0)
                if response.status_code == 200 and response.json().get("result") == "PONG":
                    self.results["Redis"] = "CONNECTED"
                else:
                    self.results["Redis"] = "FAILED"
                    self.errors["Redis"] = f"HTTP {response.status_code}: {response.text}"
            except Exception as e:
                self.results["Redis"] = "FAILED"
                self.errors["Redis"] = str(e)

    async def test_openrouter(self):
        print("Testing OpenRouter API...")
        api_key = os.getenv("OPENROUTER_API_KEY")
        base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        
        if not api_key or "your_openrouter_key" in api_key:
            self.results["OpenRouter"] = "FAILED"
            self.errors["OpenRouter"] = "API Key is missing or using placeholder."
            return

        headers = {
            "Authorization": f"Bearer {api_key}",
            "HTTP-Referer": "https://github.com/SyedMusadiq/whatsapp-chatbot-suite",
            "X-Title": "Diagnostic Test"
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{base_url}/models", headers=headers, timeout=5.0)
                if response.status_code == 200:
                    self.results["OpenRouter"] = "CONNECTED"
                else:
                    self.results["OpenRouter"] = "FAILED"
                    self.errors["OpenRouter"] = f"HTTP {response.status_code}: {response.text}"
            except Exception as e:
                self.results["OpenRouter"] = "FAILED"
                self.errors["OpenRouter"] = str(e)

    def run_all(self):
        self.check_syntax()
        self.validate_api_formats()
        self.test_mongodb()
        asyncio.run(self.test_redis())
        asyncio.run(self.test_openrouter())
        
        print("\n" + "="*40)
        print("DIAGNOSTIC REPORT")
        print("="*40)
        for service, status in self.results.items():
            print(f"{service:25}: {status}")
            if status == "FAILED" or status == "MISSING":
                print(f"  Error: {self.errors.get(service, 'Unknown error')}")
        print("="*40)

if __name__ == "__main__":
    diag = Diagnostics()
    diag.run_all()
