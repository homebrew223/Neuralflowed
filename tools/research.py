import os, json, re
import requests
from dotenv import load_dotenv
load_dotenv()

def research(topic: str, n: int = 5) -> list[dict]:
    key = os.getenv("SERPER_API_KEY")
    if not key:
        print("Error: SERPER_API_KEY missing from .env")
        raise SystemExit(1)
    url = "https://google.serper.dev/search"
    try:
        resp = requests.post(url, json={"q": topic, "num": n}, headers={"X-API-KEY": key}, timeout=30)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"Serper API error: {e}")
        raise SystemExit(1)
    results = data.get("organicResults", data.get("newsResults", []))
    articles = []
    for r in results[:n]:
        articles.append({
            "title": r.get("title", ""),
            "url": r.get("link", ""),
            "snippet": r.get("snippet", ""),
        })
    return articles
