"""
Google Gemini LLM Provider

Implements LLM provider interface using Google's Gemini API via Google AI Studio.
"""

import os
from typing import Dict, Any
import google.generativeai as genai
from .base import LLMProvider


class GeminiProvider(LLMProvider):
    """
    Google Gemini API provider implementation.
    
    Uses the google-generativeai library to interact with Gemini models.
    Requires GEMINI_API_KEY environment variable to be set.
    """
    
    def __init__(self):
        """Initialize the Gemini provider with API key and model configuration."""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY environment variable is not set. "
                "Please configure your Google AI Studio API key in the .env file."
            )
        
        # Configure the Gemini API
        genai.configure(api_key=api_key)
        
        # Get model name from environment or use default
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        
        # Initialize the model
        self.model = genai.GenerativeModel(self.model_name)
        
        print(f"[SUCCESS] Google Gemini provider initialized with model: {self.model_name}")
    
    def complete(self, prompt: str, temperature: float = 0.7, max_tokens: int = 4000) -> Dict[str, Any]:
        """
        Generate a completion using Google Gemini.
        
        Args:
            prompt: The input prompt (combines system + user messages)
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum number of tokens to generate
            
        Returns:
            Dictionary with completion results
        """
        try:
            # Configure generation parameters
            generation_config = genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
            )
            
            # Generate content
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            # Extract response text
            content = response.text
            
            # Build response in OpenAI-compatible format
            return {
                'content': content,
                'model': self.model_name,
                'finish_reason': 'stop',  # Gemini doesn't provide detailed finish reasons
                'usage': {
                    'prompt_tokens': 0,  # Gemini API doesn't expose token counts in free tier
                    'completion_tokens': 0,
                    'total_tokens': 0
                },
                'metadata': {
                    'provider': 'Google Gemini',
                    'id': '',
                    'created': '',
                    'object': 'chat.completion',
                    'system_fingerprint': ''
                }
            }
            
        except Exception as e:
            # Re-raise with more context
            raise Exception(f"Gemini API error: {str(e)}")
    
    def get_provider_name(self) -> str:
        """Get the provider name."""
        return "Google Gemini"
