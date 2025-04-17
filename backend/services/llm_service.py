from abc import ABC, abstractmethod
import os
from typing import List, Dict, Any
from openai import OpenAI
import google.generativeai as genai

class BaseLLMService(ABC):
    """Base class for LLM services"""
    
    @abstractmethod
    async def generate_response(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate a response from the LLM"""
        pass
    
    @abstractmethod
    async def generate_vision(self, messages: List[Dict[str, Any]], **kwargs) -> str:
        """Generate a response from the LLM for vision tasks"""
        pass

class OpenAIService(BaseLLMService):
    """OpenAI implementation of the LLM service"""
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)
    
    async def generate_response(self, messages: List[Dict[str, str]], **kwargs) -> str:
        response = self.client.chat.completions.create(
            model=kwargs.get("model", "gpt-3.5-turbo"),
            messages=messages,
            **kwargs
        )
        return response.choices[0].message.content
    
    async def generate_vision(self, messages: List[Dict[str, Any]], **kwargs) -> str:
        response = self.client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=messages,
            max_tokens=4096,
            **kwargs
        )
        return response.choices[0].message.content

class GeminiService(BaseLLMService):
    """Google Gemini implementation of the LLM service"""
    
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=api_key)
        self.chat_model = genai.GenerativeModel('gemini-1.5-flash')
        self.vision_model = genai.GenerativeModel('gemini-1.5-flash')
    
    async def generate_response(self, messages: List[Dict[str, str]], **kwargs) -> str:
        # Convert OpenAI message format to Gemini format
        prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])
        response = self.chat_model.generate_content(prompt)
        return response.text
    
    async def generate_vision(self, messages: List[Dict[str, Any]], **kwargs) -> str:
        # Extract the system prompt and user content
        system_prompt = next((msg["content"] for msg in messages if msg["role"] == "system"), "")
        user_message = next((msg for msg in messages if msg["role"] == "user"), None)
        
        if not user_message:
            raise ValueError("No user message found in the messages list")
            
        # Combine text parts and image parts for Gemini
        text_parts = []
        image_parts = []
        
        for content in user_message["content"]:
            if content["type"] == "text":
                text_parts.append(content["text"])
            elif content["type"] == "image_url":
                # For Gemini, we need to extract the base64 data from the URL
                url = content["image_url"]["url"]
                if url.startswith("data:"):
                    # Extract mime type and base64 data
                    mime_type = url.split(";")[0].split(":")[1]
                    base64_data = url.split("base64,")[1] if "base64," in url else url.split("base64,")[0]
                    image_parts.append({"mime_type": mime_type, "data": base64_data})
        
        # Combine system prompt and user text
        prompt = f"{system_prompt}\n{''.join(text_parts)}"
        
        # Generate response using vision model
        response = self.vision_model.generate_content(
            contents=[prompt, *image_parts],
            **kwargs
        )
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