import os
import subprocess
import tempfile
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from typing import List, Dict, Any, Optional
import imageio_ffmpeg
from utils.background_generator import get_procedural_background_frame

FFMPEG_BIN = imageio_ffmpeg.get_ffmpeg_exe()

DEFAULT_WIDTH = 720
DEFAULT_HEIGHT = 1280

def create_subtitled_frame(
    text: str,
    subtext: str,
    active_word_idx: int = 0,
    background_type: str = "minecraft",
    frame_idx: int = 0,
    width: int = DEFAULT_WIDTH,
    height: int = DEFAULT_HEIGHT,
    progress: float = 0.0,
    reddit_header: Optional[Dict[str, str]] = None
) -> np.ndarray:
    """
    Renders an authentic TikTok split-screen vertical frame:
    - Top half: Reddit Post card with upvotes, subreddit tag, or clean Story card
    - Bottom half: Dynamic background loop (Minecraft block parkour, Hypnotic synth tunnel, etc.)
    - Center/Overlay: Karaoke bouncing subtitle highlighting the exact spoken word
    - Bottom: Glowing progress bar
    """
    # 1. Background layer
    bg_arr = get_procedural_background_frame(background_type, width, height, frame_idx)
    img = Image.fromarray(bg_arr)
    draw = ImageDraw.Draw(img)

    # 2. Reddit Header Card (or Story Card) in top-center zone
    card_margin = 35
    card_top = 80
    card_height = 240
    card_bottom = card_top + card_height

    # Semi-transparent dark card backing
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rounded_rectangle(
        [(card_margin, card_top), (width - card_margin, card_bottom)],
        radius=20,
        fill=(24, 25, 34, 230),
        outline=(255, 255, 255, 60),
        width=2
    )

    img.paste(Image.alpha_composite(Image.new("RGBA", img.size, (0, 0, 0, 0)), overlay).convert("RGB"), (0, 0))
    draw = ImageDraw.Draw(img)

    # Subreddit / Channel Badge
    sub_title = reddit_header.get("subreddit", "r/Confession") if reddit_header else "r/StorytimeTik"
    author_tag = reddit_header.get("author", "u/ViralCreator") if reddit_header else "u/StorytimeTik"
    upvotes = reddit_header.get("upvotes", "32.4K") if reddit_header else "48.2K"

    draw.text((card_margin + 25, card_top + 25), f"🔴 {sub_title} • Posted by {author_tag}", fill=(180, 185, 200))
    draw.text((width - card_margin - 30, card_top + 25), f"⬆️ {upvotes}", fill=(255, 90, 40), anchor="ra")

    # Hook / Title on Card
    card_text = reddit_header.get("title", text) if reddit_header else text
    words_c = card_text.split()
    lines_c = []
    cur = []
    for w in words_c:
        cur.append(w)
        if len(" ".join(cur)) > 28:
            lines_c.append(" ".join(cur[:-1]))
            cur = [w]
    if cur:
        lines_c.append(" ".join(cur))

    ty = card_top + 70
    for l in lines_c[:3]:
        draw.text((card_margin + 25, ty), l, fill=(255, 255, 255))
        ty += 40

    # 3. Karaoke Bouncing Subtitles in the lower-middle focal zone (y ~ 720 to 880)
    words = text.split()
    karaoke_y = int(height * 0.62)

    # Subtitle background bubble
    sub_box_top = karaoke_y - 45
    sub_box_bottom = karaoke_y + 65
    draw.rounded_rectangle(
        [(card_margin + 20, sub_box_top), (width - card_margin - 20, sub_box_bottom)],
        radius=18,
        fill=(10, 10, 14),
        outline=(255, 215, 0),
        width=2
    )

    # Word wrapping for spoken text with active-word highlight
    chunk_size = 4
    chunk_start = max(0, (active_word_idx // chunk_size) * chunk_size)
    chunk_words = words[chunk_start:chunk_start + chunk_size]

    start_x = width // 2
    rendered_chunk = " ".join(chunk_words)
    draw.text((start_x, karaoke_y), rendered_chunk, fill=(255, 255, 255), anchor="mm")

    # Highlight current spoken word
    highlight_word = words[active_word_idx] if active_word_idx < len(words) else ""
    if highlight_word:
        draw.text((start_x, karaoke_y + 35), f"🗣️ [{highlight_word.upper()}]", fill=(255, 230, 0), anchor="mm")

    # 4. On-Screen Climax / Visual Cue Pill
    if subtext:
        cue_y = int(height * 0.86)
        draw.rounded_rectangle(
            [(width // 2 - 200, cue_y - 20), (width // 2 + 200, cue_y + 20)],
            radius=14,
            fill=(255, 0, 80)
        )
        draw.text((width // 2, cue_y), f"⚡ {subtext}", fill=(255, 255, 255), anchor="mm")

    # 5. Glowing Retention Progress Bar at the base
    bar_width = int(width * progress)
    draw.rectangle([(0, height - 16), (width, height)], fill=(30, 30, 40))
    draw.rectangle([(0, height - 16), (bar_width, height)], fill=(255, 0, 80))

    return np.array(img)


def assemble_story_video(
    scenes: List[Dict[str, Any]],
    output_path: str,
    audio_path: Optional[str] = None,
    fps: int = 15,
    background_type: str = "minecraft",
    reddit_header: Optional[Dict[str, str]] = None
) -> bool:
    """
    Compiles story scenes into a vertical MP4 video with synced karaoke subtitles,
    split-screen gameplay background, frame animations, and audio.
    """
    try:
        temp_dir = tempfile.mkdtemp()
        frame_pattern = os.path.join(temp_dir, "frame_%05d.png")

        total_scenes = len(scenes)
        frame_idx = 0

        for s_idx, scene in enumerate(scenes):
            scene_duration_sec = 4
            num_frames = scene_duration_sec * fps
            main_text = scene.get("voiceover", "")
            cue_text = scene.get("on_screen_text", "")
            scene_words = main_text.split()
            word_count = max(1, len(scene_words))

            for f in range(num_frames):
                # Calculate active word index based on time progress in the scene
                progress_in_scene = f / float(num_frames)
                active_word_idx = min(word_count - 1, int(progress_in_scene * word_count))
                global_progress = (s_idx * num_frames + f) / float(total_scenes * num_frames)

                frame_arr = create_subtitled_frame(
                    text=main_text,
                    subtext=cue_text,
                    active_word_idx=active_word_idx,
                    background_type=background_type,
                    frame_idx=frame_idx,
                    progress=global_progress,
                    reddit_header=reddit_header
                )
                img = Image.fromarray(frame_arr)
                img.save(frame_pattern % frame_idx)
                frame_idx += 1

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
