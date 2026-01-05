"""
Direct Gemini API Test
Tests if the Gemini API key is valid and working
"""

import os
from dotenv import load_dotenv

# Load environment
load_dotenv()

print("=" * 60)
print("🔑 Testing Google Gemini API Key")
print("=" * 60)
print()

# Check if key is set
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ GEMINI_API_KEY is not set in .env")
    exit(1)

print(f"✅ API Key found: {api_key[:20]}...{api_key[-4:]}")
print()

# Try to import and use Gemini
try:
    import google.generativeai as genai
    print("✅ google-generativeai package imported successfully")
    print()
except ImportError as e:
    print("❌ Failed to import google-generativeai")
    print(f"   Error: {e}")
    print()
    print("   Install with: pip install google-generativeai>=0.3.0")
    exit(1)

# Configure and test
try:
    print("🔧 Configuring Gemini with API key...")
    genai.configure(api_key=api_key)
    print("✅ API key accepted")
    print()
    
    print("🚀 Creating model instance...")
    model = genai.GenerativeModel('gemini-2.5-flash')
    print("✅ Model created successfully")
    print()
    
    print("📝 Testing generation...")
    test_prompt = "Say 'Hello from Gemini!' in exactly 5 words."
    
    response = model.generate_content(test_prompt)
    print("✅ API call successful!")
    print()
    print("Response:")
    print("-" * 60)
    print(response.text)
    print("-" * 60)
    print()
    
    print("🎉 SUCCESS! Gemini API is working perfectly!")
    print()
    print("Your API key is valid and the integration should work.")
    print("Try the /api/predict/ endpoint again - it should use Gemini now.")
    
except Exception as e:
    print(f"❌ Failed to use Gemini API")
    print(f"   Error: {str(e)}")
    print()
    
    if "API_KEY_INVALID" in str(e) or "invalid" in str(e).lower():
        print("💡 Solution: Your API key appears to be invalid")
        print("   1. Visit https://aistudio.google.com/app/apikey")
        print("   2. Create a NEW API key")
        print("   3. Update GEMINI_API_KEY in backend/.env")
        print("   4. Restart the Django server")
    elif "quota" in str(e).lower():
        print("💡 Solution: API quota exceeded")
        print("   1. Check your Google AI Studio quota")
        print("   2. Wait for quota reset or upgrade plan")
    elif "network" in str(e).lower() or "connection" in str(e).lower():
        print("💡 Solution: Network issue detected")
        print("   1. Check your internet connection")
        print("   2. Verify firewall settings")
        print("   3. Try again in a few moments")
    else:
        print("💡 General troubleshooting:")
        print("   1. Verify API key is correct")
        print("   2. Check internet connection")
        print("   3. See error message above for details")
    
    exit(1)
