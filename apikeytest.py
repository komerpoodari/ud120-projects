from google import genai
from dotenv import load_dotenv
import os

# Best practice: Load from a secure source, not hardcoded
load_dotenv()  # Load environment variables from a .env file if using python-dotenv
api_key = os.getenv("GEMINI_API_KEY") # Ensure this environment variable is set before running the script
print(f"Using API Key: {api_key[:4]}...")  # Print only the first few characters for verification
# api_key = "AIzaSyDwUyI7bSvJpVg1Pry1rhed-b-vzZqMRJ0"  # Replace with your actual API key if not using environment variable
client = genai.Client(api_key=api_key)

# 2. Use the client to call the model
# NOTE: Use 'gemini-2.0-flash' or 'gemini-1.5-flash'
try:
    response = client.models.generate_content(
        model="gemini-3-flash-preview", 
        contents="Explain the role of Hardware Security Modules (HSM) in automotive gateways."
    )
    print(response.text)
except Exception as e:
    print(f"Error: {e}")