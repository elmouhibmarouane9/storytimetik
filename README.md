# 🎬 StorytimeTik Studio & Content Engine

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://storytimetik.streamlit.app)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

An all-in-one AI-powered creator studio and automation platform built for TikTok, Reels, YouTube Shorts, and SEO monetization.

---

## 🚀 Key Modules & Features

### 1. ⚡ TikTok Storytime Generator
- Generates retention-engineered viral story scripts based on proven engagement archetypes:
  - Confessions & Secrets
  - Unexplained Mysteries & Glitches
  - Workplace Revenge & Karma
  - Relationship Red Flags
  - Crazy Entrepreneur Wins & Passive Income
- Breaks scripts down into parts with exact timestamps, visual cues, and on-screen text overlays.
- Integrates Text-to-Speech (TTS) audio narration preview with single-click MP3 download.
- Full JSON & Teleprompter text exports.

### 2. 🔍 Hook Virality Inspector
- Analyzes the opening 3-second hook for retention score, emotional trigger keywords, pacing, and curiosity gap.
- Provides actionable scoring feedback and proven swipe-file templates.

### 3. 📰 Trending Blog & SEO Machine
- Pulls live daily high-traffic trends and queries.
- Drafts structured 1,200+ word SEO blog posts with automatic affiliate monetization links.
- Supports both OpenAI GPT-4o-mini generation and smart offline heuristic template rendering.

### 4. 🌐 REST API (`api_app.py`)
- Headless Flask API endpoints for automated cron jobs or external integrations:
  - `GET /health`: Service health check.
  - `GET /trends`: Retrieve real-time search trends.
  - `POST /generate-story`: Headless story script generator.
  - `POST /generate-article`: Automated SEO article writer.
  - `POST /analyze-hook`: Hook scoring endpoint.

---

## 🛠️ Quickstart

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Launch the Streamlit Studio App
```bash
streamlit run streamlit_app.py
```

### 3. (Optional) Run the Headless API Service
```bash
python api_app.py
```

### 4. Run Test Suite
```bash
python -m unittest discover -s tests -p "test_*.py"
```

---

## 📁 Repository Structure

```
├── streamlit_app.py          # Main interactive Streamlit creator studio
├── api_app.py                # Standalone Flask API for headless generation
├── requirements.txt          # Python dependencies
├── utils/
│   ├── story_engine.py       # Story script archetypes & hook virality engine
│   ├── voice_synth.py        # gTTS audio narration synthesizer
│   └── content_generator.py  # Trend scraping & SEO article generator
└── tests/
    └── test_app.py           # Comprehensive automated unit test suite
```
