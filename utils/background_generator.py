"""
Generates dynamic procedural background video loops for storytime split screens
(Minecraft isometric blocks, Hypnotic Neon Tunnel, Cozy Night Cyberpunk Drive).
Ensures zero external video download dependencies.
"""

import os
import math
import numpy as np
from PIL import Image, ImageDraw

def render_minecraft_parkour_frame(width: int, height: int, frame_idx: int, total_frames: int) -> np.ndarray:
    """
    Renders an animated isometric 3D-style block parkour aesthetic with drifting clouds and floating voxel platforms.
    """
    img = Image.new("RGB", (width, height), (90, 160, 240)) # Minecraft sky blue
    draw = ImageDraw.Draw(img)

    t = frame_idx * 0.15
    scroll_y = int((frame_idx * 7) % 300)

    # Sun
    draw.rectangle([(width - 140, 40), (width - 60, 120)], fill=(255, 255, 200))

    # Clouds
    cloud_x = int((frame_idx * 2) % (width + 200)) - 100
    draw.rectangle([(cloud_x, 150), (cloud_x + 180, 200)], fill=(240, 245, 255))
    draw.rectangle([(cloud_x + 30, 130), (cloud_x + 140, 150)], fill=(240, 245, 255))

    # Floating voxel platforms (isometric block stack moving down)
    center_x = width // 2
    for i in range(7):
        base_y = int(height * 0.5) + (i * 120) - scroll_y
        w_block = 180
        h_block = 80
        left = center_x - (w_block // 2) + int(math.sin(t + i) * 60)
        top = base_y
        right = left + w_block
        bottom = top + h_block

        if -h_block < top < height + h_block:
            # Top grass face (green)
            draw.rectangle([(left, top), (right, top + 25)], fill=(86, 172, 58))
            # Dirt side face (brown)
            draw.rectangle([(left, top + 25), (right, bottom)], fill=(134, 96, 67))
            # Pixel grit
            for px in range(left + 10, right - 10, 20):
                draw.rectangle([(px, top + 35), (px + 8, top + 45)], fill=(100, 70, 50))

    return np.array(img)


def render_hypnotic_tunnel_frame(width: int, height: int, frame_idx: int, total_frames: int) -> np.ndarray:
    """
    Renders a hypnotic pulsating synthwave neon tunnel loop.
    """
    img = Image.new("RGB", (width, height), (15, 12, 28))
    draw = ImageDraw.Draw(img)

    cx, cy = width // 2, int(height * 0.65)
    t = frame_idx * 0.2

    # Draw converging perspective grid lines
    for angle_deg in range(0, 360, 30):
        rad = math.radians(angle_deg)
        x_end = cx + math.cos(rad) * 900
        y_end = cy + math.sin(rad) * 900
        draw.line([(cx, cy), (x_end, y_end)], fill=(80, 20, 120), width=2)

    # Concentric pulsating rings
    for r_idx in range(8):
        radius = int(((frame_idx * 8 + r_idx * 70) % 500))
        if radius > 15:
            col_shift = int((math.sin(t + r_idx) + 1) * 100)
            color = (255, 0, min(255, 100 + col_shift))
            draw.ellipse(
                [(cx - radius, cy - int(radius * 0.7)), (cx + radius, cy + int(radius * 0.7))],
                outline=color,
                width=3
            )

    return np.array(img)


def get_procedural_background_frame(bg_type: str, width: int, height: int, frame_idx: int, total_frames: int = 100) -> np.ndarray:
    if bg_type == "minecraft":
        return render_minecraft_parkour_frame(width, height, frame_idx, total_frames)
    elif bg_type == "tunnel":
        return render_hypnotic_tunnel_frame(width, height, frame_idx, total_frames)
    else:
        # Subtle dark ambient slate gradient
        img = Image.new("RGB", (width, height), (22, 24, 32))
        draw = ImageDraw.Draw(img)
        wave_y = int(math.sin(frame_idx * 0.1) * 30)
        draw.ellipse([(width//2 - 200, height//2 - 200 + wave_y), (width//2 + 200, height//2 + 200 + wave_y)], outline=(40, 45, 60), width=4)
        return np.array(img)
