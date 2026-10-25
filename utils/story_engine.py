import re
import random
from typing import List, Dict, Any, Optional
from datetime import datetime

STORY_ARCHETYPES = {
    "confession": {
        "title": "A Secret I've Never Told Anyone",
        "hooks": [
            "I kept this secret for 5 years, and today it finally caught up with me...",
            "Nobody believed me when I warned them, but look what happened...",
            "I found something in my attic that completely shattered our family...",
            "If you ever see this weird text on your phone, throw it into the ocean immediately."
        ],
        "twists": [
            "The person warning me was actually the one pulling the strings.",
            "I discovered that the apartment was never empty to begin with.",
            "The photo was taken 10 years before either of us was born."
        ],
        "tags": ["#storytime", "#confession", "#truestory", "#viral", "#fyp", "#drama"]
    },
    "mystery": {
        "title": "The Unexplained Occurrence",
        "hooks": [
            "At exactly 3:17 AM every Wednesday, my smart doorbell records the exact same silhouette.",
            "I bought a storage unit in rural Ohio and found an encrypted diary.",
            "Do NOT ignore this glitch if your GPS ever reroutes you through old route 9."
        ],
        "twists": [
            "The signal wasn't coming from outside — it was originating in my own basement.",
            "Every single contact in the address book was marked 'deceased' since 1998.",
            "The house in the photograph doesn't exist on any satellite map."
        ],
        "tags": ["#mystery", "#creepy", "#storytimetik", "#unexplained", "#chills", "#fyp"]
    },
    "revenge": {
        "title": "The Petty Workplace Revenge",
        "hooks": [
            "My boss thought stealing my project idea would get him promoted. He had no idea what I hid in slide 14.",
            "When my landlord tried to keep my $3,000 security deposit, I called the historical society.",
            "They laughed at my proposal in the board meeting. Six months later, they begged to buy it back."
        ],
        "twists": [
            "He presented the deck live to the CEO without reading the hidden audit appendix.",
            "The entire property was legally classified as an unpermitted historic landmark.",
            "The trademark had been registered under my personal LLC three days prior."
        ],
        "tags": ["#pettyrevenge", "#workplace", "#karma", "#storytime", "#justice", "#satisfying"]
    },
    "relationship": {
        "title": "Red Flags I Ignored",
        "hooks": [
            "I thought he was just being secretive about his birthday surprise...",
            "We were together for 3 years before I realized his 'family cottage' didn't exist.",
            "She insisted on paying for dinner in cash. Here's what I found in her car glovebox."
        ],
        "twists": [
            "He was living a completely double life two towns over.",
            "She had hired an actor to pose as her eccentric uncle.",
            "Every gift he ever gave me was taken from an unclaimed baggage auction."
        ],
        "tags": ["#relationshiptok", "#redflags", "#datingstorytime", "#tea", "#caught", "#fyp"]
    },
    "entrepreneur": {
        "title": "How a Ridiculous Idea Made $50k",
        "hooks": [
            "Everyone told me I was insane to quit my 9-to-5 for this weird side hustle.",
            "I spent $12 on a domain name and accidentally built a 6-figure micro-SaaS.",
            "How this simple automated script generated $4,200 while I was asleep."
        ],
        "twists": [
            "A Fortune 500 company accidentally linked to my tool in their employee handbook.",
            "The single TikTok video got 4 million views overnight and crashed my Stripe webhook.",
            "I ended up hiring the very manager who fired me as an independent contractor."
        ],
        "tags": ["#sidehustle", "#passiveincome", "#entrepreneur", "#buildinpublic", "#moneytok", "#growth"]
    }
}


