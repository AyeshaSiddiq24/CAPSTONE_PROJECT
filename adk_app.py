from google.adk.apps.app import App
from agent import Agent

app = App(
    root_agent=Agent(),
    name="startup_sense_ai"
)

__all__ = ["app"]
