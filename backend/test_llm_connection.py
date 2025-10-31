"""
Test script to verify LLM server connection
"""
import requests
import json
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuration
LLM_API_BASE = "https://accompanying-seats-antonio-madrid.trycloudflare.com"
LLM_MODEL_ID = "llama-model"

def test_connection():
    """Test basic connection to the LLM server"""
    
    print("=" * 60)
    print("Testing LLM Server Connection")
    print("=" * 60)
    
    # Test 1: Basic GET request to check if server is accessible
    print("\n1. Testing server accessibility...")
    try:
        response = requests.get(
            f"{LLM_API_BASE}/health",
            timeout=10,
            verify=False
        )
        print(f"   ✅ Server is accessible (Status: {response.status_code})")
    except requests.exceptions.ConnectionError as e:
        print(f"   ❌ Cannot connect to server")
        print(f"   Error: {str(e)}")
        print(f"\n   Possible issues:")
        print(f"   - Cloudflare tunnel may have expired")
        print(f"   - URL may have changed")
        print(f"   - Server may not be running")
        return False
    except Exception as e:
        print(f"   ⚠️  Unexpected error: {str(e)}")
    
    # Test 2: Try the root endpoint
    print("\n2. Testing root endpoint...")
    try:
        response = requests.get(
            LLM_API_BASE,
            timeout=10,
            verify=False
        )
        print(f"   ✅ Root endpoint accessible (Status: {response.status_code})")
    except Exception as e:
        print(f"   ⚠️  Error: {str(e)}")
    
    # Test 3: Test the chat completions endpoint
    print("\n3. Testing chat completions endpoint...")
    try:
        api_url = f"{LLM_API_BASE}/v1/chat/completions"
        print(f"   URL: {api_url}")
        
        payload = {
            "model": LLM_MODEL_ID,
            "messages": [
                {"role": "user", "content": "Say 'hello' in one word"}
            ],
            "temperature": 0.7,
            "max_tokens": 50
        }
        
        print(f"   Sending test request...")
        response = requests.post(
            api_url,
            json=payload,
            timeout=120,
            verify=False
        )
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0].get('message', {}).get('content', '')
                print(f"   ✅ SUCCESS! Model responded with: {content[:100]}...")
                print(f"\n   Full response:")
                print(json.dumps(result, indent=2))
                return True
            else:
                print(f"   ⚠️  Unexpected response format")
                print(f"   Response: {response.text[:500]}")
        else:
            print(f"   ❌ Error response")
            print(f"   Response: {response.text[:500]}")
            
    except requests.exceptions.Timeout:
        print(f"   ⏱️  Request timed out (model may be loading or processing)")
    except requests.exceptions.ConnectionError as e:
        print(f"   ❌ Connection error: {str(e)}")
    except Exception as e:
        print(f"   💥 Error: {str(e)}")
        import traceback
        traceback.print_exc()
    
    return False

if __name__ == "__main__":
    success = test_connection()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ LLM Server is working correctly!")
    else:
        print("❌ LLM Server connection failed")
        print("\nTroubleshooting steps:")
        print("1. Verify the Cloudflare tunnel is still active")
        print("2. Check if the tunnel URL has changed")
        print("3. Ensure llama.cpp server is running on port 8888")
        print("4. Try accessing the URL in a browser")
        print(f"5. Current URL: {LLM_API_BASE}")
    print("=" * 60)
