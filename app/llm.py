
import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv(override=True)

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

client = genai.Client(api_key=API_KEY) if API_KEY else None


def generate_response(prompt: str) -> str:

    if client is None:
        raise RuntimeError("GEMINI_API_KEY is missing. Check your .env file.")

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=prompt
            )

            return response.text or ""

        except Exception as error:
            error_message = str(error)

            if "503" in error_message and attempt < 2:
                time.sleep(2 ** (attempt + 1))
                continue

            raise
