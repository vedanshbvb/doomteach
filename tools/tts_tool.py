# from sqlite3 import _Parameters
from google.adk.tools import FunctionTool
import os
from dotenv import load_dotenv
from google.genai.types import Schema
from generator.tts2 import TTSPipeline

load_dotenv()

def log_line(line):
    log_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "run_pipeline.log")
    with open(log_file, "a") as f:
        f.write(line + "\n")

class TTSTool(FunctionTool):
    """
    ADK Tool for running TTS on a script and returning audio path and timeline.
    """
    def __init__(self):
        async def tts_tool(script: list[list[str]]) -> dict:
            """
            Converts a script (list of [speaker, line] lists) to audio using TTS and returns audio path and timeline.

            Args:
                script (list[list[str]]): List of [speaker, line] lists.

            Returns:
                dict: {"audio_path": str, "timestamps": list}
            """
            tts = TTSPipeline()
            log_line("STATUS: Starting script generation...")
            final_audio, timeline = await tts.run(script)
            return {"audio_path": final_audio, "timestamps": timeline}

        schema = {
            "type": "object",
            "properties": {

                "script": {
                    "type": "array",
                    "items": {
                        "type": "array",
                        "items": [
                            {"type": "string"},  # speaker
                            {"type": "string"}   # line
                        ],
                        "minItems": 2,
                        "maxItems": 2
                    },
                    "description": "List of [speaker, line] pairs."
                }
            },
            "required": ["script"]
        }


        super().__init__(func=tts_tool)
