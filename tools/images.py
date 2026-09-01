import os, base64
from google import genai
from google.genai import types
from dotenv import load_dotenv
load_dotenv()

DEFAULT_IMAGE = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="

def _to_base64(data: bytes) -> str:
    return base64.b64encode(data).decode()

def generate_images(topic: str) -> list[str]:
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        print("Warning: GEMINI_API_KEY missing, using placeholder images")
        return [DEFAULT_IMAGE, DEFAULT_IMAGE]
    client = genai.Client(api_key=key)
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[f"Infographic style image about {topic}"],
            generation_config=types.GenerateContentConfig(response_modalities=["IMAGE"]),
        )
        images = []
        for cand in response.candidates:
            for part in cand.content.parts:
                if hasattr(part, "inline_data") and part.inline_data:
                    images.append(_to_base64(part.inline_data.data))
        if images:
            return images[:2]
        return [DEFAULT_IMAGE, DEFAULT_IMAGE]
    except Exception as e:
        print(f"Image generation failed, using placeholders: {e}")
        return [DEFAULT_IMAGE, DEFAULT_IMAGE]
