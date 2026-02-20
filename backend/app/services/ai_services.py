import os
from dotenv import load_dotenv

load_dotenv()

PROVIDER = "gemini"

def summarize_text(text: str) -> str:
    if PROVIDER == "gemini":
        return _summarize_with_gemini(text)
    elif PROVIDER == "openai":
        return _summarize_with_openai(text)
    else:
        raise ValueError("Invalid AI provider selected")
    
def _summarize_with_gemini(text: str) -> str:
    from google import genai

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found")
    
    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"Summarize this note clearly and concisely:\n\n{text}",
    )

    return response.text


def _summarize_with_openai(text: str) -> str:
    from openai import OpenAI

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found")
    
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes notes closely and concisely."},
            {"role": "user", "content": f"Summarize this note:\n\n{text}"}
        ],
        temperature=0.5,
    )

    return response.choices[0].message.content