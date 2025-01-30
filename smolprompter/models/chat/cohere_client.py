from typing import Dict, List
import cohere
from .base import ChatClient

class CohereClient(ChatClient):
    def __init__(self, api_key: str = None):
        self.client = cohere.ClientV2(api_key=api_key)
    
    def get_response(self, user_msg: str, model_name: str) -> str:
        response = self.client.chat(
            model=model_name,
            messages=[{"role": "user", "content": user_msg}]
        )
        
        text_response = response.message.content[0].text
        
        return text_response