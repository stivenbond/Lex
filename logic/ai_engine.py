import requests
import json

class AIEngine:
    def __init__(self, base_url="http://localhost:11434"):
        self.base_url = base_url
        self.model = "llama3" # Default model

    def generate(self, prompt, model=None):
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": model or self.model,
            "prompt": prompt,
            "stream": False
        }
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json().get("response", "")
        except requests.exceptions.RequestException as e:
            # Fallback for when Ollama is not running (Mocking for dev)
            print(f"Warning: Could not connect to Ollama at {self.base_url}. Error: {e}")
            return f"[MOCK AI RESPONSE] Generated answer for prompt: '{prompt[:30]}...'"

    def check_connection(self):
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            return response.status_code == 200
        except:
            return False
