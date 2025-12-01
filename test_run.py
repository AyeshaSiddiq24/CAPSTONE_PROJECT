import asyncio

from researcher_agent import researcher_agent
from writer_agent import writer_agent
from supervisor_agent import supervisor_agent

topic = "Future of AI Agents"

print("\n=== TESTING RESEARCHER AGENT ===")
research_output = researcher_agent(topic)
print("Research Keys:", list(research_output.keys()))
print()

print("=== TESTING WRITER AGENT ===")
writer_output = writer_agent(research_output)
print("Writer Keys:", list(writer_output.keys()))
print()

print("=== TESTING SUPERVISOR AGENT ===")

# Run async supervisor_agent properly
final_output = asyncio.run(supervisor_agent(topic))

print("Supervisor Keys:", list(final_output.keys()))
print()
