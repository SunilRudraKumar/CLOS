
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load key from api/.env
load_dotenv("api/.env")
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    # Try reading directly if dotenv fails
    with open("api/.env") as f:
        for line in f:
            if line.startswith("GOOGLE_API_KEY="):
                api_key = line.strip().split("=")[1]
                break

print(f"Using Key: {api_key[:10]}...")
genai.configure(api_key=api_key)

print("List of available models:")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)
