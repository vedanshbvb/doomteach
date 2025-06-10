# tts.py

import os
import asyncio
import tempfile
import wave

from pydub import AudioSegment
from fakeyou import AsyncFakeYou

# Replace these if you want to default them here; or pass them in.
EMAIL = "vedanshbvb"
PASSWORD = "Ved@fakeyou"
LOG_FILE = os.path.join(os.path.dirname(__file__), "pipeline.log")

class TTSPipeline:
    def __init__(self, email=EMAIL, password=PASSWORD):
        self.email = email
        self.password = password
        self.fy = AsyncFakeYou()
        self._logged_in = False
    
    def log_line(self, line):
        with open(LOG_FILE, "a") as f:
            f.write(line)
            f.write("\n")

    async def _ensure_login(self):
        if not self._logged_in:
            await self.fy.login(self.email, self.password)
            self._logged_in = True

    async def _synthesize(self, text: str, token: str, out_path: str):
        """Generate speech for a single line and save to out_path."""
        await self._ensure_login()

        self.log_line(f"Synthesizing text: {text} with token: {token} to {out_path}")

        try:
            wav = await self.fy.say(text=text, ttsModelToken=token)
            with open(out_path, "wb") as f:
                f.write(wav.content)
        except Exception as e:
            self.log_line(f"ERROR: Failed to synthesize text '{text}' with token '{token}': {e}")
            return 0.0  # Return 0 duration on failure



        # get duration in seconds
        with wave.open(out_path, 'rb') as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            duration = frames / float(rate)
        return duration

    # def run(self, script_lines, tokens_map, out_dir="media/generated/audio"):
    #     """
    #     script_lines: list of tuples [(speaker, line_text), ...]
    #     tokens_map:     dict { speaker: fakeyou_token, ... }

    #     Returns:
    #       final_audio_path: str
    #       timeline: list of {speaker, start, duration, filename}
    #     """
    #     # prepare output directory
    #     tempdir = out_dir or tempfile.mkdtemp(prefix="tts_")
    #     timeline = []
    #     current_start = 0.0
    #     wav_files = []

    #     async def _process_all():
    #         nonlocal current_start
    #         for idx, item in enumerate(script_lines, start=1):
    #             if not (isinstance(item, tuple) and len(item) == 2):
    #                 continue  # skip malformed lines
    #             speaker, text = item
    #             token = tokens_map[speaker]
    #             fname = f"{speaker.lower().replace(' ', '_')}{idx}.wav"
    #             path = os.path.join(tempdir, fname)
    #             duration = await self._synthesize(text, token, path)
    #             timeline.append({
    #                 "speaker": speaker,
    #                 "start": current_start,
    #                 "duration": duration,
    #                 "filename": fname
    #             })
    #             wav_files.append(path)
    #             current_start += duration

    #     # run the async processing
    #     asyncio.run(_process_all())

    #     # merge all into one final track
    #     combined = AudioSegment.empty()
    #     for path in wav_files:
    #         clip = AudioSegment.from_wav(path)
    #         combined += clip

    #     final_path = os.path.join(tempdir, "final_audio.wav")
    #     combined.export(final_path, format="wav")

    #     return final_path, timeline


    def run(self, script_lines, tokens_map, out_dir="media/generated/audio"):
        self.log_line("entered run")
        # self.log_line(script_lines)
        import uuid  # to generate unique names

        tempdir = out_dir or tempfile.mkdtemp(prefix="tts_")
        timeline = []
        current_start = 0.0
        wav_files = []

        async def _process_all():
            nonlocal current_start
            for idx, (speaker, text) in enumerate(script_lines, start=1):
                token = tokens_map[speaker]
                # Ensure unique filename using UUID
                uid = uuid.uuid4().hex[:8]
                fname = f"{speaker.lower().replace(' ', '_')}_{idx}_{uid}.wav"
                path = os.path.join(tempdir, fname)

                await asyncio.sleep(2)  

                duration = await self._synthesize(text, token, path)
                if duration > 0:
                    self.log_line(f"Processed {speaker}: {text} -> {fname} ({duration:.2f}s)")
                    timeline.append({
                        "speaker": speaker,
                        "start": current_start,
                        "duration": duration,
                        "filename": fname
                    })
                    wav_files.append(path)
                    current_start += duration

        # Clear old event loops if any
        try:
            asyncio.run(_process_all())
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(_process_all())
            loop.close()

        # Merge final audio
        combined = AudioSegment.empty()
        for path in wav_files:
            clip = AudioSegment.from_wav(path)
            combined += clip

        final_path = os.path.join(tempdir, "final_audio.wav")
        combined.export(final_path, format="wav")

        return final_path, timeline
