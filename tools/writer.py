import os, json, re
from google import genai
from dotenv import load_dotenv
load_dotenv()

def write(topic: str, articles: list[dict]) -> dict:
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        print("Error: GEMINI_API_KEY missing from .env")
        raise SystemExit(1)
    client = genai.Client(api_key=key)
    articles_text = "\n".join(
        f"- {a.get('title','')}: {a.get('snippet','')}" for a in articles
    )
    prompt = (
        f"Write a newsletter about \"{topic}\" based on these reference articles:\n"
        f"{articles_text}\n\n"
        "Return ONLY a JSON object with this shape:\n"
        "{\"headline\": \"...\", \"sections\": [{\"title\": \"...\", \"body\": \"...\"}], \"cta_text\": \"...\"}\n"
        "No markdown, no extra text. Just the JSON."
    )
    try:
        response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        text = response.text
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
        return json.loads(text)
    except Exception as e:
        print(f"Gemini write failed, using fallback: {e}")
        return {
            "headline": f"Everything You Need to Know About {topic}",
            "sections": [
                {"title": "Introduction", "body": f"In this issue we explore {topic} — a topic that continues to shape how we think and build. Here is what matters most."},
                {"title": "Key Points", "body": f"Across the web, recent coverage highlights important developments around {topic}. We bring together the sharpest perspectives to give you a clear picture."},
                {"title": "Looking Ahead", "body": f"As {topic} evolves, staying informed helps you stay ahead. Bookmark this issue and watch this space for updates."},
            ],
            "cta_text": "Read more on the topic",
        }
