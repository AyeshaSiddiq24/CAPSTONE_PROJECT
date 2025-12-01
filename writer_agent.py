from dotenv import load_dotenv
import os
import google.generativeai as genai
import traceback

# Load env
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-2.0-flash")
else:
    print("⚠️ Warning: GEMINI_API_KEY not found. Writer agent may not run properly.")
    model = None


def safe_generate(prompt: str):
    """
    A safe synchronous wrapper around Gemini calls.
    Ensures: 
      - no async conflicts
      - catches failures
      - always returns a string
    """
    if model is None:
        return "⚠️ Gemini unavailable — no API key."

    try:
        response = model.generate_content(prompt)

        # Extract text
        if hasattr(response, "text") and response.text:
            return response.text

        # Cold fallback
        if hasattr(response, "candidates"):
            parts = response.candidates[0].content.parts
            return "\n".join(
                p.text for p in parts if hasattr(p, "text")
            )

        return "(No text returned.)"

    except Exception as e:
        print("Writer Agent Error:", e)
        traceback.print_exc()
        return f"ERROR from Gemini: {e}"


def writer_agent(research_output, mode="all"):
    """
    Writer Agent (SYNC + ADK SAFE)
    Generates:
      - Full report
      - 6-bullet summary
      - Slide deck outline
      - LinkedIn post
    """

    if model is None:
        return {"error": "Gemini model unavailable – missing API key."}

    topic = research_output.get("topic", "")
    keypoints = research_output.get("keypoints", "")
    summary_text = research_output.get("summary", "")

    outputs = {}

    # -------------------------------
    # FULL REPORT
    # -------------------------------
    prompt_report = f"""
Write a detailed, structured full report on the topic "{topic}" using these extracted keypoints:

{keypoints}

Include these sections:
1. Introduction  
2. Key Insights  
3. Deep Analysis  
4. Conclusion  
"""
    outputs["report"] = safe_generate(prompt_report)

    # -------------------------------
    # EXECUTIVE SUMMARY (6 BULLETS)
    # -------------------------------
    prompt_summary = f"""
Summarize the topic "{topic}" using this information:

{summary_text}

Write EXACTLY 6 concise bullet points.
"""
    outputs["summary"] = safe_generate(prompt_summary)

    # -------------------------------
    # SLIDE DECK OUTLINE (10 SLIDES)
    # -------------------------------
    prompt_slides = f"""
Create a 10-slide presentation outline for the topic "{topic}".

Each slide MUST have:
- Slide title
- 3 to 5 bullet points
- No long paragraphs
- Professional, clean formatting
"""
    outputs["slides"] = safe_generate(prompt_slides)

    # -------------------------------
    # LINKEDIN POST (VIRAL STYLE)
    # -------------------------------
    prompt_linkedin = f"""
Write a viral LinkedIn post about the topic "{topic}".

Rules:
- Start with a strong hook.
- Add 3–5 insights in short bullet points.
- Tone: professional, inspiring, shareable.
- End with 5 relevant hashtags.
"""
    outputs["linkedin"] = safe_generate(prompt_linkedin)

    return outputs
