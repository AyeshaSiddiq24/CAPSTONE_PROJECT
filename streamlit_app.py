import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Load Gemini API Key safely
key = os.getenv("GEMINI_API_KEY")
if key:
    os.environ["GEMINI_API_KEY"] = key

import streamlit as st
import asyncio
from supervisor_agent import supervisor_agent
from ppt_generator import create_ppt


# ---------------------------------------
# Streamlit Page Configuration
# ---------------------------------------
st.set_page_config(
    page_title="AI Multi-Agent Research System",
    layout="wide"
)

st.title("🤖 Multi-Agent AI Research & Content Generator")
st.write("Enter any topic and the agents will research, summarize, and generate structured content.")


# ---------------------------------------
# Input Box
# ---------------------------------------
topic = st.text_input("Enter your topic:")


# ---------------------------------------
# Safe async runner for Streamlit
# ---------------------------------------
def run_async(coro):
    """
    Safely run an async coroutine inside Streamlit 
    without causing event loop conflicts.
    """
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            new_loop = asyncio.new_event_loop()
            return new_loop.run_until_complete(coro)
        else:
            return loop.run_until_complete(coro)
    except RuntimeError:
        return asyncio.run(coro)



# ---------------------------------------
# Button Action
# ---------------------------------------
if st.button("Generate"):
    if not topic.strip():
        st.error("Please enter a topic.")
    else:
        with st.spinner("Agents are working... 🔍🤖"):
            result = run_async(supervisor_agent(topic))

        st.success("Generation complete!")

        # ---------------------------------------
        # Display Results
        # ---------------------------------------
        st.header("📘 Full Report")
        st.write(result.get("full_report", "No full report available."))

        st.header("📝 Summary")
        st.write(result.get("short_summary", "No summary available."))

        st.header("🧠 Keypoints")
        st.write(result.get("keypoints", "No keypoints available."))

        st.header("📚 Research Summary")
        st.write(result.get("research_summary", "No research summary available."))

        st.header("📽 Slide Deck Outline")
        st.write(result.get("slides", "No slides available."))

        st.header("💼 LinkedIn Post")
        st.write(result.get("linkedin", "No LinkedIn post generated."))

        # ---------------------------------------
        # PowerPoint Generation & Download
        # ---------------------------------------
        st.header("📥 Download Presentation")

        ppt_filename = create_ppt(result.get("slides", ""), filename="AI_Slides.pptx")

        with open(ppt_filename, "rb") as f:
            st.download_button(
                label="📥 Download PowerPoint (.pptx)",
                data=f,
                file_name="AI_Slides.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
            )
