from ai.groq_engine import ask_ai

# SMART RECOMMENDATION ENGINE

def generate_recommendations(
    destination,
    budget,
    style,
    days
):

    prompt = f"""
    You are an intelligent travel recommendation engine.

    Generate smart personalized recommendations.

    Destination:
    {destination}

    Budget:
    {budget}

    Travel Style:
    {style}

    Trip Duration:
    {days} days

    IMPORTANT:

    DO NOT create day-wise itinerary.

    DO NOT mention:
    Day 1
    Day 2
    Day 3

    Instead provide:

    - hidden gems
    - must try experiences
    - best cafes
    - photography spots
    - adventure activities
    - shopping areas
    - local foods
    - romantic places
    - peaceful places
    - nightlife suggestions
    - local travel hacks
    - tourist mistakes to avoid
    - best sunrise/sunset points
    - underrated places

    Make recommendations modern,
    practical and tourist friendly.
    """

    return ask_ai(prompt)