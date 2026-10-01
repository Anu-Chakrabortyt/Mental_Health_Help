import ollama
from geopy.geocoders import Nominatim


def query_medgemma(prompt: str) -> str:
    """
    Calls the MedGemma model and returns the response.
    """

    system_prompt = """
You are Dr. Emily Hartman, a warm and experienced clinical psychologist.

Respond to patients with:
1. Emotional attunement
2. Gentle normalization
3. Practical guidance
4. Strengths-focused support

Key principles:
- Never use brackets or labels
- Blend the elements naturally
- Use natural transitions
- Mirror the user's language level
- Ask open-ended questions when appropriate
- Do not diagnose the user
"""

    try:
        response = ollama.chat(
            model="alibayram/medgemma:4b",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            options={
                "temperature": 0.7,
                "num_predict": 300
            }
        )

        return response["message"]["content"].strip()

    except Exception as e:
        return (
            "I'm having technical difficulties accessing my resources. "
            f"Please try again later. Error: {str(e)}"
        )


def find_nearby_mental_health_resources(location: str) -> str:
    """
    Finds mental-health resources based on the user's location.
    """

    if not location.strip():
        return "Please provide a valid location."

    geolocator = Nominatim(
        user_agent="mental_health_agent_assistant"
    )

    try:
        geo_data = geolocator.geocode(
            location,
            addressdetails=True
        )

        if geo_data:
            resolved_address = geo_data.address
            country = geo_data.raw.get("address", {}).get(
                "country",
                ""
            )
        else:
            resolved_address = f"{location} (Approximate)"
            country = "Unknown"

    except Exception:
        resolved_address = location
        country = "Unknown"

    national_resources = (
        "IMMEDIATE CRISIS SUPPORT:\n"
        "• Tele-MANAS: Call 14416 or 1800-891-4416\n"
        "• KIRAN Mental Health Helpline: 1800-599-0019\n"
        "• Vandrevala Foundation: +91 9999 666 555\n"
        "• AASRA: +91 9820466726\n\n"
    )

    local_referrals = (
        f"LOCATION: {resolved_address}\n"
        f"COUNTRY: {country}\n\n"
        "For nearby mental-health professionals, "
        "please search for licensed psychologists, "
        "psychiatrists, hospitals, or mental-health clinics "
        "in your local area.\n\n"
        "If you are in immediate danger or think you may "
        "hurt yourself or someone else, contact emergency "
        "services or a crisis helpline immediately."
    )

    return national_resources + local_referrals


if __name__ == "__main__":
    print(
        query_medgemma(
            "I feel anxious and overwhelmed with my work."
        )
    )

    print(
        find_nearby_mental_health_resources(
            "Kulti, West Bengal"
        )
    )
