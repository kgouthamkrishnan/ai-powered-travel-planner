from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

client = Groq(
    api_key=api_key
)

def ask_ai(prompt):

    try:

        chat = client.chat.completions.create(

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            model="llama-3.1-8b-instant",

            temperature=0.7,

            max_tokens=800
        )

        return chat.choices[0].message.content

    except Exception as e:

        return f"""
AI service temporarily unavailable.

Reason:
{str(e)}

Please wait and try again.
"""