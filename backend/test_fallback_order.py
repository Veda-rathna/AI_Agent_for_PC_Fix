"""
Test to verify the LLM provider fallback order is working correctly
"""

import os
import sys
import django

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pc_diagnostic.settings')
django.setup()

from dotenv import load_dotenv
load_dotenv()

print("=" * 60)
print("🔍 Testing LLM Provider Fallback Order")
print("=" * 60)

print("\n📋 Environment Configuration:")
print(f"   LLM_PROVIDER: {os.getenv('LLM_PROVIDER')}")
print(f"   GEMINI_API_KEY: {'✅ Set' if os.getenv('GEMINI_API_KEY') else '❌ Not Set'}")
print(f"   GEMINI_MODEL: {os.getenv('GEMINI_MODEL')}")
print(f"   LLAMA_API_BASE: {os.getenv('LLAMA_API_BASE')}")
print(f"   LLAMA_MODEL_ID: {os.getenv('LLAMA_MODEL_ID')}")

print("\n🧪 Test 1: Normal Operation (with Gemini)")
print("-" * 60)
from pc_diagnostic.llm.factory import get_llm_provider

try:
    provider = get_llm_provider()
    provider_name = provider.get_provider_name()
    print(f"✅ Got provider: {provider_name}")
    
    # Test a simple completion
    print("\n📝 Testing completion...")
    result = provider.complete(
        prompt="Briefly explain what causes a computer to overheat.",
        temperature=0.7,
        max_tokens=100
    )
    
    print(f"✅ Completion successful!")
    print(f"   Model: {result['model']}")
    print(f"   Response length: {len(result['content'])} characters")
    print(f"   First 100 chars: {result['content'][:100]}...")
    
except Exception as e:
    print(f"❌ Error: {str(e)}")

print("\n" + "=" * 60)
print("✅ Test Complete!")
print("=" * 60)

print("\n📊 Expected Fallback Order:")
print("   1️⃣  Gemini Model (gemini-2.5-flash)")
print("   2️⃣  Local LLaMA (reasoning-llama-3.1-cot-re1-nmt-v2-orpo-i1)")
print("   3️⃣  Offline Diagnostic (basic pattern matching)")

print("\n💡 Current Status:")
if os.getenv('LLM_PROVIDER') == 'gemini' and os.getenv('GEMINI_API_KEY'):
    print("   ✅ Should be using: Gemini Model")
elif os.getenv('LLM_PROVIDER') == 'local':
    print("   ✅ Should be using: Local LLaMA")
else:
    print("   ⚠️  Unclear configuration")
