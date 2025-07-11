import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Google AI Studio (Gemini API)
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    print("✅ API key loaded successfully")
else:
    print("❌ API key not found in .env file")
    exit(1)

def test_api_connection():
    """Test the API connection with a simple prompt"""
    try:
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        response = model.generate_content("Hello! Please respond with 'API connection successful' if you can see this message.")
        print("✅ API connection successful!")
        print(f"Response: {response.text}")
        return True
    except Exception as e:
        print(f"❌ API connection failed: {e}")
        return False

if __name__ == "__main__":
    test_api_connection() 