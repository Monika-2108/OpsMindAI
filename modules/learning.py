import os
import re

from dotenv import load_dotenv
from groq import Groq

from database.db import get_all_incidents

from modules.memory_engine import (
    retain_incident,
    recall_incidents
)

load_dotenv()


def remember_resolved_incident(incident):
    return retain_incident(
        incident_id=incident["id"],
        title=incident["title"],
        description=incident["description"],
        suggested_solution=incident["suggested_solution"] or "",
        actual_solution=incident["actual_solution"] or "",
        outcome=incident["outcome"],
        root_cause=incident["root_cause"] or ""
    )


def find_similar_incidents(query):
    """
    Try Hindsight first.
    If unavailable, search local SQLite incident history.
    """

    try:
        return recall_incidents(query)

    except Exception:
        incidents = get_all_incidents()

        if not incidents:
            return "No incidents are stored in the local database."

        keywords = set(
            re.findall(r"[a-zA-Z0-9]+", query.lower())
        )

        stop_words = {
            "the", "and", "for", "with", "from",
            "what", "where", "when", "should",
            "could", "would", "find", "previous",
            "incident", "incidents", "problem",
            "remember", "show", "me", "our"
        }

        keywords -= stop_words

        matches = []

        for incident in incidents:
            record = dict(incident)

            searchable_text = " ".join(
                str(record.get(field) or "")
                for field in [
                    "title",
                    "description",
                    "severity",
                    "suggested_solution",
                    "actual_solution",
                    "root_cause",
                    "outcome"
                ]
            ).lower()

            score = sum(
                1 for word in keywords
                if word in searchable_text
            )

            if score > 0:
                matches.append((score, record))

        matches.sort(
            key=lambda item: (
                item[0],
                item[1].get("id", 0)
            ),
            reverse=True
        )

        if not matches:
            return (
                "No closely matching incidents found. "
                "Here are the latest locally stored incidents:"
                + str([dict(item) for item in incidents[:5]])
            )

        return [
            {
                "source": "Local SQLite",
                "match_score": score,
                "incident": record
            }
            for score, record in matches[:5]
        ]


def generate_learning_insights(query):
    """
    Generate learning insights from resolved SQLite incidents
    using Groq. Does not require Hindsight credits.
    """

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is missing. Check your .env file."
        )

    model = os.getenv(
        "GROQ_MODEL",
        "openai/gpt-oss-120b"
    )

    incidents = get_all_incidents()

    resolved_incidents = [
        dict(incident)
        for incident in incidents
        if str(incident["outcome"] or "").lower() == "resolved"
    ]

    if not resolved_incidents:
        return "No resolved incidents are available yet."

    client = Groq(api_key=api_key)

    prompt = f"""
You are OpsMind AI, an IT operations learning assistant.

Analyze these resolved incidents from SQLite:

{resolved_incidents}

USER QUESTION:
{query}

Create a report containing:

1. INCIDENT PATTERNS
2. ROOT-CAUSE ANALYSIS
3. SUCCESSFUL RESOLUTION STRATEGIES
4. PREVENTIVE RECOMMENDATIONS
5. OPERATIONAL IMPROVEMENTS
6. KEY LEARNINGS

IMPORTANT:
- Use only evidence present in the incident records.
- Do not invent logs, metrics, or verification steps.
- Do not claim recurring patterns from one incident.
- Clearly separate confirmed facts from recommendations.
- Keep the report practical and understandable.
"""

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an evidence-based IT "
                        "operations learning assistant."
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
            raise ValueError(
                "The AI returned an empty learning report."
            )

        return result.strip()

    except Exception as error:
        raise RuntimeError(
            f"Groq learning analysis failed: {error}"
        ) from error