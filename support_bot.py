import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import ClientError

# Load API key from .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Load iNextLabs data from file
with open("data/inextlabs.txt", "r", encoding="utf-8") as f:
    company_data = f.read()

# Build the system prompt
system_prompt = f"""You are a helpful customer support assistant for iNextLabs, a Cloud and AI company.

Use ONLY the information provided in the context below to answer questions.
If the answer is not in the context, say: "I don't have that information. Please contact info@inextlabs.com for more details."
Do not make up information. Do not answer questions unrelated to iNextLabs.
Keep answers concise and professional.

CONTEXT:
{company_data}
"""

# Create the Gemini client
client = genai.Client(api_key=api_key)

# A list of test questions — mix of answerable + edge cases
test_questions = [
    "What products does iNextLabs offer?",
    "Where is iNextLabs headquartered?",
    "What is iNextLabs's pricing?",
    "Who is the CEO of iNextLabs?",
    "What's the weather in Chennai today?",
    "Tell me about EngageAI for customer service.",
    "Does iNextLabs work with WhatsApp?",
]


def ask_bot(question, max_retries=3):
    """Send a question to the bot. Retry with backoff on rate limits."""
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=0
                ),
                contents=question
            )
            return response.text
        except ClientError as e:
            if "RESOURCE_EXHAUSTED" in str(e) and attempt < max_retries - 1:
                wait_seconds = 30
                print(f"  [Rate limit hit. Waiting {wait_seconds}s before retry {attempt + 2}/{max_retries}...]")
                time.sleep(wait_seconds)
            else:
                raise


# Loop through questions with a small delay between calls
for i, question in enumerate(test_questions):
    answer = ask_bot(question)
    print("=" * 70)
    print("Q:", question)
    print()
    print("A:", answer)
    print()
    
    # Pause between calls to stay under the rate limit
    if i < len(test_questions) - 1:
        time.sleep(5)