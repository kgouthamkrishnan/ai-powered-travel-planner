
from ai.groq_engine import ask_ai

def generate_itinerary(destination, days, budget, style):
    prompt = f'''
    Create a detailed travel itinerary for:
    Destination: {destination}
    Days: {days}
    Budget: {budget}
    Style: {style}

    Include:
    - Attractions
    - Food recommendations
    - Transport suggestions
    - Clothing advice
    - Safety tips
    '''

    return ask_ai(prompt)
