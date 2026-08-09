import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

print("===== OPENAI API SETUP TEST =====")

if api_key:
    print("✅ API key loaded successfully")
    print("✅ Key detected")
else:
    print("❌ API key not found")

print("\nAPI connection test skipped because your account has no API credits.")
print("We will connect the real AI after billing/credits are available.")