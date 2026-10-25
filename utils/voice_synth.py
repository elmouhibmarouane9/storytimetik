import io
import os
from typing import Optional

def synthesize_audio(text: str, lang: str = "en", tld: str = "com") -> Optional[bytes]:
    """
    Synthesize text into speech MP3 bytes using gTTS.
    Falls back gracefully if network is unavailable or voice fails.
    """
    try:
        from gtts import gTTS
        clean_text = " ".join(text.strip().split())
        if not clean_text:
            return None
        # Limit preview text to 500 characters to ensure quick generation
        preview_text = clean_text[:500]
        tts = gTTS(text=preview_text, lang=lang, tld=tld, slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp.read()
    except Exception as exc:
        print(f"[voice_synth] Voice synthesis error: {exc}")
        return None
