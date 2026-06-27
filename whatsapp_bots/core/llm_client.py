import httpx
from whatsapp_bots.config.settings import settings

class LLMClient:
    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY
        self.base_url = settings.OPENROUTER_BASE_URL
        self.default_model = settings.DEFAULT_MODEL
        self.fallback_model = settings.FALLBACK_MODEL
        
        # OpenRouter required headers
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/SyedMusadiq/whatsapp-chatbot-suite", # Required by OpenRouter
            "X-Title": "WhatsApp Chatbot Suite" # Required by OpenRouter
        }

    async def chat_completion(self, messages: list, model: str = None):
        model = model or self.default_model
        payload = {
            "model": model,
            "messages": messages
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=self.headers,
                    json=payload,
                    timeout=30.0
                )
                
                if response.status_code != 200:
                    print(f"LLM Error ({response.status_code}): {response.text}")
                    # Simple fallback logic
                    if model != self.fallback_model:
                        print(f"Attempting fallback to {self.fallback_model}...")
                        return await self.chat_completion(messages, model=self.fallback_model)
                    return None

                data = response.json()
                return data['choices'][0]['message']['content']
            
            except Exception as e:
                print(f"LLM Exception: {e}")
                if model != self.fallback_model:
                    print(f"Attempting fallback to {self.fallback_model}...")
                    return await self.chat_completion(messages, model=self.fallback_model)
                return None

llm_client = LLMClient()
