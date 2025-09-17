# test_deepseek.py
import requests
import json

# Method 1: Using requests (simpler)
def test_with_requests():
    print("=== Testing with requests ===")
    
    api_key = "sk-1a53952d285149a6aa4eda9a8a9ed027"
    url = "https://api.deepseek.com/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": "Hello"}
        ],
        "max_tokens": 10
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Success: {result['choices'][0]['message']['content']}")
            return True
        else:
            print(f"Error Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"Request failed: {e}")
        return False

# Method 2: Using OpenAI client (if you have it installed)
def test_with_openai_client():
    print("\n=== Testing with OpenAI client ===")
    
    try:
        from openai import OpenAI
        
        client = OpenAI(
            api_key="sk-1a53952d285149a6aa4eda9a8a9ed027",
            base_url="https://api.deepseek.com"
        )
        
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": "Hello"}
            ],
            max_tokens=10
        )
        
        print(f"Success: {response.choices[0].message.content}")
        return True
        
    except ImportError:
        print("OpenAI library not installed. Install with: pip install openai")
        return False
    except Exception as e:
        print(f"OpenAI client failed: {e}")
        return False

# Run both tests
if __name__ == "__main__":
    print("Testing DeepSeek API...")
    
    # Test Method 1
    success1 = test_with_requests()
    
    # Test Method 2
    success2 = test_with_openai_client()
    
    print(f"\n=== Results ===")
    print(f"Requests method: {'✅ SUCCESS' if success1 else '❌ FAILED'}")
    print(f"OpenAI client method: {'✅ SUCCESS' if success2 else '❌ FAILED'}")
    
    if success1 or success2:
        print("\n🎉 API is working! The issue is in your Streamlit app.")
    else:
        print("\n⚠️  API not working. Check:")
        print("1. API key validity")
        print("2. Account balance/credits")
        print("3. Network connection")
        print("4. DeepSeek service status")