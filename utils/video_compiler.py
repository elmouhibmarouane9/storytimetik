import os
import subprocess
import tempfile
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from typing import List, Dict, Any, Optional
import imageio_ffmpeg

FFMPEG_BIN = imageio_ffmpeg.get_ffmpeg_exe()

# TikTok standard vertical resolution: 1080 x 1920 (9:16)
DEFAULT_WIDTH = 720
DEFAULT_HEIGHT = 1280

def create_subtitled_frame(
    text: str,
    subtext: str,
    background_color: tuple = (18, 18, 24),
    highlight_color: tuple = (255, 0, 80), # TikTok Red-Pink
    width: int = DEFAULT_WIDTH,
    height: int = DEFAULT_HEIGHT,
    progress: float = 0.0
) -> np.ndarray:
    """
    Renders an optimized vertical 9:16 TikTok story card frame with text wrapping,
    dynamic contrast, progress bar, and visual indicators.
    """
    img = Image.new("RGB", (width, height), color=background_color)
    draw = ImageDraw.Draw(img)

    # Gradient background accent
    for y in range(0, int(height * 0.25)):
        alpha = int(45 * (1 - y / (height * 0.25)))
        draw.line([(0, y), (width, y)], fill=(alpha + 20, 20, 35))

    # Top brand header
    draw.text((width // 2, 80), "STORYTIME TIKTOK", fill=(120, 120, 130), anchor="mm")

    # Center text box / Card container
    card_margin = 40
    card_top = int(height * 0.30)
    card_bottom = int(height * 0.70)
    draw.rounded_rectangle(
        [(card_margin, card_top), (width - card_margin, card_bottom)],
        radius=24,
        fill=(30, 32, 42),
        outline=(255, 255, 255, 30),
        width=2
    )

    # Main text formatting with basic wrapping
    words = text.split()
    lines = []
    curr_line = []
    for w in words:
        curr_line.append(w)
        if len(" ".join(curr_line)) > 26:
            lines.append(" ".join(curr_line[:-1]))
            curr_line = [w]
    if curr_line:
        lines.append(" ".join(curr_line))

    # Render wrapped lines
    line_y = card_top + 60
    for l in lines[:6]:
        draw.text((width // 2, line_y), l, fill=(255, 255, 255), anchor="mm")
        line_y += 50

    # Subtext / Climax cue
    if subtext:
        draw.text((width // 2, card_bottom - 50), f"👉 {subtext}", fill=highlight_color, anchor="mm")

    # Bottom Progress Bar
    bar_width = int(width * progress)
    draw.rectangle([(0, height - 16), (width, height)], fill=(40, 40, 50))
    draw.rectangle([(0, height - 16), (bar_width, height)], fill=highlight_color)

    return np.array(img)


def assemble_story_video(
    scenes: List[Dict[str, Any]],
    output_path: str,
    audio_path: Optional[str] = None,
    fps: int = 15
) -> bool:
    """
    Compiles story scenes into a vertical MP4 video with synced subtitles,
    frame animations, and optional voiceover audio.
    """
    try:
        temp_dir = tempfile.mkdtemp()
        frame_pattern = os.path.join(temp_dir, "frame_%05d.png")

        total_scenes = len(scenes)
        frame_idx = 0

        for s_idx, scene in enumerate(scenes):
            # 3 to 4 seconds per scene frame sequence
            scene_duration_sec = 4
            num_frames = scene_duration_sec * fps
            main_text = scene.get("voiceover", "")
            cue_text = scene.get("on_screen_text", "")

            for f in range(num_frames):
                progress = (s_idx * num_frames + f) / (total_scenes * num_frames)
                frame_arr = create_subtitled_frame(
                    text=main_text,
                    subtext=cue_text,
                    progress=progress
                )
                img = Image.fromarray(frame_arr)
                img.save(frame_pattern % frame_idx)
                frame_idx += 1

        # Use imageio-ffmpeg binary directly for speed and reliability
        cmd = [
            FFMPEG_BIN,
            "-y",
            "-framerate", str(fps),
            "-i", os.path.join(temp_dir, "frame_%05d.png"),
        ]

        if audio_path and os.path.exists(audio_path):
            cmd.extend([
                "-i", audio_path,
                "-c:a", "aac",
                "-shortest"
            ])

        cmd.extend([
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-preset", "ultrafast",
            output_path
        ])

        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return proc.returncode == 0
    except Exception as exc:
        print(f"[video_compiler] Failed to build video: {exc}")
        return False
