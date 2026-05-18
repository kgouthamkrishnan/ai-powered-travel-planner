from ai.groq_engine import ask_ai

# CULTURE ENGINE

def generate_culture_info(
    destination,
    style
):

    try:

        prompt = f"""
        You are a travel culture expert.

        Generate destination-specific cultural guidance.

        Destination:
        {destination}

        Travel Style:
        {style}

        IMPORTANT:

        DO NOT include:
        - clothing suggestions
        - safety tips
        - travel essentials

        ONLY provide:

        1. Local Culture
        2. Traditions
        3. Festivals
        4. Local Food Habits
        5. Tourist Etiquette
        6. Local Experiences
        7. Cultural Tips
        8. Local Lifestyle

        Complete all sentences properly.
        Keep formatting clean.
        """

        response = ask_ai(prompt)

        if response:

            return response

        return "Culture information currently unavailable."

    except Exception:

        return "Unable to generate culture information right now."