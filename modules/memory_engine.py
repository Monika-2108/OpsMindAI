import os

from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

BANK_ID = "opsmind"

_client = None


def get_memory_client():
    global _client

    if _client is None:
        api_key = os.getenv("HINDSIGHT_API_KEY")
        base_url = os.getenv(
            "HINDSIGHT_BASE_URL",
            "https://api.hindsight.vectorize.io"
        )

        if not api_key:
            raise ValueError(
                "HINDSIGHT_API_KEY is missing in .env"
            )

        _client = Hindsight(
            base_url=base_url,
            api_key=api_key
        )

    return _client


def retain_incident(
    incident_id,
    title,
    description,
    suggested_solution,
    actual_solution,
    outcome,
    root_cause
):
    content = f"""
OPS MIND INCIDENT EXPERIENCE

Incident ID: {incident_id}
Title: {title}
Description: {description}

AI Suggested Solution:
{suggested_solution}

Actual Action Taken:
{actual_solution}

Outcome:
{outcome}

Confirmed Root Cause:
{root_cause}

Learning:
Remember what was attempted, whether it worked,
and what evidence confirmed the root cause.
"""

    return get_memory_client().retain(
        bank_id=BANK_ID,
        content=content,
        context="IT incident troubleshooting experience"
    )


def recall_incidents(query):
    return get_memory_client().recall(
        bank_id=BANK_ID,
        query=query
    )


def reflect_on_incidents(query):
    return get_memory_client().reflect(
        bank_id=BANK_ID,
        query=query
    )