def generate_story_script(
    archetype: str,
    custom_premise: Optional[str] = None,
    pacing_seconds: int = 60,
    tone: str = "Dramatic & Suspenseful"
) -> Dict[str, Any]:
    """
    Generate an engaging multi-part TikTok story script with hooks, scene breakdowns,
    voiceover text, visual cues, and optimized hashtags.
    """
    data = STORY_ARCHETYPES.get(archetype, STORY_ARCHETYPES["confession"])
    hook = random.choice(data["hooks"]) if not custom_premise else f"Let me tell you about the day {custom_premise.rstrip('.')}..."
    twist = random.choice(data["twists"])

    # Target word count: roughly 140 words per 60 seconds (TikTok narration pace)
    target_words = int((pacing_seconds / 60) * 140)

    scenes = [
        {
            "part": 1,
            "timestamp": "0:00 - 0:05",
            "section": "The Hook (First 3 Seconds)",
            "visual_direction": "Fast-paced visual zoom / Minecraft parkour / Subway surfers / POV reaction shot",
            "voiceover": hook,
            "on_screen_text": hook[:50] + ("..." if len(hook) > 50 else "")
        },
        {
            "part": 2,
            "timestamp": "0:05 - 0:20",
            "section": "The Context & Build-up",
            "visual_direction": "Cut to b-roll, text screenshots, or subtle dark mood aesthetics",
            "voiceover": f"So here's the context. It was late autumn, and everything seemed completely normal on the surface. But behind closed doors, things were already spiraling. You need to understand how subtle the red flags were at first.",
            "on_screen_text": "Nobody noticed the warning signs..."
        },
        {
            "part": 3,
            "timestamp": "0:20 - 0:40",
            "section": "The Rising Climax",
            "visual_direction": "Speed up cuts, intense sound effect (whoosh / bass drop), close-up reaction",
            "voiceover": f"I decided to check the logs myself. My heart was pounding like crazy. Every single piece of evidence pointed to something I never could have predicted in a million years.",
            "on_screen_text": "Then I found the proof."
        },
        {
            "part": 4,
            "timestamp": "0:40 - 0:55",
            "section": "The Twist",
            "visual_direction": "Freeze-frame, dramatic pause, bold colored captions",
            "voiceover": f"And that's when the truth dropped: {twist} I literally stood there in complete shock.",
            "on_screen_text": f"Wait for it... {twist[:40]}..."
        },
        {
            "part": 5,
            "timestamp": "0:55 - 1:00",
            "section": "Call to Action / Engagement Bait",
            "visual_direction": "Point to comments button / prompt question overlay",
            "voiceover": "Part 2 is already recorded if you want the aftermath. What would you have done in my situation? Drop a comment below and follow for the update.",
            "on_screen_text": "What would YOU do? Part 2 in bio!"
        }
    ]

    full_voiceover = " ".join(scene["voiceover"] for scene in scenes)
    total_words = len(full_voiceover.split())
    estimated_duration_sec = round((total_words / 140) * 60, 1)

    return {
        "title": f"{data['title']} — {datetime.now().strftime('%b %d')}",
        "archetype": archetype,
        "tone": tone,
        "hook": hook,
        "twist": twist,
        "scenes": scenes,
        "full_voiceover": full_voiceover,
        "word_count": total_words,
        "estimated_duration_sec": estimated_duration_sec,
        "hashtags": data["tags"] + ["#storytimetik", "#foryoupage"]
    }


def analyze_hook_strength(hook: str) -> Dict[str, Any]:
    """
    Evaluates a TikTok hook on virality factors: curiosity gap, emotional punch,
    length, and keyword engagement.
    """
    score = 60
    feedback = []

    words = hook.split()
    word_count = len(words)

    if 8 <= word_count <= 22:
        score += 15
        feedback.append("Great length (under 25 words keeps viewer retention high).")
    elif word_count < 8:
        feedback.append("A bit brief; try expanding curiosity.")
    else:
        score -= 10
        feedback.append("Slightly too wordy for a 3-second hook; tighten it up.")

    curiosity_triggers = ["secret", "never", "warned", "caught", "insane", "truth", "hidden", "nobody", "glitch", "ruined"]
    matched_triggers = [t for t in curiosity_triggers if t in hook.lower()]

    if matched_triggers:
        score += 15
        feedback.append(f"Strong emotional trigger words detected: {', '.join(matched_triggers)}.")
    else:
        feedback.append("Tip: Add high-stakes trigger words (e.g., 'secret', 'never', 'caught').")

    if "?" in hook or "..." in hook or "!" in hook:
        score += 10
        feedback.append("Good punctuation pacing for pauses and tension.")

    score = min(100, max(20, score))
    rating = "Viral Potential 🚀" if score >= 85 else ("Solid Hook 👍" if score >= 70 else "Needs Punch ✍️")

    return {
        "score": score,
        "rating": rating,
        "feedback": feedback
    }
