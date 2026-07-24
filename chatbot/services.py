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

with open(
    os.path.join(BASE_DIR, "psychology_keywords.json"),
    encoding="utf-8",
) as f:
    KEYWORDS = json.load(f)


# ==========================================================
# System Prompt
# ==========================================================

def system_prompt(language):
    return f"""
You are CalmMind, a warm and supportive mental health companion.

Rules:
- Reply only in {language}.
- Answer only psychology and mental health questions.
- Respond naturally, like a caring listener.
- Never diagnose or claim to be a therapist.
- Start by acknowledging the user's emotion.
- Then gently encourage them to share more or offer simple emotional support.
- Use exactly 2 complete sentences.
- Each sentence should be around 15-25 words.
- Never repeat the user's exact words.
- Never give one-line or incomplete responses.
- Do not use bullet points.
- If the user only says something short like "মন খারাপ", "I feel sad", or "I'm anxious", still provide a complete and caring two-sentence response.
"""

# ==========================================================
# Greetings
# ==========================================================

GREETINGS = {
    "English": {
        "hi", "hello", "hey", "hii", "helo"
    },
    "Bangla": {
        "হাই", "হ্যালো", "হ্যালো!", "হ্যালো।", "হ্যালো", "হেই"
    },
    "Hindi": {
        "नमस्ते", "हाय", "हेलो"
    },
    "Arabic": {
        "مرحبا", "السلام", "اهلا"
    },
}


def is_greeting(text, language):

    text = text.strip().lower()

    return text in GREETINGS.get(language, set())


# ==========================================================
# Reject Messages
# ==========================================================

REJECT = {
    "English":
        "I answer only psychology and mental health related questions.",

    "Bangla":
        "আমি শুধুমাত্র মনোবিজ্ঞান ও মানসিক স্বাস্থ্য সম্পর্কিত প্রশ্নের উত্তর দিই।",

    "Hindi":
        "मैं केवल मानसिक स्वास्थ्य और मनोविज्ञान से जुड़े प्रश्नों का उत्तर देता हूँ।",

    "Arabic":
        "أجيب فقط على أسئلة الصحة النفسية وعلم النفس."
}


# ==========================================================
# Greeting Replies
# ==========================================================

HELLO = {

    "English":
        "Hello! How can I help you today?",

    "Bangla":
        "হ্যালো! আজ কী নিয়ে কথা বলতে চান?",

    "Hindi":
        "नमस्ते! मैं आपकी कैसे मदद कर सकता हूँ?",

    "Arabic":
        "مرحبًا، كيف يمكنني مساعدتك؟",
}


# ==========================================================
# Psychology Check
# ==========================================================

LANGUAGE_MAP = {
    "English": "english",
    "Bangla": "bangla",
    "Hindi": "hindi",
    "Arabic": "arabic",
}


def is_psychology_question(message, language):

    lang = LANGUAGE_MAP.get(language)

    if not lang:
        return False

    message = message.lower()

    for category in KEYWORDS.values():

        for keyword in category.get(lang, []):

            if fuzz.partial_ratio(message, keyword.lower()) >= 80:
                return True

    return False


# ==========================================================
# Generate Reply
# ==========================================================

def generate_reply(message, history, language):

    if is_greeting(message, language):
        return HELLO[language]

    if not is_psychology_question(message, language):
        return REJECT[language]

    contents = []

    for item in history:

        role = "user" if item["role"] == "user" else "model"

        contents.append(
            types.Content(
                role=role,
                parts=[types.Part(text=item["content"])]
            )
        )

    contents.append(
        types.Content(
            role="user",
            parts=[types.Part(text=message)]
        )
    )

    try:

        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt(language),
                temperature=0.9,
                top_p=0.95,
                max_output_tokens=406,
            ),
        )

        if response.text:
            return response.text.strip()

        return "No response generated."

    except Exception:

        traceback.print_exc()

        return "Sorry, something went wrong."
