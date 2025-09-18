from adapters.llm.base import register
import requests

@register("ollama")
class OllamaLLM:
    def __init__(self, endpoint: str, model: str, options: dict|None=None):
        self.endpoint = endpoint.rstrip("/")
        self.model = model
        self.options = options or {}

    def generate(self, prompt: str, **opts) -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {**self.options, **opts},
        }
        r = requests.post(self.endpoint, json=payload, timeout=600)
        r.raise_for_status()
        js = r.json()
        return js.get("response") or js.get("message") or str(js)
