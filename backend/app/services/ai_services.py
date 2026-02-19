import os
from openai import OpenAI


def summarize_text(text: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY not found")

    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes notes clearly and concisely."},
            {"role": "user", "content": f"Summarize this note:\n\n{text}"}
        ],
        temperature=0.5,
    )

    return response.choices[0].message.content
