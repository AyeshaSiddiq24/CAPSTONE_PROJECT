from dotenv import load_dotenv
import os
from ddgs import DDGS
import google.generativeai as genai

# Load environment
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)
    gemini_model = genai.GenerativeModel("gemini-2.0-flash")
else:
    gemini_model = None
    print("⚠️ GEMINI_API_KEY missing. Research summaries will be limited.")


def web_search(query, max_results=5):
    """DuckDuckGo text search."""
    try:
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=max_results)
            cleaned = []

            for r in results:
                cleaned.append({
                    "title": r.get("title"),
                    "body": r.get("body"),
                    "url": r.get("href")
                })

            return cleaned
    except Exception as e:
        print(f"Error during DDG search: {e}")
        return []


def extract_keypoints(text, k=5):
    """Extract bullet-point key ideas."""
    sentences = text.split(".")
    points = []

    for s in sentences:
        if len(points) >= k:
            break
        if len(s.split()) > 6:
            points.append("• " + s.strip())

    return "\n".join(points)


def researcher_agent(topic):
    """
    Researcher Agent (SYNC)
    Performs:
    1. Web search
    2. Extract keypoints
    3. Gemini summary (if API available)
    """
    print(f"\n🔍 Researcher Agent Working on: {topic}\n")

    # Step 1 — Web Search
    results = web_search(topic, max_results=5)
    combined_text = "\n".join([r["body"] or "" for r in results])

    # Step 2 — Extract key points
    keypoints = extract_keypoints(combined_text)

    # Step 3 — Gemini Summary
    if gemini_model is None:
        summary = "⚠️ Gemini API key missing — cannot produce summary."
    else:
        prompt = f"""
Summarize the following information about "{topic}".
Include:
- 5–7 bullet points
- A short paragraph

Information:
{combined_text}
"""

        try:
            response = gemini_model.generate_content(prompt)
            summary = response.text
        except Exception as e:
            summary = f"⚠️ Gemini request failed: {e}"

    print("✅ Researcher Agent Ready!")

    return {
        "topic": topic,
        "keypoints": keypoints,
        "summary": summary,
        "sources": results
    }
