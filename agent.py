from google.adk.agents import BaseAgent
from google.adk.events.event import Event

from researcher_agent import researcher_agent
from writer_agent import writer_agent
from supervisor_agent import supervisor_agent


class Agent(BaseAgent):
    name: str = "startup_sense_ai"

    async def _run_async_impl(self, event_stream):
        first_event = await event_stream.__anext__()
        topic = (first_event.input_text or "future of AI agents").strip()

        yield Event(author=self.name, text=f"🔍 Starting work on: {topic}")

        research = researcher_agent(topic)
        yield Event(author=self.name, text="📚 Research complete.")

        report = writer_agent(research)
        yield Event(author=self.name, text="✍️ Report drafted.")

        final = await supervisor_agent(topic)
        yield Event(author=self.name, text="🎯 Supervisor finished reviewing.")

        final_text = (
f"========================\n"
f"📊 FINAL OUTPUT FOR: {topic}\n"
f"========================\n\n"
f"🧠 Research Summary:\n{research.get('summary','N/A')}\n\n"
f"📘 Report Preview:\n{report.get('report','N/A')[:800]}...\n\n"
f"👨‍⚖️ Supervisor Summary:\n{final.get('short_summary','N/A')}\n"
        )

        yield Event(author=self.name, text=final_text)
