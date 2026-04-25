"""
Gemma LLM wrapper for LangChain.
Supports both local and remote (HTTP API) connections to Gemma.
"""

import os
from typing import Optional, List, Any, Dict
from langchain_core.language_models.llms import LLM
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
import httpx
import json


class GemmaLLM(LLM):
    """
    Custom LLM wrapper for Gemma model.
    Can connect to Gemma via HTTP API endpoint running on ASUS Ascent GX10.
    """
    
    base_url: str = "http://localhost:8000"
    model_name: str = "google/gemma-4-2b-it"
    temperature: float = 0.7
    max_new_tokens: int = 512
    top_p: float = 0.95
    timeout: float = 60.0
    
    @property
    def _llm_type(self) -> str:
        return "gemma"
    
    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """Call the Gemma model via HTTP API."""
        
        endpoint = f"{self.base_url}/generate"
        
        payload = {
            "prompt": prompt,
            "max_new_tokens": self.max_new_tokens,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "do_sample": True,
        }
        
        if stop:
            payload["stop_sequences"] = stop
        
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(endpoint, json=payload)
                response.raise_for_status()
                result = response.json()
                return result.get("generated_text", "")
        except httpx.HTTPError as e:
            raise Exception(f"Error calling Gemma API: {e}")
    
    @property
    def _identifying_params(self) -> Dict[str, Any]:
        """Get the identifying parameters."""
        return {
            "base_url": self.base_url,
            "model_name": self.model_name,
            "temperature": self.temperature,
            "max_new_tokens": self.max_new_tokens,
        }


def create_gemma_llm(
    base_url: str = "http://localhost:8000",
    model_name: str = "google/gemma-4-2b-it",
    temperature: float = 0.7,
    max_new_tokens: int = 512,
) -> GemmaLLM:
    """
    Factory function to create a GemmaLLM instance.
    
    Args:
        base_url: The base URL of the Gemma HTTP API endpoint
        model_name: The name of the Gemma model
        temperature: Sampling temperature
        max_new_tokens: Maximum number of tokens to generate
    
    Returns:
        A GemmaLLM instance
    """
    return GemmaLLM(
        base_url=base_url,
        model_name=model_name,
        temperature=temperature,
        max_new_tokens=max_new_tokens,
    )
