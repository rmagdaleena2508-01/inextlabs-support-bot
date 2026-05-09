"""
Run all prompt variants × all test questions and log results to a CSV.
"""

import os
import csv
import time
from datetime import datetime
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import ClientError

from prompts import PROMPT_VARIANTS
from questions import TEST_QUESTIONS

# Setup
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
MODEL = "gemini-2.0-flash-lite"

# Load company data
with open("data/inextlabs.txt", "r", encoding="utf-8") as f:
    company_data = f.read()


def ask_bot(system_prompt, question, max_retries=3):
    """Send a question with a given system prompt. Retry on rate limits."""
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=MODEL,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=0
                ),
                contents=question
            )
            return response.text
        except ClientError as e:
            if "RESOURCE_EXHAUSTED" in str(e) and attempt < max_retries - 1:
                wait = 35
                print(f"  [Rate limit. Waiting {wait}s...]")
                time.sleep(wait)
            else:
                raise


# Prepare CSV output
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
csv_path = f"results_{timestamp}.csv"

with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["prompt_variant", "question_id", "category", "question", "answer"])

    total = len(PROMPT_VARIANTS) * len(TEST_QUESTIONS)
    counter = 0

    # Outer loop: prompt variants
    for variant_name, prompt_template in PROMPT_VARIANTS.items():
        # Fill in the {company_data} placeholder
        system_prompt = prompt_template.format(company_data=company_data)
        print(f"\n{'#' * 70}")
        print(f"# VARIANT: {variant_name}")
        print(f"{'#' * 70}")

        # Inner loop: questions
        for q in TEST_QUESTIONS:
            counter += 1
            print(f"\n[{counter}/{total}] {variant_name} | {q['id']} ({q['category']})")
            print(f"Q: {q['question']}")

            answer = ask_bot(system_prompt, q["question"])
            print(f"A: {answer[:200]}{'...' if len(answer) > 200 else ''}")

            # Write to CSV
            writer.writerow([
                variant_name,
                q["id"],
                q["category"],
                q["question"],
                answer
            ])

            # Pause to stay under rate limit
            time.sleep(5)

print(f"\n✅ Done. Results saved to: {csv_path}")