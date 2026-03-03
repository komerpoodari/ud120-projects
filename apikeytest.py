from google import genai
from dotenv import load_dotenv
import os

#0  Best practice: Load from a secure source, not hardcoded
load_dotenv()  # Load environment variables from a .env file if using python-dotenv
api_key = os.getenv("GEMINI_API_KEY") # Ensure this environment variable is set before running the script

#1 Get the Client
if api_key:
    print("Using API Key: ✓ Successfully loaded from environment")
    client = genai.Client(api_key=api_key)
    api_key = None # Clear variable to prevent accidental exposure in logs or memory dumps
else:
    print("ERROR: GEMINI_API_KEY not found in environment variables")

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