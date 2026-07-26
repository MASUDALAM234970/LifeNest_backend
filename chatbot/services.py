from datetime import datetime
import json
import os
import re
import traceback

from decouple import config
from google import genai
from google.genai import types
from rapidfuzz import fuzz

# ==========================================================
# Gemini Client
# ==========================================================

client = genai.Client(api_key=config("GEMINI_API_KEY"))


# ==========================================================
# Load Keywords
# ==========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# ==========================================================
# System Prompt
# ==========================================================

def system_prompt():
    return """
You are CalmMind, a warm and supportive mental health companion.

Rules:
- Reply in exactly 2 sentences.
- Maximum 35 words.
- Never use bullet points.
- Never use numbered lists.
- Never use markdown.
- Give only one practical suggestion.
- Keep the response concise and natural.
"""


# ==========================================================
# Greetings
# ==========================================================


GREETINGS = {
    "English": {
        "hi", "hello", "hey", "hii", "helo"
    },
    "Bangla": {
        "হাই", "হ্যালো", "হেই", "আসসালামু আলাইকুম", "সালাম"
    },
}


def is_greeting(text, language):

    text = text.strip().lower()

    return text in GREETINGS.get(language, set())


# ==========================================================
# Reject Messages
# ==========================================================




# ==========================================================
# Greeting Replies
# ==========================================================
HELLO = {
    "English":
        "Hello! I'm CalmMind. How are you feeling today?",

    "Bangla":
        "হ্যালো! আমি CalmMind। আজ আপনার কেমন লাগছে?",
}

# ==========================================================
# Psychology Check
# ==========================================================


# ==========================================================
# Generate Reply
# ==========================================================


import re

def generate_reply(message):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    prompt = f"""
Current Time: {current_time}

User Message:
{message}
"""

    try:
        response = client.models.generate_content(
            model="models/gemini-3.5-flash-lite",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.2,
                top_p=0.9,
                max_output_tokens=30,
            ),
        )

        # Clean the response
        reply = response.text.strip()
        reply = re.sub(r"\n+", " ", reply)
        reply = re.sub(r"\s{2,}", " ", reply).strip()

        return reply

    except Exception:
        traceback.print_exc()
        return "Sorry, something went wrong."