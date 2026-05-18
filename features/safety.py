from ai.groq_engine import ask_ai

# =====================================================
# SAFETY ENGINE
# =====================================================

def generate_safety_tips(
    destination,
    style,
    weather
):

    try:

        prompt = f"""
        You are a professional travel safety advisor.

        Generate destination-specific travel safety guidance.

        Destination:
        {destination}

        Travel Style:
        {style}

        Current Weather:
        {weather}

        ONLY provide:

        1. Safety Tips
        2. Travel Essentials
        3. Clothing Suggestions
        4. Weather Precautions
        5. Emergency Guidance
        6. Health Precautions

        Complete all sentences properly.
        Keep formatting clean.
        """

        response = ask_ai(prompt)

        if response:

            return response

        return "Safety information currently unavailable."

    except Exception:

        return "Unable to generate safety information right now."