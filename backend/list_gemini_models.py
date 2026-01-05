"""
List Available Gemini Models
"""

import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 60)
print("📋 Listing Available Gemini Models")
print("=" * 60)
print()

try:
    import google.generativeai as genai
    
    api_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    
    print("Available models:")
    print("-" * 60)
    
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"✅ {model.name}")
            print(f"   Display Name: {model.display_name}")
            print(f"   Description: {model.description[:100] if len(model.description) > 100 else model.description}")
            print()
    
except Exception as e:
    print(f"Error: {e}")
