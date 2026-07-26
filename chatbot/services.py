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

def system_prompt(language):
    return f"""
You are CalmMind, a warm and supportive mental health companion.

Rules:

- Reply only in {language}.

- If the message is about emotions, stress, anxiety, depression, overthinking,
  loneliness, relationships, trauma, self-esteem, motivation, psychology,
  or mental health, provide a warm and supportive response.

- If the message is NOT related to psychology or mental health,
  politely explain that you specialize in mental health support
  and invite the user to ask a related question.

- Never diagnose or claim to be a licensed therapist.

- Respond naturally like a caring friend.

- Use exactly two complete sentences.

- Each sentence should contain around 15–25 words.

- Never use bullet points.

- Never switch languages.
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

REJECT = {
    "English":
        "I specialize in psychology and mental health support. Feel free to ask me anything related to emotions, stress, anxiety, relationships, or mental well-being.",

    "Bangla":
        "আমি মূলত মনোবিজ্ঞান ও মানসিক স্বাস্থ্য সম্পর্কিত বিষয়ে সহায়তা করি। আপনি চাইলে আপনার অনুভূতি, মানসিক চাপ, উদ্বেগ বা সম্পর্ক নিয়ে যেকোনো প্রশ্ন করতে পারেন।",
}


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

LANGUAGE_MAP = {
    "English": "english",
    "Bangla": "bangla",
}


# ==========================================================
# Generate Reply
# ==========================================================

 
def generate_reply(message, history, language):
    if is_greeting(message, language):
        return HELLO[language]

    contents = []

    for item in history:
        contents.append(
            types.Content(
                role="user" if item["role"] == "user" else "model",
                parts=[types.Part(text=item["content"])]
            )
        )

    contents.append(
        types.Content(
            role="user",
            parts=[types.Part(text=message)]
        )
    )

    # print(contents)

    try:
        response = client.models.generate_content(
            model="models/gemini-3.5-flash-lite",
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt(language),
                temperature=0.9,
                top_p=0.95,
                max_output_tokens=406,
            ),
           
        )

            # ================= DEBUG =================
      
        print(len(response.text))
       # print(repr(response.text))
        # =========================================


       
        return response.text.strip()
  

    except Exception:
        traceback.print_exc()
        return "Sorry, something went wrong."