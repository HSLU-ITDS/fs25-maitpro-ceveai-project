from abc import ABC, abstractmethod
import os
from typing import List, Dict, Any
from openai import OpenAI
import google.generativeai as genai

class BaseLLMService(ABC):
    """Base class for LLM services"""
    
    @abstractmethod
    def generate_response(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate a response from the LLM"""
        pass

class OpenAIService(BaseLLMService):
    """OpenAI implementation of the LLM service"""


    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)
    
    def generate_response(self, messages: List[Dict[str, str]], **kwargs) -> str:
        response = self.client.chat.completions.create(
            model=kwargs.get("model", "gpt-3.5-turbo"),
            messages=messages,
            **kwargs
        )
        return response.choices[0].message.content

class GeminiService(BaseLLMService):
    """Google Gemini implementation of the LLM service"""
    
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def generate_response(self, messages: List[Dict[str, str]], **kwargs) -> str:
        # Convert OpenAI message format to Gemini format
        prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])
        response = self.model.generate_content(prompt)
        return response.text

def get_llm_service() -> BaseLLMService:
    """Factory function to get the appropriate LLM service based on available API keys"""
    
    provider = os.getenv("PROVIDER")


    if provider == "openai":
        return OpenAIService()
    elif provider == "google":
        return GeminiService()
    else:
        raise ValueError("No API keys found. Please set either OPENAI_API_KEY or GOOGLE_API_KEY in your .env file") 
    
    #if openai_key:
    #    return OpenAIService(openai_key)
    #elif gemini_key:
    #    return GeminiService(gemini_key)
    #else:
    #    raise ValueError("No API keys found. Please set either OPENAI_API_KEY or GOOGLE_API_KEY in your .env file") 