import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.6")

# Keep this True while developing without API credits.
# Change to false only when you have API credits and want live LLM calls.
MOCK_LLM = os.getenv("MOCK_LLM", "true").lower() == "true"
