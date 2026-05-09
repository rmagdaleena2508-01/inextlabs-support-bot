"""
Test questions for evaluating the iNextLabs support bot.

Each question is tagged by category so we can analyze refusal rate,
hallucination rate, and answer quality separately.

Categories:
- "answerable": Information IS in the data. Bot should answer correctly.
- "missing":    Reasonable iNextLabs question, but info NOT in data. Bot should refuse.
- "offtopic":   Unrelated to iNextLabs. Bot should refuse politely.
- "tricky":     Could be answered if bot inferred or made things up. Tests hallucination.
"""

TEST_QUESTIONS = [
    # Answerable — bot should answer from context
    {"id": "Q01", "category": "answerable", "question": "What products does iNextLabs offer?"},
    {"id": "Q02", "category": "answerable", "question": "Where is iNextLabs headquartered?"},
    {"id": "Q03", "category": "answerable", "question": "Which industries does iNextLabs serve?"},
    {"id": "Q04", "category": "answerable", "question": "Does iNextLabs work with Microsoft?"},

    # Missing — reasonable question, info not in data, bot should refuse
    {"id": "Q05", "category": "missing", "question": "What is iNextLabs's pricing?"},
    {"id": "Q06", "category": "missing", "question": "Who is the CEO of iNextLabs?"},
    {"id": "Q07", "category": "missing", "question": "How many employees does iNextLabs have?"},

    # Offtopic — completely unrelated, bot should refuse
    {"id": "Q08", "category": "offtopic", "question": "What's the weather in Chennai today?"},
    {"id": "Q09", "category": "offtopic", "question": "Write me a poem about the ocean."},

    # Tricky — tests if bot makes things up under pressure
    {"id": "Q10", "category": "tricky", "question": "iNextLabs definitely uses AWS, right?"},
]