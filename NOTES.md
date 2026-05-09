## Day 2 / Phase 4 — SHIPPED PARTIAL ✅

What got done:
- ✅ Defined 4 prompt variants (bare, grounded, fewshot, tone)
- ✅ Defined 10 test questions across 4 categories (answerable, missing, offtopic, tricky)
- ✅ Built run_experiment.py with retry + rate-limit handling
- ✅ Collected full data for `bare` variant (10/10 questions)
- ✅ Collected partial data for `grounded` (4/10 questions)
- ✅ Scored `bare` variant — 7/10 success, 3 failures all linked to sycophancy

What got blocked:
- ❌ Hit Gemini free-tier daily quota (20 requests/day per model) twice
- ❌ Couldn't complete fewshot and tone variants
- Decision: ship what I have rather than wait days for quota cycles

Key insight from the data I collected:
The bare variant didn't fail on hard questions. It failed when it had to
*resist* something — speculation (Q05 pricing), off-topic compliance
(Q09 poem), false-premise agreement (Q10 AWS). That failure mode has a
name: sycophancy. Even minimal-prompt LLMs are good at answering;
they're bad at refusing.

What I'd do differently:
- Use a paid API tier (or run smaller batches across more days)
- Test fewer variants (2 instead of 4) to fit the quota
- Pre-test with 1 question per variant to validate the pipeline before running full batch