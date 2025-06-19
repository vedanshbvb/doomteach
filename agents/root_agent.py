from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool
import os

from agents.script_agent import ScriptAgent
from agents.identify_characters_agent import IdentifyCharactersAgent
from agents.voice_agent import VoiceAgent
from agents.video_agent import VideoAgent
from agents.publish_agent import PublishAgent
from agents.analytics_agent import AnalyticsAgent

RootAgent = LlmAgent(
    name="root_agent",
    model=os.environ.get("AGENT_MODEL", "gemini-2.0-flash"),
    description="Coordinator agent that orchestrates the full video generation and publishing pipeline.",
    instruction="""
    You are the coordinator agent for a multi-step video generation pipeline. For each user prompt, you must:
    1. Use the ScriptAgent to generate a script.
    2. Use the IdentifyCharactersAgent to extract character names.
    3. Use the VoiceAgent to generate audio and timeline from the script and characters.
    4. Use the VideoAgent to fetch stickers, compose the video, and add subtitles.
    5. Optionally use the PublishAgent to publish the video.
    6. Optionally use the AnalyticsAgent to fetch analytics for published videos.
    Always reason about which agent/tool to call next, and pass outputs as needed. Return the final video path or analytics as appropriate.
    """,
    tools=[
        AgentTool(agent=ScriptAgent),
        AgentTool(agent=IdentifyCharactersAgent),
        AgentTool(agent=VoiceAgent),
        AgentTool(agent=VideoAgent),
        AgentTool(agent=PublishAgent),
        AgentTool(agent=AnalyticsAgent),
    ],
)
