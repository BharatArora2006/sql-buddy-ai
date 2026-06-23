import os

from groq import Groq
from dotenv import load_dotenv
import time

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_sql(prompt):

    primary_model = "llama-3.3-70b-versatile"
    fallback_model = "llama3-8b-8192"

    # Try primary model 3 times

    for attempt in range(3):

        try:

            response = client.chat.completions.create(
                model=primary_model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0
            )

            print(f"Using model: {primary_model}")

            return response.choices[0].message.content

        except Exception as e:

            print(
                f"Primary model failed - Attempt {attempt + 1}"
            )

            print(str(e))

            time.sleep(2 ** attempt)

    # Fallback model

    try:

        print(
            f"Switching to fallback model: {fallback_model}"
        )

        response = client.chat.completions.create(
            model=fallback_model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        return response.choices[0].message.content

    except Exception as e:

        print("Fallback model failed")
        print(str(e))

        raise Exception(
            "AI service is temporarily unavailable. Please try again in a few moments."
        )