import os
from abc import ABC, abstractmethod
from typing import List, Dict

class ChatClient(ABC):
    @abstractmethod
    def get_response(self, model: str, messages: List[Dict[str, str]]) -> str:
        pass