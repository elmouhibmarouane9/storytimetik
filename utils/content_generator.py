import os
import requests
from typing import List, Dict, Any, Optional
from datetime import datetime

DEFAULT_TRENDS = [
    {"topic": "AI Passive Income 2026", "traffic": "250K+", "niche": "Tech / Finance"},
    {"topic": "Viral TikTok Storytelling Hacks", "traffic": "180K+", "niche": "Content Creation"},
    {"topic": "Top 10 Micro-SaaS Side Hustles", "traffic": "140K+", "niche": "Business / Tech"},
    {"topic": "Workplace Red Flags You Missed", "traffic": "320K+", "niche": "Storytime / Lifestyle"},
    {"topic": "Best AI Tools For Creators This Month", "traffic": "95K+", "niche": "Productivity"}
]

def fetch_trending_topics() -> List[Dict[str, Any]]:
    """
    Fetch trending search queries or return curated high-engagement niches.
    """
    try:
        url = "https://trends.google.com/trends/trendingsearches/daily/rss?geo=US"
        resp = requests.get(url, timeout=4)
        if resp.status_code == 200:
            import xml.etree.ElementTree as ET
            root = ET.fromstring(resp.content)
            items = []
            for item in root.findall(".//item")[:5]:
                title = item.find("title")
                approx_traffic = item.find("{https://trends.google.com/trends/trendingsearches/daily}approx_traffic")
                traffic_str = approx_traffic.text if approx_traffic is not None and approx_traffic.text else "Trending"
                if title is not None and title.text:
                    items.append({
                        "topic": title.text,
                        "traffic": traffic_str,
                        "niche": "Daily Trending Search"
                    })
            if items:
                return items
    except Exception as exc:
        pass
    return DEFAULT_TRENDS


def generate_seo_article(
    topic: str,
    keywords: List[str],
    affiliate_links: Optional[List[Dict[str, str]]] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generate an SEO-optimized blog / newsletter article with monetization affiliate placeholders.
    Supports OpenAI if key is present, otherwise produces a high-quality Markdown template structure.
    """
    date_str = datetime.now().strftime("%B %d, %Y")
    kw_str = ", ".join(keywords)

    if not affiliate_links:
        affiliate_links = [
            {"name": "Jasper AI (Content Writing)", "url": "https://jasper.ai/?aff=creator"},
            {"name": "ElevenLabs (AI Voiceovers)", "url": "https://elevenlabs.io/?aff=creator"},
            {"name": "Notion AI (Workflow Hub)", "url": "https://notion.so/?aff=creator"}
        ]

    # If OpenAI API key is supplied, attempt live completion
    if api_key:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            prompt = (
                f"Write a 1200-word engaging, SEO-optimized blog article on '{topic}'. "
                f"Primary SEO keywords: {kw_str}. Current date: {date_str}. "
                f"Include an eye-catching H1 title, quick executive summary, 4 structured sections with bullet points, "
                f"actionable step-by-step guidance, and a compelling conclusion with call to action. Return in Markdown."
            )
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2200
            )
            article_body = response.choices[0].message.content
        except Exception as exc:
            article_body = _fallback_article_template(topic, keywords, date_str)
    else:
        article_body = _fallback_article_template(topic, keywords, date_str)

    # Append disclosure and affiliate links
    affiliate_section = "\n\n---\n\n### 🔗 Featured Creator & Monetization Resources\n"
    for link in affiliate_links:
        affiliate_section += f"- **[{link['name']}]({link['url']})**: Boost your production speed.\n"
    affiliate_section += "\n*Earnings Disclaimer: Some links above may be affiliate links. We may earn a commission at no additional cost to you.*\n"

    final_content = article_body + affiliate_section

    return {
        "topic": topic,
        "keywords": keywords,
        "date": date_str,
        "content": final_content,
        "word_count": len(final_content.split())
    }


def _fallback_article_template(topic: str, keywords: List[str], date_str: str) -> str:
    kw_tags = " • ".join(f"`{k}`" for k in keywords)
    return f"""# Master {topic}: The Comprehensive 2026 Strategy Guide

*Published on {date_str} • Reading time: 5 minutes*

**Target Keywords**: {kw_tags}

---

## 📌 Executive Summary
In today's fast-moving digital economy, understanding **{topic}** separates the casual observers from creators and businesses generating consistent impact. This in-depth guide reveals the key dynamics, actionable tactical steps, and high-leverage tools to capitalize on this trend right now.

---

## 1. Why {topic} Matters More Than Ever
Consumer attention is shifting at unprecedented speed. Audiences value authentic storytelling, high-speed execution, and streamlined workflows. Whether you are building an audience or monetizing digital products:

- **Algorithmic Velocity**: Platforms reward high retention, dynamic pacing, and consistent messaging.
- **Micro-Audience Monetization**: You no longer need millions of followers to generate significant revenue.
- **Tool Automation**: Workflows that used to take entire production teams now take minutes with modern AI pipelines.

---

## 2. Strategic Framework & Step-by-Step Implementation

1. **Identify the Core Hook**: Every piece of content or marketing campaign succeeds or fails in the first 3 seconds.
2. **Structure the Tension**: Deliver continuous micro-payoffs to keep readers and viewers invested until the very end.
3. **Execute Clean Distribution**: Repurpose long-form assets across TikTok, Instagram Reels, YouTube Shorts, and newsletters.
4. **Build the Monetization Flywheel**: Direct traffic to email newsletters, digital downloads, and trusted affiliate partnerships.

---

## 3. Real-World Case Studies & Performance Benchmarks
Top operators in this niche focus on **clarity over complexity**. By refining the headline and hook:
- Click-through rates often improve by **2.4x to 3.8x**.
- Viewer retention in the first 10 seconds jumps above **65%**.
- Conversion on affiliate and digital offerings doubles through clear, value-driven calls to action.

---

## 4. Key Takeaways & Action Checklist
- [x] Pick your high-leverage niche and define 3 primary keywords.
- [x] Test at least 3 distinct hook variations before launching.
- [x] Maintain ethical disclosures on all monetization funnels.
- [x] Reinvest in tools that automate your repetitive production tasks.

---
"""
