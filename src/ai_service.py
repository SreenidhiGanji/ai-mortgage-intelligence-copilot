import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def generate_test_response() -> str:
    response = client.responses.create(
        model="gpt-4.1-mini",
        input="Explain mortgage denial rate in one simple sentence."
    )

    return response.output_text