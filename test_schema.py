# test_schema.py
from tools.get_stickers_tool import GetStickersTool
from google.adk.agents import LlmAgent

tool = GetStickersTool()

agent = LlmAgent(
    name="test_agent",
    model="gemini-2.0-flash",
    tools=[tool],
)
