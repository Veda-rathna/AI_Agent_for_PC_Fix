"""
Base LLM Provider Interface

Defines the abstract interface that all LLM providers must implement.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class LLMProvider(ABC):
    """
    Abstract base class for LLM providers.
    
    All LLM providers (Gemini, Local LLaMA, etc.) must inherit from this class
    and implement the complete() method.
    """
    
    @abstractmethod
    def complete(self, prompt: str, temperature: float = 0.7, max_tokens: int = 4000) -> Dict[str, Any]:
        """
        Generate a completion for the given prompt.
        
        Args:
            prompt: The input prompt for the LLM
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum number of tokens to generate
            
        Returns:
            Dictionary containing:
                - 'content': The generated text response
                - 'model': Name of the model used
                - 'finish_reason': Reason for completion ('stop', 'length', etc.)
                - 'usage': Token usage statistics
                - 'metadata': Additional provider-specific metadata
        """
        pass
    
    @abstractmethod
    def get_provider_name(self) -> str:
        """
        Get the name of this provider.
        
        Returns:
            String identifier for this provider (e.g., "Google Gemini", "Local LLaMA")
        """
        pass
