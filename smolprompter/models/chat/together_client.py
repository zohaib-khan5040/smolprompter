from typing import Dict, List
from openai import OpenAI
from .base import ChatClient

class OpenAIClient(ChatClient):
    def __init__(self, api_key: str = None):
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.together.xyz/v1"
        )
    
    def get_response(self, model: str, messages: List[Dict[str, str]], **kwargs) -> str:
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            **kwargs
        )
        response_content = response.choices[0].messages.content
        return {
            "content": response_content
        }