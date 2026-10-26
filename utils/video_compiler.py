import os
import subprocess
import tempfile
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from typing import List, Dict, Any, Optional
import imageio_ffmpeg
from utils.background_generator import get_procedural_background_frame

FFMPEG_BIN = imageio_ffmpeg.get_ffmpeg_exe()

DEFAULT_WIDTH = 720
DEFAULT_HEIGHT = 1280

# Clean crisp TrueType fonts available on the system
FONT_REGULAR_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def _get_font(path: str, size: int):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

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
    Renders a high-converting, crisp 9:16 vertical video frame:
    - Dynamic gameplay background
    - Crisp Reddit / Story Card
    - Bold bouncing karaoke subtitles
    - Active retention bar
    """
    font_bold_lg = _get_font(FONT_BOLD_PATH, 28)
    font_bold_md = _get_font(FONT_BOLD_PATH, 22)
    font_bold_sm = _get_font(FONT_BOLD_PATH, 18)
    font_reg_md = _get_font(FONT_REGULAR_PATH, 22)
    font_reg_sm = _get_font(FONT_REGULAR_PATH, 16)

    # 1. Background layer
    bg_arr = get_procedural_background_frame(background_type, width, height, frame_idx)
    img = Image.fromarray(bg_arr).convert("RGBA")

    # 2. Card overlay
    card_margin = 35
    card_top = 70
    card_height = 230
    card_bottom = card_top + card_height

    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rounded_rectangle(
        [(card_margin, card_top), (width - card_margin, card_bottom)],
        radius=18,
        fill=(16, 18, 26, 240),
        outline=(255, 255, 255, 70),
        width=2
    )

    img = Image.alpha_composite(img, overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    # Reddit header metadata
    sub_title = reddit_header.get("subreddit", "r/Confession") if reddit_header else "r/StorytimeTik"
    author_tag = reddit_header.get("author", "u/ViralCreator") if reddit_header else "u/StorytimeTik"
    upvotes = reddit_header.get("upvotes", "32.4K") if reddit_header else "48.2K"

    # Badges
    draw.text((card_margin + 20, card_top + 20), f"{sub_title} • Posted by {author_tag}", font=font_reg_sm, fill=(180, 190, 210))
    draw.text((width - card_margin - 25, card_top + 18), f"▲ {upvotes}", font=font_bold_sm, fill=(255, 90, 40), anchor="ra")

    # Card Title
    card_text = reddit_header.get("title", text) if reddit_header else text
    words_c = card_text.split()
    lines_c = []
    cur = []
    for w in words_c:
        cur.append(w)
        if len(" ".join(cur)) > 26:
            lines_c.append(" ".join(cur[:-1]))
            cur = [w]
    if cur:
        lines_c.append(" ".join(cur))

    ty = card_top + 65
    for l in lines_c[:3]:
        draw.text((card_margin + 20, ty), l, font=font_bold_md, fill=(255, 255, 255))
        ty += 34

    # 3. Karaoke Bouncing Subtitle Box in focal zone
    words = text.split()
    karaoke_y = int(height * 0.64)

    sub_box_top = karaoke_y - 50
    sub_box_bottom = karaoke_y + 65
    draw.rounded_rectangle(
        [(card_margin + 15, sub_box_top), (width - card_margin - 15, sub_box_bottom)],
        radius=16,
        fill=(10, 12, 18),
        outline=(255, 215, 0),
        width=2
    )

    chunk_size = 4
    chunk_start = max(0, (active_word_idx // chunk_size) * chunk_size)
    chunk_words = words[chunk_start:chunk_start + chunk_size]

    start_x = width // 2
    rendered_chunk = " ".join(chunk_words)
    draw.text((start_x, karaoke_y - 12), rendered_chunk, font=font_reg_md, fill=(255, 255, 255), anchor="mm")

    highlight_word = words[active_word_idx] if active_word_idx < len(words) else ""
    if highlight_word:
        draw.text((start_x, karaoke_y + 26), f"► {highlight_word.upper()} ◄", font=font_bold_lg, fill=(255, 235, 20), anchor="mm")

    # 4. On-Screen Climax / Visual Cue Pill
    if subtext:
        cue_y = int(height * 0.86)
        draw.rounded_rectangle(
            [(width // 2 - 180, cue_y - 24), (width // 2 + 180, cue_y + 24)],
            radius=14,
            fill=(255, 0, 80)
        )
        draw.text((width // 2, cue_y), f"★ {subtext}", font=font_bold_sm, fill=(255, 255, 255), anchor="mm")

    # 5. Glowing Retention Progress Bar
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
