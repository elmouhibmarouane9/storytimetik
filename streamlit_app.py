import os
import json
import streamlit as st
from utils.story_engine import generate_story_script, analyze_hook_strength, STORY_ARCHETYPES
from utils.voice_synth import synthesize_audio
from utils.content_generator import fetch_trending_topics, generate_seo_article

# 1. Page Configuration
st.set_page_config(
    page_title="StorytimeTik Studio & Creator Engine",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for polished dark/light mode experience
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
    .metric-card {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 12px;
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
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 48px;
        border-radius: 8px 8px 0px 0px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# 2. Sidebar Navigation & Global Controls
st.sidebar.markdown("## 🎬 StorytimeTik Studio")
st.sidebar.caption("v2.0 • AI-Powered Creator & Monetization Engine")

module = st.sidebar.radio(
    "Choose Studio Tool:",
    [
        "⚡ TikTok Storytime Generator",
        "🔍 Hook Virality Inspector",
        "📰 Trending Blog & SEO Machine",
        "🛠️ Interactive Creator Tools"
    ],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Settings & API Keys")
openai_key = st.sidebar.text_input("OpenAI API Key (Optional)", type="password", help="Enables live OpenAI GPT-4o-mini generation. If blank, high-quality built-in heuristics and templates run.")
if openai_key:
    os.environ["OPENAI_API_KEY"] = openai_key
    st.sidebar.success("OpenAI Key registered!")

st.sidebar.markdown("---")
st.sidebar.caption("Built with Streamlit & Python • Optimized for TikTok, Reels & SEO Automation")


# ==========================================
# MODULE 1: TikTok Storytime Script Generator
# ==========================================
if module == "⚡ TikTok Storytime Generator":
    st.markdown('<div class="main-header">⚡ TikTok Storytime Generator</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Craft retention-engineered storytime scripts complete with timestamps, visual directions, audio hooks, and auto-generated voiceovers.</div>', unsafe_allow_html=True)

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

        custom_prompt = st.text_area(
            "Custom Premise or Starting Seed (Optional)",
            placeholder="e.g. I hired a private investigator to check on my roommate...",
            help="Leave blank to use verified viral story templates."
        )

        generate_clicked = st.button("🚀 Generate Story Script", type="primary", use_container_width=True)

    if generate_clicked or "current_story" in st.session_state:
        if generate_clicked:
            with st.spinner("Generating viral multi-part story structure..."):
                st.session_state.current_story = generate_story_script(
                    archetype=selected_archetype,
                    custom_premise=custom_prompt if custom_prompt.strip() else None,
                    pacing_seconds=pacing,
                    tone=tone
                )

        story = st.session_state.current_story

        with col_preview:
            st.subheader("2. Story Breakdown & Teleprompter")
            
            # Overview Metrics
            mcol1, mcol2, mcol3 = st.columns(3)
            mcol1.metric("Est. Duration", f"{story['estimated_duration_sec']}s")
            mcol2.metric("Word Count", f"{story['word_count']} w")
            mcol3.metric("Scene Count", len(story["scenes"]))

            # Voiceover Audio Preview
            st.markdown("#### 🎙️ Voiceover Audio Preview (TTS)")
            audio_bytes = synthesize_audio(story["full_voiceover"])
            if audio_bytes:
                st.audio(audio_bytes, format="audio/mp3")
                st.download_button(
                    label="⬇️ Download Voiceover (MP3)",
                    data=audio_bytes,
                    file_name="storytimetik_voiceover.mp3",
                    mime="audio/mp3"
                )
            else:
                st.info("Voice synthesis preview ready.")

            # Scene-by-scene script cards
            st.markdown("#### 🎬 Scene Breakdown")
            for scene in story["scenes"]:
                with st.expander(f"📍 Part {scene['part']}: {scene['section']} ({scene['timestamp']})", expanded=(scene["part"] == 1)):
                    st.markdown(f"**🗣️ Spoken Voiceover:**\n> {scene['voiceover']}")
                    st.markdown(f"**👀 Visual Cue:** `{scene['visual_direction']}`")
                    st.markdown(f"**💬 On-Screen Text:** `{scene['on_screen_text']}`")

            # Hashtags
            st.markdown("#### 🏷️ Recommended Viral Hashtags")
            tags_html = "".join([f'<span class="badge-pill">{tag}</span>' for tag in story["hashtags"]])
            st.markdown(tags_html, unsafe_allow_html=True)

            # Export Options
            st.markdown("---")
            col_exp1, col_exp2 = st.columns(2)
            col_exp1.download_button(
                "📥 Export Script (JSON)",
                data=json.dumps(story, indent=2),
                file_name="story_script.json",
                mime="application/json",
                use_container_width=True
            )
            col_exp2.download_button(
                "📝 Export Teleprompter (TXT)",
                data=story["full_voiceover"],
                file_name="teleprompter_script.txt",
                mime="text/plain",
                use_container_width=True
            )


# ==========================================
# MODULE 2: Hook Virality Inspector
# ==========================================
elif module == "🔍 Hook Virality Inspector":
    st.markdown('<div class="main-header">🔍 Hook Virality Inspector</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Test your opening 3-second hook for emotional triggers, pacing, retention score, and curiosity gap before you hit record.</div>', unsafe_allow_html=True)

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

        st.markdown("---")
        st.markdown("#### 💡 Proven 3-Second Hook Formulas to Swipe:")
        st.markdown("""
        1. **The Forbidden Secret:** *"Nobody was supposed to see this security footage, but..."*
        2. **The High-Stakes Warning:** *"If you ever receive an email from this domain, delete it instantly."*
        3. **The Karmic Reversal:** *"My manager told me I was easily replaceable. Two months later..."*
        4. **The Unexpected Discovery:** *"I bought an abandoned hard drive at an estate sale for $5..."*
        """)


# ==========================================
# MODULE 3: Trending Blog & SEO Machine
# ==========================================
elif module == "📰 Trending Blog & SEO Machine":
    st.markdown('<div class="main-header">📰 Trending Blog & SEO Machine</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Automate high-converting Medium/blog articles, fetch current trending topics, and embed affiliate revenue links.</div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🔥 Real-Time Trends", "✍️ Generate SEO Article"])

    with tab1:
        st.subheader("Daily High-Traffic Niches & Search Queries")
        if st.button("🔄 Refresh Trending Topics"):
            st.session_state.trends = fetch_trending_topics()

        trends_data = st.session_state.get("trends", fetch_trending_topics())
        
        for idx, item in enumerate(trends_data, 1):
            with st.container():
                col_t1, col_t2, col_t3 = st.columns([3, 1, 1])
                col_t1.markdown(f"**{idx}. {item['topic']}**")
                col_t2.caption(f"Category: {item.get('niche', 'Trending')}")
                if col_t3.button(f"Use Topic #{idx}"):
                    st.session_state.selected_trend = item['topic']
                    st.info(f"Selected: '{item['topic']}'! Switch to the Generate tab to create the article.")

    with tab2:
        st.subheader("Create Monetized SEO Article")
        
        default_topic = st.session_state.get("selected_trend", "AI Passive Income 2026")
        topic_input = st.text_input("Article Topic", value=default_topic)
        keywords_input = st.text_input("Target SEO Keywords (comma-separated)", value="passive income, AI tools, side hustles, automation")
        
        with st.expander("💼 Custom Affiliate Links"):
            st.caption("Customize your monetization links to embed directly in the generated post.")
            aff1 = st.text_input("Affiliate 1 URL", value="https://jasper.ai/?aff=creator")
            aff2 = st.text_input("Affiliate 2 URL", value="https://elevenlabs.io/?aff=creator")

        if st.button("🚀 Generate Article", type="primary"):
            kw_list = [k.strip() for k in keywords_input.split(",") if k.strip()]
            aff_list = [
                {"name": "Jasper AI (Content Writing)", "url": aff1},
                {"name": "ElevenLabs (AI Voiceovers)", "url": aff2}
            ]
            with st.spinner("Drafting full-length SEO article..."):
                article_res = generate_seo_article(
                    topic=topic_input,
                    keywords=kw_list,
                    affiliate_links=aff_list,
                    api_key=openai_key
                )
                st.session_state.current_article = article_res

        if "current_article" in st.session_state:
            art = st.session_state.current_article
            st.success(f"Article Generated! ({art['word_count']} words)")
            st.markdown(art["content"])
            st.download_button(
                "📥 Download Article (Markdown)",
                data=art["content"],
                file_name=f"{art['topic'].lower().replace(' ', '_')}_article.md",
                mime="text/markdown"
            )


# ==========================================
# MODULE 4: Interactive Creator Tools & Portfolio
# ==========================================
elif module == "🛠️ Interactive Creator Tools":
    st.markdown('<div class="main-header">🛠️ Interactive Creator Tools & Contact</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Interactive productivity widgets, content planner, and direct collaboration form.</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.subheader("📋 Content Production To-Do Checklist")
        if "todos" not in st.session_state:
            st.session_state.todos = [
                {"task": "Record 3-second hook with dynamic camera movement", "done": True},
                {"task": "Add bold colored auto-captions with pop animations", "done": False},
                {"task": "Overlay background Minecraft or cooking gameplay b-roll", "done": False},
                {"task": "Add sound effect on the climax twist", "done": False},
                {"task": "Pin the top comment with call-to-action to Part 2", "done": False}
            ]

        for i, item in enumerate(st.session_state.todos):
            st.session_state.todos[i]["done"] = st.checkbox(item["task"], value=item["done"], key=f"todo_{i}")

        new_task = st.text_input("Add new checklist item:")
        if st.button("➕ Add Task") and new_task.strip():
            st.session_state.todos.append({"task": new_task.strip(), "done": False})
            st.rerun()

    with col2:
        st.subheader("📬 Creator Collaboration & Inquiries")
        with st.form("contact_form", clear_on_submit=True):
            name = st.text_input("Your Name / Channel")
            email = st.text_input("Your Email")
            niche = st.selectbox("Your Niche", ["TikTok / Reels Creator", "Brand / Sponsor", "Developer / Collaborator"])
            message = st.text_area("Message / Collaboration Idea")
            submitted = st.form_submit_button("Send Collaboration Request")
            if submitted:
                if not name.strip() or not email.strip() or "@" not in email:
                    st.error("Please provide a valid name and email address.")
                else:
                    st.success(f"Thank you {name}! Your message regarding '{niche}' has been received. We'll reach out to {email} shortly.")

st.markdown("---")
st.caption("StorytimeTik v2.0 • High-Performance Streamlit Studio & Multi-Platform Content Automation")
