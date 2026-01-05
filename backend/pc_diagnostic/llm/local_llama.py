"""
Local LLaMA Provider

Implements LLM provider interface using local llama.cpp server.
This provider connects to a locally-running LLM server using OpenAI-compatible API.
"""

import os
import requests
import urllib3
from typing import Dict, Any
from .base import LLMProvider

# Disable SSL warnings for cloudflare tunnels
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class LocalLlamaProvider(LLMProvider):
    """
    Local LLaMA llama.cpp server provider.
    
    Connects to a locally running llama.cpp server that exposes an OpenAI-compatible API.
    This is the fallback provider when Gemini is not available or configured.
    """
    
    def __init__(self):
        """Initialize the local LLaMA provider with server configuration."""
        # Get configuration from environment or use defaults
        self.api_base = os.getenv("LLAMA_API_BASE", "http://127.0.0.1:1234")
        self.model_id = os.getenv("LLAMA_MODEL_ID", "reasoning-llama-3.1-cot-re1-nmt-v2-orpo-i1")
        
        print(f"[SUCCESS] Local LLaMA provider initialized")
        print(f"   API Base: {self.api_base}")
        print(f"   Model ID: {self.model_id}")
    
    def complete(self, prompt: str, temperature: float = 0.7, max_tokens: int = 4000) -> Dict[str, Any]:
        """
        Generate a completion using local llama.cpp server.
        
        This method maintains the exact same logic as the original views.py implementation
        to ensure compatibility and prevent breaking changes.
        
        Args:
            prompt: The input prompt (combines system + user messages)
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum number of tokens to generate
            
        Returns:
            Dictionary with completion results
        """
        try:
            api_url = f"{self.api_base}/v1/chat/completions"
            print(f"[INFO] Attempting to connect to: {api_url}")
            print(f"[INFO] Using model: {self.model_id}")
            
            # Parse the prompt to extract system and user messages
            # The prompt format should be "System: ...\n\nUser: ..."
            messages = self._parse_prompt_to_messages(prompt)
            
            # Make request to llama.cpp server
            response = requests.post(
                api_url,
                json={
                    "model": self.model_id,
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens
                },
                timeout=600,  # 10 minutes timeout for reasoning models
                verify=False  # Disable SSL verification for cloudflare tunnels
            )
            
            print(f"[SUCCESS] Response status: {response.status_code}")
            
            # Check if the request was successful
            if response.status_code != 200:
                raise Exception(f'Model API error: {response.status_code} - {response.text}')
            
            # Parse the response
            result = response.json()
            
            # Extract the model's response
            if 'choices' not in result or len(result['choices']) == 0:
                raise Exception('No choices in model response')
            
            choice = result['choices'][0]
            
            # Get the assistant's message content
            content = choice.get('message', {}).get('content', '')
            finish_reason = choice.get('finish_reason', 'unknown')
            
            if not content:
                raise Exception('No content in model response')
            
            # Get usage information
            usage = result.get('usage', {})
            model_used = result.get('model', self.model_id)
            
            # Return in standardized format
            return {
                'content': content,
                'model': model_used,
                'finish_reason': finish_reason,
                'usage': {
                    'prompt_tokens': usage.get('prompt_tokens', 0),
                    'completion_tokens': usage.get('completion_tokens', 0),
                    'total_tokens': usage.get('total_tokens', 0)
                },
                'metadata': {
                    'provider': 'Local LLaMA',
                    'id': result.get('id', ''),
                    'created': result.get('created', ''),
                    'object': result.get('object', ''),
                    'system_fingerprint': result.get('system_fingerprint', '')
                }
            }
            
        except requests.exceptions.ConnectionError as e:
            raise Exception(f"Failed to connect to local LLaMA server at {self.api_base}: {str(e)}")
        except requests.exceptions.Timeout as e:
            raise Exception(f"Timeout connecting to local LLaMA server: {str(e)}")
        except Exception as e:
            raise Exception(f"Local LLaMA error: {str(e)}")
    
    def _parse_prompt_to_messages(self, prompt: str) -> list:
        """
        Parse a combined prompt into OpenAI-style messages.
        
        Expects format with system and user sections, or treats entire prompt as user message.
        
        Args:
            prompt: Combined prompt text
            
        Returns:
            List of message dictionaries
        """
        # Try to parse structured prompt
        if "SYSTEM CONTEXT:" in prompt or "You are an AI PC Diagnostic Expert" in prompt:
            # Split into system and user parts
            parts = prompt.split("User Problem:", 1)
            if len(parts) == 2:
                system_content = parts[0].strip()
                user_content = "User Problem:" + parts[1]
                
                return [
                    {"role": "system", "content": system_content},
                    {"role": "user", "content": user_content}
                ]
        
        # Fallback: treat entire prompt as user message
        return [{"role": "user", "content": prompt}]
    
    def get_provider_name(self) -> str:
        """Get the provider name."""
        return "Local LLaMA"
