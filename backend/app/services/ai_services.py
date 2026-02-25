import os
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

PROVIDER = os.getenv("AI_PROVIDER", "gemini")


def summarize_text(text: str) -> str:
    if not text or not text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    try:
        if PROVIDER == "gemini":
            return _summarize_with_gemini(text)

        elif PROVIDER == "openai":
            return _summarize_with_openai(text)

        else:
            raise HTTPException(
                status_code=500,
                detail="Invalid AI provider configured"
            )

    except HTTPException:
        raise  # re-raise clean FastAPI errors

    except Exception as e:
        # Unknown failure → treat as upstream provider issue
        raise HTTPException(
            status_code=502,
            detail=f"AI provider error: {str(e)}"
        )


# ---------------- GEMINI ---------------- #

def _summarize_with_gemini(text: str) -> str:
    try:
        from google import genai

        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise HTTPException(
                status_code=500,
                detail="GEMINI_API_KEY not configured"
            )

        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Summarize this note clearly and concisely:\n\n{text}",
        )

        if not response or not response.text:
            raise Exception("Empty response from Gemini")

        return response.text.strip()

    except HTTPException:
        raise

    except Exception as e:
        raise Exception(f"Gemini error: {str(e)}")


# ---------------- OPENAI ---------------- #

def _summarize_with_openai(text: str) -> str:
    try:
        from openai import OpenAI

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise HTTPException(
                status_code=500,
                detail="OPENAI_API_KEY not configured"
            )

        client = OpenAI(api_key=api_key)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes notes clearly and concisely."
                },
                {
                    "role": "user",
                    "content": f"Summarize this note:\n\n{text}"
                }
            ],
            temperature=0.5,
        )

        content = response.choices[0].message.content

        if not content:
            raise Exception("Empty response from OpenAI")

        return content.strip()

    except HTTPException:
        raise

    except Exception as e:
        raise Exception(f"OpenAI error: {str(e)}")