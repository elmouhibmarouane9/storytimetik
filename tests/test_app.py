import unittest
from utils.story_engine import generate_story_script, analyze_hook_strength, STORY_ARCHETYPES
from utils.content_generator import fetch_trending_topics, generate_seo_article
from utils.voice_synth import synthesize_audio

class TestStorytimeTikSuite(unittest.TestCase):

    def test_story_generation_defaults(self):
        result = generate_story_script("confession")
        self.assertIn("title", result)
        self.assertIn("scenes", result)
        self.assertEqual(len(result["scenes"]), 5)
        self.assertGreater(result["word_count"], 50)
        self.assertTrue(result["full_voiceover"])
        self.assertTrue(len(result["hashtags"]) >= 5)

    def test_story_generation_custom_premise(self):
        custom = "I bought a mystery storage locker"
        result = generate_story_script("mystery", custom_premise=custom, pacing_seconds=90)
        self.assertIn(custom, result["hook"])
        self.assertGreater(result["estimated_duration_sec"], 30)

    def test_hook_virality_inspector(self):
        strong_hook = "I kept this secret for 5 years, and today it finally caught up with me..."
        analysis = analyze_hook_strength(strong_hook)
        self.assertIn("score", analysis)
        self.assertGreaterEqual(analysis["score"], 70)
        self.assertIn("rating", analysis)
        self.assertTrue(len(analysis["feedback"]) > 0)

    def test_trending_topics(self):
        trends = fetch_trending_topics()
        self.assertIsInstance(trends, list)
        self.assertGreater(len(trends), 0)
        self.assertIn("topic", trends[0])

    def test_seo_article_generator(self):
        article = generate_seo_article("Passive Income Automation", ["automation", "side hustle"])
        self.assertIn("content", article)
        self.assertIn("Passive Income Automation", article["content"])
        self.assertGreater(article["word_count"], 150)
        self.assertTrue("Affiliate" in article["content"] or "Creator" in article["content"])

    def test_voice_synthesis_empty_text(self):
        # Empty text should safely return None without crashing
        audio = synthesize_audio("")
        self.assertIsNone(audio)

    def test_video_compiler_subtitled_frame(self):
        from utils.video_compiler import create_subtitled_frame
        frame = create_subtitled_frame("Test story hook", "Highlight")
        self.assertEqual(len(frame.shape), 3)
        self.assertEqual(frame.shape[2], 3)

if __name__ == "__main__":
    unittest.main()
