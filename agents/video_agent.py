from google.adk.agents import LlmAgent
from tools.get_stickers_tool import GetStickersTool
from tools.video_editing_tool import VideoEditingTool
from tools.add_subtitles_tool import AddSubtitlesTool
import os

get_stickers_tool = GetStickersTool()
video_editing_tool = VideoEditingTool()
add_subtitles_tool = AddSubtitlesTool()

VideoAgent = LlmAgent(
    name="video_agent",
    model=os.environ.get("AGENT_MODEL", "gemini-2.0-flash"),
    description="Agent that creates a video with stickers and subtitles using the provided tools.",
    instruction="""
    You are an agent that creates a video for a social media reel. Use the 'get_stickers_tool' to fetch character stickers, 'video_editing_tool' to compose the video, and 'add_subtitles_tool' to overlay subtitles. 
    
    Important: When using the video_editing_tool, always use the default background video path "media/bg_videos/vid1.mp4" or leave it unspecified to use the default. Do not use any other background video paths.
    
    Accept all required parameters and return the final video path.
    """,
    tools=[get_stickers_tool, video_editing_tool, add_subtitles_tool],
)
