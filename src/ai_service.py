import os
from dotenv import load_dotenv
from openai import OpenAI

from src.prompt_templates import executive_summary_prompt

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def generate_executive_summary(metrics: dict) -> str:
    prompt = executive_summary_prompt(metrics)

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output_text