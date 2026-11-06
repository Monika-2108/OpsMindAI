import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()


def analyze_incident(
    title,
    description,
    severity="Medium",
    previous_memories=None
):
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is missing. Check your .env file."
        )

    model = os.getenv(
        "GROQ_MODEL",
        "openai/gpt-oss-120b"
    )

    client = Groq(api_key=api_key)

    memory_context = (
        str(previous_memories)
        if previous_memories
        else "No relevant previous incidents were found."
    )

    prompt = f"""
You are OpsMind AI, an IT incident troubleshooting assistant.

Analyze the incident carefully.

INCIDENT TITLE:
{title}

DESCRIPTION:
{description}

SEVERITY:
{severity}

PREVIOUS INCIDENT EXPERIENCE FROM HINDSIGHT:
{memory_context}

Your tasks:

1. Explain the incident in simple language.
2. Identify possible root causes.
3. Give practical troubleshooting steps in priority order.
4. Explain which checks should be performed first.
5. Use previous incident experience only when relevant.
6. Clearly distinguish evidence from assumptions.
7. Never claim that a possible cause is confirmed without evidence.
8. Mention important safety precautions before risky actions.

Use this exact structure:

INCIDENT SUMMARY:
LIKELY CAUSES:
PRIORITY CHECKS:
TROUBLESHOOTING STEPS:
PREVIOUS INCIDENT LEARNING:
CONFIDENCE:
SAFETY NOTES:

Keep the answer practical and clear.
"""

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a careful and evidence-based "
                        "IT operations incident analyst."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            max_tokens=1500
        )

        result = response.choices[0].message.content

        if not result:
            raise ValueError("The AI returned an empty response.")

        return result.strip()

    except Exception as error:
        raise RuntimeError(
            f"Groq incident analysis failed: {error}"
        ) from error