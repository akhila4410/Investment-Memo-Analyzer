import os
import requests
from typing import Optional, List
from pydantic import BaseModel, model_validator
from langchain.llms.base import LLM

class GroqLLM(LLM, BaseModel):
    model: str = "llama3-8b-8192"
    temperature: float = 0.1
    groq_api_key: Optional[str] = "GROQ_API_KEY "

    @model_validator(mode="after")
    def check_api_key(self):
        if not self.groq_api_key:
            raise ValueError("GROQ_API_KEY is not set.")
        return self

    def _call(self, prompt: str, stop: Optional[List[str]] = None, **kwargs) -> str:
        headers = {
            "Authorization": f"Bearer {self.groq_api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": self.temperature,
        }
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
        if response.status_code != 200:
            raise ValueError(f"Groq API error: {response.status_code} - {response.text}")
        return response.json()["choices"][0]["message"]["content"]

    @property
    def _llm_type(self) -> str:
        return "groq"
