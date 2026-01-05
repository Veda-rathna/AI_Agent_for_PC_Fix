"""
LLM Provider Factory

Creates and returns the appropriate LLM provider based on environment configuration.
"""

import os
from typing import Optional
from .base import LLMProvider
from .gemini import GeminiProvider
from .local_llama import LocalLlamaProvider


def get_llm_provider() -> LLMProvider:
    """
    Get the configured LLM provider.
    
    Determines which provider to use based on the LLM_PROVIDER environment variable.
    Supports automatic fallback if the primary provider fails to initialize.
    
    Supported providers:
        - "gemini": Google Gemini (via Google AI Studio)
        - "local" or "llama": Local llama.cpp server
        - Default: Local llama.cpp server
    
    Returns:
        LLMProvider instance (Gemini or Local LLaMA)
    
    Fallback chain:
        1. Try configured provider (Gemini if set)
        2. Fall back to Local LLaMA
        3. Let calling code handle final mock fallback
    """
    provider_name = os.getenv("LLM_PROVIDER", "local").lower()
    
    print(f"[LLM] Provider requested: {provider_name}")
    
    # Try to initialize the requested provider
    if provider_name == "gemini":
        try:
            provider = GeminiProvider()
            print(f"[SUCCESS] Using provider: {provider.get_provider_name()}")
            return provider
        except Exception as e:
            print(f"[WARNING] Failed to initialize Gemini provider: {str(e)}")
            print(f"[FALLBACK] Falling back to Local LLaMA provider...")
            # Fall through to local provider
    
    # Default or fallback: Local LLaMA
    try:
        provider = LocalLlamaProvider()
        print(f"[SUCCESS] Using provider: {provider.get_provider_name()}")
        return provider
    except Exception as e:
        # This shouldn't fail during initialization, but if it does,
        # re-raise so calling code knows to use mock analysis
        print(f"[ERROR] Failed to initialize Local LLaMA provider: {str(e)}")
        raise


def get_provider_info() -> dict:
    """
    Get information about the currently configured provider.
    
    Returns:
        Dictionary with provider configuration details
    """
    provider_name = os.getenv("LLM_PROVIDER", "local").lower()
    
    info = {
        "configured_provider": provider_name,
        "available_providers": ["gemini", "local"],
        "fallback_enabled": True
    }
    
    if provider_name == "gemini":
        info["gemini_model"] = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
        info["gemini_configured"] = bool(os.getenv("GEMINI_API_KEY"))
    
    if provider_name in ["local", "llama"]:
        info["llama_api_base"] = os.getenv("LLAMA_API_BASE", "http://127.0.0.1:1234")
        info["llama_model_id"] = os.getenv("LLAMA_MODEL_ID", "reasoning-llama-3.1-cot-re1-nmt-v2-orpo-i1")
    
    return info
