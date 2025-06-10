import sys
import json
import os

from script_generator import generate_script, identify_characters
from voice_generator import get_token_for_character, voices
from tts import TTSPipeline

LOG_FILE = os.path.join(os.path.dirname(__file__), "pipeline.log")

def log_line(line):
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

def call_script_generator(user_prompt):
    script = generate_script(user_prompt)
    characters = identify_characters(user_prompt)
    return script, characters

def call_voice_generator(character_name):
    token, index = get_token_for_character(character_name, voices)
    return token, index

def my_pipeline_function(result, script):
    """
    result: dict with keys:
        - "characters": str, e.g. "Optimus Prime, Elon Musk"
        - "tokens": list of str, e.g. ["tok1", "tok2"]
        - "indices": list of int, e.g. [2532, 1046]
    script: list of (speaker, line) tuples
    """
    speakers = [c.strip() for c in result["characters"].split(",")]
    tokens = result["tokens"]
    token_map = dict(zip(speakers, tokens))

    tts = TTSPipeline()
    final_audio, timeline = tts.run(script, token_map)
    log_line(f"Final audio path: {final_audio}")
    log_line(f"Timeline: {json.dumps(timeline)}")

    return {
        "audio_path": final_audio,
        "timestamps": timeline
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        log_line("STATUS: No prompt provided.")
        print("STATUS: No prompt provided.", flush=True)
        sys.exit(1)
    user_prompt = sys.argv[1]
    log_line("STATUS: Generating script...")
    print("STATUS: Generating script...", flush=True)
    script, characters = call_script_generator(user_prompt)
    log_line(script)
    log_line("STATUS: Script generated.")
    print("STATUS: Script generated.", flush=True)
    char_list = [c.strip() for c in characters.split(',') if c.strip()] if characters else []
    tokens = []
    indices = []
    for character in char_list:
        log_line(f"STATUS: Converting text to voice for {character}...")
        print(f"STATUS: Converting text to voice for {character}...", flush=True)
        token, index = call_voice_generator(character)
        tokens.append(token)
        indices.append(index)
        # log_line("STATUS: Voice conversion done.")
        print("poop", flush=True)
    result = {
        # "script": script,  # Do not include script in output
        "characters": characters,
        "tokens": tokens,
        "indices": indices
    }

    # Parse the script JSON object into a list of (speaker, line) tuples
    if isinstance(script, str):
        try:
            script_dict = json.loads(script)
            parsed_script = [(speaker, line) for speaker, line in script_dict.items()]
            script = parsed_script
        except Exception as e:
            log_line(f"ERROR: Failed to parse script JSON: {e}")
            script = []

    tts_output = my_pipeline_function(result, script)
    log_line(json.dumps(tts_output))
    print(json.dumps(tts_output), flush=True)

    log_line(json.dumps(result))
    print(json.dumps(result), flush=True)
