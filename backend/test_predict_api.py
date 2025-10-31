"""
Test script for the /api/predict/ endpoint
Run this to verify the Django backend is working correctly
"""

import requests
import json
import time

# Configuration
API_URL = "http://localhost:8000/api/predict/"
TEST_INPUT = "my pc screen is flickering"

def test_predict_endpoint():
    print("=" * 60)
    print("Testing /api/predict/ endpoint")
    print("=" * 60)
    print(f"\nSending request to: {API_URL}")
    print(f"Input text: '{TEST_INPUT}'")
    print("\nThis may take 30-120 seconds... Please wait.")
    print("-" * 60)
    
    try:
        start_time = time.time()
        
        # Make the request
        response = requests.post(
            API_URL,
            json={"input_text": TEST_INPUT},
            timeout=180  # 3 minutes timeout
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"\n✅ Response received in {duration:.1f} seconds")
        print("-" * 60)
        
        # Check status code
        if response.status_code == 200:
            data = response.json()
            
            if data.get('success'):
                print("\n✅ SUCCESS!")
                print("\n📊 Response Data:")
                print(f"  Model: {data.get('model', 'N/A')}")
                print(f"  Finish Reason: {data.get('finish_reason', 'N/A')}")
                
                if 'usage' in data:
                    usage = data['usage']
                    print(f"\n📈 Token Usage:")
                    print(f"  Prompt: {usage.get('prompt_tokens', 0)}")
                    print(f"  Completion: {usage.get('completion_tokens', 0)}")
                    print(f"  Total: {usage.get('total_tokens', 0)}")
                
                # Display the actual message
                message = data.get('message') or data.get('prediction', '')
                print(f"\n💬 AI Response:")
                print("=" * 60)
                print(message)
                print("=" * 60)
                
                # Save to file for inspection
                with open('test_response.json', 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                print("\n💾 Full response saved to: test_response.json")
                
            else:
                print("\n❌ API returned success=false")
                print(f"Error: {data.get('error', 'Unknown error')}")
        else:
            print(f"\n❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.Timeout:
        print("\n⏱️ REQUEST TIMED OUT")
        print("The model is taking longer than expected.")
        print("This could mean:")
        print("  1. The LLM server is processing a complex query")
        print("  2. The ngrok tunnel is slow")
        print("  3. The LLM server is not responding")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ CONNECTION ERROR")
        print("Could not connect to the Django server.")
        print("Make sure:")
        print("  1. Django server is running: python manage.py runserver")
        print("  2. Server is accessible at http://localhost:8000")
        
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    test_predict_endpoint()
