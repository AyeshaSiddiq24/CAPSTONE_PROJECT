from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    print("⚠️ Warning: GEMINI_API_KEY missing. Supervisor agent may have limited output.")

# Import sub-agents (sync)
from researcher_agent import researcher_agent
from writer_agent import writer_agent


async def supervisor_agent(user_query: str):
    """
    Supervisor Agent:
    - Runs Researcher Agent (sync)
    - Runs Writer Agent (sync)
    - Combines everything into final output
    """

    # -----------------------
    # STEP 1 — Research Phase
    # -----------------------
    research_output = researcher_agent(user_query)

    if isinstance(research_output, dict) and "error" in research_output:
        return {
            "status": "error",
            "message": "Researcher Agent failed.",
            "details": research_output
        }

    # -----------------------
    # STEP 2 — Writer Phase
    # -----------------------
    writer_output = writer_agent(research_output)

    if isinstance(writer_output, dict) and "error" in writer_output:
        return {
            "status": "error",
            "message": "Writer Agent failed.",
            "details": writer_output
        }

    # -----------------------
    # FINAL COMBINED OUTPUT
    # -----------------------
    final_output = {
        "status": "success",
        "topic": user_query,

        # From Research Agent
        "research_summary": research_output.get("summary", ""),
        "keypoints": research_output.get("keypoints", ""),

        # From Writer Agent
        "full_report": writer_output.get("report", ""),
        "short_summary": writer_output.get("summary", ""),
        "slides": writer_output.get("slides", ""),
        "linkedin": writer_output.get("linkedin", ""),
    }

    return final_output
