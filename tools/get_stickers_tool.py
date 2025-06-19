from google.adk.tools import FunctionTool
import os
from generator.get_stickers import download_character_stickers

class GetStickersTool(FunctionTool):
    """
    ADK Tool for downloading character stickers given a list of character names.
    """
    def __init__(self):
        def get_stickers(characters: list) -> dict:
            """
            Downloads stickers for the given characters and returns a dict of character->image path.

            Args:
                characters (list): List of character names.
            Returns:
                dict: Mapping of character name to image path (or None if not found).
            """
            return download_character_stickers(characters)
        super().__init__(func=get_stickers)
