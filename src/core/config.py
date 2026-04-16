"""
Lab 11 — Configuration & API Key Setup
"""
import os
from pathlib import Path
from dotenv import load_dotenv


def setup_api_key():
    """Load Google API key from .env file or environment."""
    # Load .env file from project root
    env_path = Path(__file__).resolve().parent.parent.parent / '.env'
    load_dotenv(dotenv_path=env_path)
    
    # Check if API key is loaded
    if "GOOGLE_API_KEY" not in os.environ or os.environ["GOOGLE_API_KEY"] == "your-google-api-key-here":
        print("⚠️  GOOGLE_API_KEY not found or not set in .env file")
        print("Please update the .env file with your Google API key")
        print("Get your key at: https://aistudio.google.com/apikey")
        api_key = input("\nOr enter your Google API Key now: ")
        if api_key:
            os.environ["GOOGLE_API_KEY"] = api_key
        else:
            raise ValueError("GOOGLE_API_KEY is required to run this lab")
    
    # Set Vertex AI flag if not already set
    if "GOOGLE_GENAI_USE_VERTEXAI" not in os.environ:
        os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "0"
    
    print("✅ API key loaded successfully")


# Allowed banking topics (used by topic_filter)
ALLOWED_TOPICS = [
    "banking", "account", "transaction", "transfer",
    "loan", "interest", "savings", "credit",
    "deposit", "withdrawal", "balance", "payment",
    "tai khoan", "giao dich", "tiet kiem", "lai suat",
    "chuyen tien", "the tin dung", "so du", "vay",
    "ngan hang", "atm",
]

# Blocked topics (immediate reject)
BLOCKED_TOPICS = [
    "hack", "exploit", "weapon", "drug", "illegal",
    "violence", "gambling", "bomb", "kill", "steal",
]
