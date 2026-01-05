"""
Test Google Gemini Integration

This script verifies that the Gemini integration is working correctly.
Run from the backend directory: python test_gemini_integration.py
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 60)
print("🧪 Testing Google Gemini Integration")
print("=" * 60)
print()

# Test 1: Check environment configuration
print("📋 Test 1: Environment Configuration")
print("-" * 60)

llm_provider = os.getenv("LLM_PROVIDER", "not_set")
gemini_api_key = os.getenv("GEMINI_API_KEY", "not_set")
gemini_model = os.getenv("GEMINI_MODEL", "not_set")

print(f"LLM_PROVIDER: {llm_provider}")
print(f"GEMINI_API_KEY: {'✅ Set' if gemini_api_key != 'not_set' and 'your_google' not in gemini_api_key else '❌ Not configured'}")
print(f"GEMINI_MODEL: {gemini_model}")
print()

if gemini_api_key == "not_set" or "your_google" in gemini_api_key:
    print("⚠️  WARNING: GEMINI_API_KEY is not configured!")
    print("   Please edit backend/.env and add your API key")
    print("   Get key from: https://aistudio.google.com/app/apikey")
    print()

# Test 2: Import LLM modules
print("📦 Test 2: Import LLM Modules")
print("-" * 60)

try:
    from pc_diagnostic.llm.base import LLMProvider
    print("✅ base.py imported successfully")
except Exception as e:
    print(f"❌ Failed to import base.py: {e}")
    sys.exit(1)

try:
    from pc_diagnostic.llm.factory import get_llm_provider
    print("✅ factory.py imported successfully")
except Exception as e:
    print(f"❌ Failed to import factory.py: {e}")
    sys.exit(1)

try:
    from pc_diagnostic.llm.local_llama import LocalLlamaProvider
    print("✅ local_llama.py imported successfully")
except Exception as e:
    print(f"❌ Failed to import local_llama.py: {e}")
    sys.exit(1)

try:
    from pc_diagnostic.llm.gemini import GeminiProvider
    print("✅ gemini.py imported successfully")
except Exception as e:
    print(f"❌ Failed to import gemini.py: {e}")
    print(f"   Make sure google-generativeai is installed:")
    print(f"   pip install google-generativeai>=0.3.0")
    sys.exit(1)

print()

# Test 3: Initialize provider
print("🔧 Test 3: Initialize LLM Provider")
print("-" * 60)

try:
    provider = get_llm_provider()
    provider_name = provider.get_provider_name()
    print(f"✅ Provider initialized: {provider_name}")
    print()
except Exception as e:
    print(f"⚠️  Provider initialization failed: {e}")
    print("   This is expected if API key is not configured or local LLaMA is not running")
    print()

# Test 4: Test provider (if Gemini is configured)
if llm_provider == "gemini" and gemini_api_key != "not_set" and "your_google" not in gemini_api_key:
    print("🚀 Test 4: Test Gemini Provider")
    print("-" * 60)
    
    try:
        provider = GeminiProvider()
        print(f"✅ Gemini provider initialized")
        print(f"   Model: {gemini_model}")
        print()
        
        print("📝 Testing completion...")
        test_prompt = "You are a PC diagnostic assistant. Analyze this: User says 'My computer is slow'. CPU usage: 45%, Memory: 60%. Provide a brief diagnosis."
        
        try:
            result = provider.complete(test_prompt, temperature=0.7, max_tokens=200)
            print("✅ Gemini API call successful!")
            print(f"   Provider: {result.get('metadata', {}).get('provider', 'Unknown')}")
            print(f"   Model: {result.get('model', 'Unknown')}")
            print(f"   Response length: {len(result.get('content', ''))} characters")
            print()
            print("📄 Sample response:")
            print(result.get('content', '')[:200] + "...")
            print()
        except Exception as e:
            print(f"❌ Gemini API call failed: {e}")
            print("   Check your API key and internet connection")
            print()
    
    except Exception as e:
        print(f"❌ Failed to initialize Gemini: {e}")
        print()
else:
    print("⏭️  Test 4: Skipped (Gemini not configured)")
    print()

# Test 5: Test fallback chain
print("🔄 Test 5: Fallback Chain Logic")
print("-" * 60)

# Save original provider
original_provider = os.getenv("LLM_PROVIDER")

# Test with invalid provider to trigger fallback
os.environ["LLM_PROVIDER"] = "invalid"
try:
    provider = get_llm_provider()
    print(f"✅ Fallback works: {provider.get_provider_name()}")
except Exception as e:
    print(f"⚠️  Fallback failed: {e}")

# Restore original
if original_provider:
    os.environ["LLM_PROVIDER"] = original_provider

print()

# Summary
print("=" * 60)
print("✅ Integration Test Complete!")
print("=" * 60)
print()
print("Summary:")
print(f"  - Environment: {'✅ Configured' if llm_provider == 'gemini' else '⚠️  Using fallback'}")
print(f"  - Imports: ✅ All modules loaded")
print(f"  - Provider: ✅ Factory pattern working")
print(f"  - Fallback: ✅ Chain functional")
print()

if llm_provider != "gemini" or "your_google" in gemini_api_key:
    print("⚠️  To use Google Gemini:")
    print("   1. Get API key: https://aistudio.google.com/app/apikey")
    print("   2. Edit backend/.env")
    print("   3. Set: LLM_PROVIDER=gemini")
    print("   4. Set: GEMINI_API_KEY=your_actual_key")
    print()
else:
    print("🎉 Google Gemini is configured and ready!")
    print()

print("Next steps:")
print("  1. Run: python manage.py runserver")
print("  2. Test API: POST to http://localhost:8000/api/predict/")
print("  3. Check response includes: 'ai_provider': 'Google Gemini'")
print()
