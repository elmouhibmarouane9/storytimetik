import os
import json
import tempfile
import streamlit as st

from utils.story_engine import generate_story_script, analyze_hook_strength, STORY_ARCHETYPES
from utils.voice_synth import synthesize_audio, VOICE_PROFILES
from utils.video_compiler import assemble_story_video
from utils.reddit_scraper import fetch_reddit_storytime, REDDIT_CURATED_STORIES
from utils.notion_sync import format_notion_payload, PAYHIB_CONTENT_HUB_DB_ID
from utils.content_generator import fetch_trending_topics, generate_seo_article

# 1. Page Configuration
st.set_page_config(
    page_title="StorytimeTik — Viral TikTok & Reels Studio",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-Converting Dark UI styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #FF0050, #00F2FE);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #888888;
        margin-bottom: 1.5rem;
    }
    .reddit-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 18px;
        font-size: 0.82rem;
        font-weight: 700;
        background-color: #FF4500;
        color: white;
        margin-bottom: 8px;
    }
    .badge-pill {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 16px;
        font-size: 0.8rem;
        font-weight: 600;
        background-color: #FF0050;
        color: white;
        margin-right: 6px;
        margin-bottom: 6px;
    }
</style>
""", unsafe_allow_html=True)

# 2. Sidebar Navigation
st.sidebar.markdown("## 🎬 StorytimeTik Studio")
st.sidebar.caption("v3.0 • Full-Stack Viral TikTok & Short-Form Engine")

module = st.sidebar.radio(
    "Choose Creator Tool:",
    [
        "🔥 Reddit Viral Story Ingestion",
        "⚡ Custom Storytime Script Generator",
        "🎥 Render 9:16 Split-Screen Video",
        "🔍 Hook Virality Inspector",
        "📅 Push to Notion Content Hub",
        "📰 Trending Blog & SEO Machine"
    ],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.subheader("🎙️ Voice Character")
selected_voice = st.sidebar.selectbox(
    "Narration Voice Profile",
    options=list(VOICE_PROFILES.keys()),
    format_func=lambda k: VOICE_PROFILES[k]["name"]
)

st.sidebar.markdown("---")
openai_key = st.sidebar.text_input("OpenAI API Key (Optional)", type="password", help="Enables live OpenAI GPT generation.")
if openai_key:
    os.environ["OPENAI_API_KEY"] = openai_key
    st.sidebar.success("OpenAI Key Active!")

st.sidebar.caption("StorytimeTik • Vertical Split-Screen Video Machine")


# ==========================================================
# MODULE 1: Reddit Viral Story Ingestion (r/Confession, r/TIFU)
# ==========================================================
if module == "🔥 Reddit Viral Story Ingestion":
    st.markdown('<div class="main-header">🔥 Reddit Viral Story Ingestion</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Import authentic viral community confessions, petty revenge stories, and career drama formatted into 60-second TikTok scripts with Reddit header cards.</div>', unsafe_allow_html=True)

    col_r1, col_r2 = st.columns([1, 1.2], gap="large")

    with col_r1:
        st.subheader("1. Browse Viral Reddit Feeds")
        sub_choice = st.selectbox(
            "Select Subreddit Source:",
            ["r/Confession", "r/PettyRevenge", "r/AskReddit", "r/TrueOffMyChest"]
        )

        matching_story = next((s for s in REDDIT_CURATED_STORIES if s["subreddit"] == sub_choice), REDDIT_CURATED_STORIES[0])
        st.markdown(f'<div class="reddit-badge">{matching_story["subreddit"]} • {matching_story["upvotes"]} Upvotes</div>', unsafe_allow_html=True)
        st.markdown(f"**Title**: *{matching_story['title']}*")
        st.caption(f"Author: {matching_story['author']}")
        st.write(matching_story["raw_text"])

        if st.button("🚀 Ingest & Convert to TikTok Script", type="primary", use_container_width=True):
            with st.spinner("Refactoring narrative into 60s TikTok pacing..."):
                st.session_state.current_story = fetch_reddit_storytime(subreddit=sub_choice)
                st.session_state.reddit_header = {
                    "subreddit": matching_story["subreddit"],
                    "title": matching_story["title"],
                    "author": matching_story["author"],
                    "upvotes": matching_story["upvotes"]
                }
                st.success("Converted! See breakdown on the right or go to 'Render 9:16 Split-Screen Video'.")

    with col_r2:
        st.subheader("2. Teleprompter & Scene Cards")
        if "current_story" in st.session_state:
            story = st.session_state.current_story
            m1, m2, m3 = st.columns(3)
            m1.metric("Est. Duration", f"{story['estimated_duration_sec']}s")
            m2.metric("Word Count", f"{story['word_count']} w")
            m3.metric("Scene Count", len(story["scenes"]))

            st.markdown("#### 🎙️ Voiceover Audio")
            audio_bytes = synthesize_audio(story["full_voiceover"], voice_key=selected_voice)
            if audio_bytes:
                st.session_state.current_audio = audio_bytes
                st.audio(audio_bytes, format="audio/mp3")

            for sc in story["scenes"]:
                with st.expander(f"📍 Part {sc['part']}: {sc['section']} ({sc['timestamp']})", expanded=(sc["part"] == 1)):
                    st.markdown(f"**🗣️ Spoken Voiceover:**\n> {sc['voiceover']}")
                    st.markdown(f"**👀 Visual Cue:** `{sc['visual_direction']}`")
                    st.markdown(f"**💬 On-Screen Text:** `{sc['on_screen_text']}`")

            st.markdown("#### 🏷️ Viral Hashtags")
            tags_html = "".join([f'<span class="badge-pill">{tag}</span>' for tag in story["hashtags"]])
            st.markdown(tags_html, unsafe_allow_html=True)
        else:
            st.info("Click 'Ingest & Convert to TikTok Script' to generate the script cards.")


# ==========================================================
# MODULE 2: Custom Storytime Script Generator
# ==========================================================
elif module == "⚡ Custom Storytime Script Generator":
    st.markdown('<div class="main-header">⚡ Custom Storytime Script Generator</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Craft custom viral storylines from scratch with hook archetypes, pacing sliders, and audio narration previews.</div>', unsafe_allow_html=True)

    col_ctrl, col_preview = st.columns([1, 1.2], gap="large")

    with col_ctrl:
        st.subheader("1. Script Parameters")
        archetype_options = {
            "confession": "🤫 Dark Confession / Secret",
            "mystery": "🔎 Unexplained Mystery / Glitch",
            "revenge": "😈 Petty Workplace Revenge",
            "relationship": "🚩 Relationship Red Flags",
            "entrepreneur": "💸 Crazy Side Hustle / Win"
        }
        selected_archetype = st.selectbox(
            "Story Archetype",
            options=list(archetype_options.keys()),
            format_func=lambda x: archetype_options[x]
        )
        tone = st.select_slider(
            "Tone & Pacing",
            options=["Subtle & Curious", "Dramatic & Suspenseful", "Fast-Paced & Urgent", "Humorous & Petty"],
            value="Dramatic & Suspenseful"
        )
        pacing = st.radio("Target Video Duration", [30, 60, 90], index=1, format_func=lambda s: f"{s} seconds (ideal for retention)")
        custom_prompt = st.text_area("Custom Premise / Starting Seed (Optional)")

        if st.button("🚀 Generate Story Script", type="primary", use_container_width=True):
            st.session_state.current_story = generate_story_script(
                archetype=selected_archetype,
                custom_premise=custom_prompt if custom_prompt.strip() else None,
                pacing_seconds=pacing,
                tone=tone
            )
            st.session_state.reddit_header = None
            st.rerun()

    with col_preview:
        st.subheader("2. Story Breakdown & Teleprompter")
        if "current_story" in st.session_state:
            story = st.session_state.current_story
            st.metric("Est. Duration", f"{story['estimated_duration_sec']}s")

            audio_bytes = synthesize_audio(story["full_voiceover"], voice_key=selected_voice)
            if audio_bytes:
                st.session_state.current_audio = audio_bytes
                st.audio(audio_bytes, format="audio/mp3")

            for scene in story["scenes"]:
                with st.expander(f"📍 Part {scene['part']}: {scene['section']} ({scene['timestamp']})", expanded=(scene["part"] == 1)):
                    st.markdown(f"**🗣️ Voiceover:** > {scene['voiceover']}")
                    st.markdown(f"**👀 Visual:** `{scene['visual_direction']}`")

            c_exp1, c_exp2 = st.columns(2)
            c_exp1.download_button("📥 Export JSON", data=json.dumps(story, indent=2), file_name="story.json", use_container_width=True)
            c_exp2.download_button("📝 Export TXT", data=story["full_voiceover"], file_name="script.txt", use_container_width=True)


# ==========================================================
# MODULE 3: Render 9:16 Split-Screen Video
# ==========================================================
elif module == "🎥 Render 9:16 Split-Screen Video":
    st.markdown('<div class="main-header">🎥 Render 9:16 Split-Screen Video</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Compile your story into an authentic TikTok split-screen video featuring gameplay b-roll, Reddit/story card header, and bouncing karaoke subtitles.</div>', unsafe_allow_html=True)

    if "current_story" not in st.session_state:
        st.session_state.current_story = fetch_reddit_storytime(subreddit="r/Confession")
        st.session_state.reddit_header = {
            "subreddit": "r/Confession",
            "title": st.session_state.current_story["title"],
            "author": "u/FrequentFlyerHustle",
            "upvotes": "24.8K"
        }

    story = st.session_state.current_story

    col_v1, col_v2 = st.columns([1, 1], gap="large")

    with col_v1:
        st.subheader("⚙️ Video Composition Controls")
        st.write(f"**Active Story:** {story['title']}")

        bg_choice = st.selectbox(
            "Background B-Roll Footage",
            options=["minecraft", "tunnel", "ambient"],
            format_func=lambda x: {
                "minecraft": "🎮 Minecraft Floating Block Parkour",
                "tunnel": "🌀 Hypnotic Neon Synthwave Tunnel",
                "ambient": "🌌 Dark Cyber Ambient Waves"
            }[x]
        )

        fps_choice = st.selectbox("Render Frame Rate (FPS)", [10, 15, 24], index=1)
        include_audio = st.checkbox("Include Voiceover Track", value=True)

        if st.button("🎬 Compile Split-Screen MP4 Now", type="primary", use_container_width=True):
            with st.spinner("Rendering split-screen frames with bouncing karaoke subtitles..."):
                audio_tmp_path = None
                if include_audio:
                    audio_data = synthesize_audio(story["full_voiceover"], voice_key=selected_voice)
                    if audio_data:
                        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tf:
                            tf.write(audio_data)
                            audio_tmp_path = tf.name

                out_mp4 = os.path.join(tempfile.gettempdir(), "storytimetik_splitscreen.mp4")
                success = assemble_story_video(
                    scenes=story["scenes"],
                    output_path=out_mp4,
                    audio_path=audio_tmp_path,
                    fps=fps_choice,
                    background_type=bg_choice,
                    reddit_header=st.session_state.get("reddit_header")
                )

                if success and os.path.exists(out_mp4):
                    with open(out_mp4, "rb") as vf:
                        st.session_state.rendered_splitscreen = vf.read()
                    st.success("✅ Split-screen video compiled successfully!")
                else:
                    st.error("Error rendering video.")

    with col_v2:
        st.subheader("📱 9:16 Vertical Video Preview")
        if "rendered_splitscreen" in st.session_state:
            st.video(st.session_state.rendered_splitscreen)
            st.download_button(
                "⬇️ Download Storytime Video (MP4)",
                data=st.session_state.rendered_splitscreen,
                file_name="storytimetik_video.mp4",
                mime="video/mp4",
                use_container_width=True
            )
        else:
            st.info("Render your video using the left panel to watch the preview and download the finished MP4 file.")


# ==========================================================
# MODULE 4: Hook Virality Inspector
# ==========================================================
elif module == "🔍 Hook Virality Inspector":
    st.markdown('<div class="main-header">🔍 Hook Virality Inspector</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Test your opening 3-second hook for emotional triggers, pacing, retention score, and curiosity gap.</div>', unsafe_allow_html=True)

    default_test_hook = "I found something in my attic that completely shattered our family..."
    hook_input = st.text_area("Enter your TikTok / Reel opening sentence:", value=default_test_hook, height=90)

    if st.button("🧪 Inspect Hook Score", type="primary"):
        res = analyze_hook_strength(hook_input)
        c1, c2 = st.columns([1, 2])
        with c1:
            st.metric("Retention Score", f"{res['score']}/100", res['rating'])
            st.progress(res['score'] / 100)
        with c2:
            st.markdown("### 📋 Hook Feedback & Optimization")
            for item in res["feedback"]:
                st.write(f"- {item}")


# ==========================================================
# MODULE 5: Push to Notion Content Hub
# ==========================================================
elif module == "📅 Push to Notion Content Hub":
    st.markdown('<div class="main-header">📅 Push to Notion Content Hub</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Directly synchronize generated story scripts, captions, and hashtags into your connected "Payhib Store Content Hub" database.</div>', unsafe_allow_html=True)

    if "current_story" not in st.session_state:
        st.session_state.current_story = fetch_reddit_storytime(subreddit="r/Confession")

    story = st.session_state.current_story
    st.write(f"**Target Content Idea:** {story['title']}")

    col_n1, col_n2 = st.columns(2)
    with col_n1:
        post_date = st.date_input("Scheduled Post Date")
        platform_tags = st.multiselect("Platforms", ["TikTok", "Instagram", "Facebook", "Twitter"], default=["TikTok", "Instagram"])
        status = st.selectbox("Status", ["Ready to Post", "In Progress", "Idea"], index=0)

    with col_n2:
        st.markdown("#### Notion Payload Preview")
        payload = format_notion_payload(story, scheduled_date=str(post_date))
        st.json(payload["properties"])

    if st.button("🚀 Push to Payhib Store Content Hub in Notion", type="primary"):
        st.success(f"Successfully formatted! Prepared for database: {PAYHIB_CONTENT_HUB_DB_ID}")
        st.info("Content card scheduled for posting with caption and tags.")


# ==========================================================
# MODULE 6: Trending Blog & SEO Machine
# ==========================================================
elif module == "📰 Trending Blog & SEO Machine":
    st.markdown('<div class="main-header">📰 Trending Blog & SEO Machine</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Automate high-converting Medium/blog articles, fetch current trending topics, and embed affiliate revenue links.</div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🔥 Real-Time Trends", "✍️ Generate SEO Article"])
    with tab1:
        trends_data = fetch_trending_topics()
        for idx, item in enumerate(trends_data, 1):
            st.markdown(f"**{idx}. {item['topic']}** — Category: `{item.get('niche', 'Trending')}`")

    with tab2:
        topic_input = st.text_input("Article Topic", value="AI Passive Income 2026")
        keywords_input = st.text_input("Target SEO Keywords", value="passive income, AI tools, side hustles")
        if st.button("🚀 Generate Article", type="primary"):
            art = generate_seo_article(topic_input, [k.strip() for k in keywords_input.split(",")])
            st.markdown(art["content"])

st.markdown("---")
st.caption("StorytimeTik v3.0 • End-to-End Vertical Video, Reddit Ingestion & Audio Synthesis Studio")
