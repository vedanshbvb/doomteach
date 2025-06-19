from google.adk.tools import FunctionTool
import os
from generator.video_editing import create_video_with_stickers

class VideoEditingTool(FunctionTool):
    """
    ADK Tool for creating a video with stickers overlay.
    """
    def __init__(self):
        def video_editing_tool(tts_output: dict, character_img_paths: dict, char_list: list, bg_video_path: str, audio_path: str, output_dir: str) -> str:
            """
            Creates a video with stickers overlay using the given parameters.

            Args:
                tts_output (dict): TTS output with timestamps.
                character_img_paths (dict): Mapping of character names to image paths.
                char_list (list): List of character names.
                bg_video_path (str): Path to background video.
                audio_path (str): Path to audio file.
                output_dir (str): Output directory for the video.
            Returns:
                str: Path to the generated video file.
            """
            return create_video_with_stickers(tts_output, character_img_paths, char_list, bg_video_path, audio_path, output_dir)
        super().__init__(func=video_editing_tool)
