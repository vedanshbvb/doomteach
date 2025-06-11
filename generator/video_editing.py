import moviepy.config as mpy_conf
mpy_conf.change_settings({"textclip_backend": "imagemagick"})


import os
import json
import subprocess
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, ImageClip, TextClip


def convert_mp3_to_wav(mp3_path, wav_path):
    """Converts MP3 to WAV using ffmpeg"""
    subprocess.run([
        "ffmpeg", "-y", "-i", mp3_path, wav_path
    ], check=True)



def create_video_with_stickers(tts_output, character_img_paths, char_list, bg_video_path, audio_path=None, output_dir="../media/generated/video/"):
    import os
    os.makedirs(output_dir, exist_ok=True)
    output_filename = "final_video.mp4"
    output_path = os.path.join(output_dir, output_filename)

    # Load background video
    video = VideoFileClip(bg_video_path)
    clips = [video]

    # Define position mapping
    position_map = {
        char_list[0]: ("left", 0.2),
        char_list[1]: ("right", 0.75),
    }

    # Overlay stickers and subtitles
    for entry in tts_output["timestamps"]:
        speaker = entry["speaker"]
        start = entry["start"]
        duration = entry["duration"]
        img_path = character_img_paths.get(speaker)

        # === STICKER IMAGE ===
        if img_path:
            sticker = (
                ImageClip(img_path)
                .set_start(start)
                .set_duration(duration)
                .resize(height=350)  # Increased size
                .set_position((position_map.get(speaker, ("center", 0.5))[1] * video.w, video.h - 350))  # custom horizontal
            )
            clips.append(sticker)

        # === SUBTITLES ===
        subtitle_text = entry.get("text", os.path.splitext(entry.get("filename", ""))[0])  # fallback from filename
        # subtitle = (
        #     TextClip(
        #         txt=subtitle_text,
        #         fontsize=40,
        #         color='white',
        #         font='Arial',  # Use simpler font name (no '-Bold' suffix)
        #         stroke_color='black',
        #         stroke_width=2,
        #         method='label',  # MUST use 'label' for PIL
        #         size=(video.w * 0.9, None)  # Constrain width to 90% of video
        #     )

        #     .set_start(start)
        #     .set_duration(duration)
        #     .set_position(("center", video.h - 100))  # Bottom-center
        # )
        # Calculate text width (90% of video width) and approximate height
        text_width = int(video.w * 0.9)
        text_height = 100  # Adjust based on your needs

        subtitle = (
            TextClip(
                txt=subtitle_text,
                fontsize=40,
                color='white',
                font='Arial-Bold',
                stroke_color='black',
                stroke_width=2,
                size=(text_width, text_height),
                align='center'
            )
            .set_duration(duration)
            .set_start(start)
            .set_position(('center', video.h - 120))
        )

        clips.append(subtitle)

    final = CompositeVideoClip(clips, size=video.size)

    # Add audio
    if not audio_path and "audio_path" in tts_output:
        audio_path = tts_output["audio_path"]
    if audio_path:
        # from . import convert_mp3_to_wav  # if this function is defined in same module
        
        wav_path = audio_path.replace(".mp3", ".wav")
        convert_mp3_to_wav(audio_path, wav_path)
        audio = AudioFileClip(wav_path)
        final = final.set_audio(audio)
        final = final.set_duration(audio.duration)

    # Export main video
    final.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac",
        temp_audiofile="temp-audio.m4a",
        remove_temp=True
    )

    # Replace final audio if needed
    if audio_path:
        final_audio = AudioFileClip(audio_path)
        final_video = VideoFileClip(output_path)
        final_with_audio = final_video.set_audio(final_audio)
        output_final_path = os.path.join(output_dir, "final_video_final.mp4")
        final_with_audio.write_videofile(
            output_final_path,
            codec="libx264",
            audio_codec="aac",
            temp_audiofile="temp-audio.m4a",
            remove_temp=True
        )
        return output_final_path

    return output_path


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Create video with stickers overlay.")
    parser.add_argument("--tts_output", type=str, help="Path to TTS output JSON file")
    parser.add_argument("--character_img_paths", type=str, help="Path to character image paths JSON file")
    parser.add_argument("--char_list", type=str, help="Comma-separated list of character names")
    parser.add_argument("--bg_video_path", type=str, default="../media/bg_videos/vid1.mp4", help="Path to background video")
    parser.add_argument("--audio_path", type=str, help="Path to audio file (optional)")
    parser.add_argument("--output_dir", type=str, default="../media/generated/video", help="Folder where video will be saved")

    args = parser.parse_args()

    if args.tts_output and args.character_img_paths and args.char_list:
        with open(args.tts_output, "r") as f:
            tts_output = json.load(f)
        with open(args.character_img_paths, "r") as f:
            character_img_paths = json.load(f)
        char_list = [c.strip() for c in args.char_list.split(",") if c.strip()]
        audio_path = args.audio_path
    else:
        # Hardcoded fallback values for testing
        tts_output = {
            "audio_path": "../media/generated/audio/final_audio.mp3",
            "timestamps": [
                {"speaker": "Stewie", "start": 0.0, "duration": 1.51, "filename": "stewie_1.mp3"},
                {"speaker": "Barbie", "start": 1.51, "duration": 5.32, "filename": "barbie_2.mp3"},
                {"speaker": "Stewie", "start": 6.84, "duration": 4.54, "filename": "stewie_3.mp3"},
                {"speaker": "Barbie", "start": 11.38, "duration": 7.88, "filename": "barbie_4.mp3"},
                {"speaker": "Stewie", "start": 19.27, "duration": 2.11, "filename": "stewie_5.mp3"},
                {"speaker": "Barbie", "start": 21.39, "duration": 6.68, "filename": "barbie_6.mp3"},
                {"speaker": "Stewie", "start": 28.08, "duration": 2.63, "filename": "stewie_7.mp3"},
                {"speaker": "Barbie", "start": 30.72, "duration": 12.43, "filename": "barbie_8.mp3"},
                {"speaker": "Stewie", "start": 43.15, "duration": 4.85, "filename": "stewie_9.mp3"},
                {"speaker": "Barbie", "start": 48.01, "duration": 10.63, "filename": "barbie_10.mp3"},
                {"speaker": "Stewie", "start": 58.64, "duration": 3.78, "filename": "stewie_11.mp3"},
                {"speaker": "Barbie", "start": 62.43, "duration": 8.17, "filename": "barbie_12.mp3"},
                {"speaker": "Stewie", "start": 70.60, "duration": 4.44, "filename": "stewie_13.mp3"},
                {"speaker": "Barbie", "start": 75.04, "duration": 4.20, "filename": "barbie_14.mp3"},
                {"speaker": "Stewie", "start": 79.25, "duration": 2.40, "filename": "stewie_15.mp3"},
                {"speaker": "Barbie", "start": 81.65, "duration": 2.82, "filename": "barbie_16.mp3"},
                {"speaker": "Stewie", "start": 84.48, "duration": 0.83, "filename": "stewie_17.mp3"},
                {"speaker": "Barbie", "start": 85.31, "duration": 1.20, "filename": "barbie_18.mp3"}
            ]
        }
        character_img_paths = {
            "Stewie": "../media/stickers/stewiegriffin.png",
            "Barbie": "../media/stickers/barbie.png"
        }
        char_list = ["Stewie", "Barbie"]
        audio_path = tts_output["audio_path"]

    out_path = create_video_with_stickers(
        tts_output,
        character_img_paths,
        char_list,
        args.bg_video_path,
        audio_path=audio_path,
        output_dir=args.output_dir
    )
    print(f"✅ Video created at: {out_path}")
