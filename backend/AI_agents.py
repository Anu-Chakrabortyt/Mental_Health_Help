from backend.tools import query_medgemma


SYSTEM_PROMPT = """
You are a warm and supportive mental health assistant.

Respond naturally and empathetically to the user's questions.

For location-related requests, provide relevant mental health
resources and helplines.
"""


def ask_mental_health_specialist(query: str) -> str:
    return query_medgemma(query)


def process_query(query: str) -> tuple[str, str]:
    response = query_medgemma(query)
    return response, "ask_mental_health_specialist"


if __name__ == "__main__":
    print("🧠 MedGemma initialized successfully!")