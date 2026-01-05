"""
Test the Django /api/predict/ endpoint with Gemini
"""

import requests
import json

print("=" * 60)
print("🚀 Testing Django API with Google Gemini")
print("=" * 60)
print()

# Test data
test_data = {
    "input_text": "My computer is running slow and the fans are very loud",
    "generate_report": False
}

print("📤 Sending request to http://localhost:8000/api/predict/")
print(f"   Input: {test_data['input_text']}")
print()

try:
    response = requests.post(
        "http://localhost:8000/api/predict/",
        json=test_data,
        timeout=60
    )
    
    if response.status_code == 200:
        result = response.json()
        
        print("✅ API call successful!")
        print()
        print("=" * 60)
        print("📊 Response Summary")
        print("=" * 60)
        print()
        print(f"✅ Success: {result.get('success')}")
        print(f"🤖 AI Provider: {result.get('ai_provider', result.get('metadata', {}).get('provider', 'Unknown'))}")
        print(f"📦 Model: {result.get('model')}")
        print(f"🏁 Finish Reason: {result.get('finish_reason')}")
        print(f"🆔 Session ID: {result.get('session_id')}")
        print()
        
        # Check if Gemini was used
        provider = result.get('ai_provider') or result.get('metadata', {}).get('provider')
        
        if 'Gemini' in str(provider):
            print("🎉 SUCCESS! Google Gemini is being used!")
            print()
        elif 'LLaMA' in str(provider) or 'Local' in str(provider):
            print("⚠️  Using Local LLaMA fallback (Gemini not reached)")
            print()
        elif 'Mock' in str(provider) or 'Offline' in str(provider):
            print("⚠️  Using Offline Mock fallback (both Gemini and LLaMA failed)")
            print()
        
        print("=" * 60)
        print("📄 AI Analysis (First 500 characters)")
        print("=" * 60)
        print()
        message = result.get('message', result.get('prediction', ''))
        print(message[:500])
        if len(message) > 500:
            print("...")
        print()
        
        # Telemetry summary
        if 'telemetry_summary' in result:
            print("=" * 60)
            print("📊 Telemetry Summary")
            print("=" * 60)
            print()
            telemetry = result['telemetry_summary']
            print(f"System: {telemetry.get('system')}")
            print(f"CPU Usage: {telemetry.get('cpu_usage')}%")
            print(f"Memory Usage: {telemetry.get('memory_usage')}%")
            print()
        
        # Token usage
        if 'usage' in result:
            usage = result['usage']
            print("=" * 60)
            print("📈 Token Usage")
            print("=" * 60)
            print()
            print(f"Prompt Tokens: {usage.get('prompt_tokens', 0)}")
            print(f"Completion Tokens: {usage.get('completion_tokens', 0)}")
            print(f"Total Tokens: {usage.get('total_tokens', 0)}")
            print()
        
    else:
        print(f"❌ API returned error status: {response.status_code}")
        print(response.text)
        
except requests.exceptions.ConnectionError:
    print("❌ Failed to connect to Django server")
    print()
    print("💡 Make sure the Django server is running:")
    print("   python manage.py runserver")
    print()
except Exception as e:
    print(f"❌ Error: {e}")
    print()

print("=" * 60)
print("✅ Test Complete")
print("=" * 60)
