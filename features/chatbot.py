from ai.groq_engine import ask_ai


def travel_chat(user_message, destination=None):

    prompt = f'''
    You are an intelligent AI travel assistant.

    Destination: {destination}

    User Message: {user_message}

    Behave like a friendly travel guide.

    Help users with:
    - travel planning
    - tourist places
    - local food
    - safety
    - transport
    - hotels
    - culture
    - budgeting
    - weather guidance

    Keep answers conversational and easy to understand.
    '''

    return ask_ai(prompt)