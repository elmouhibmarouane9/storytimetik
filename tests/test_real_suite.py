import unittest
from utils.story_engine import generate_story_script, analyze_hook_strength
from utils.reddit_scraper import fetch_reddit_storytime, REDDIT_CURATED_STORIES
from utils.background_generator import get_procedural_background_frame
from utils.video_compiler import create_subtitled_frame, assemble_story_video
from utils.notion_sync import format_notion_payload
from utils.voice_synth import synthesize_audio, VOICE_PROFILES

class TestStorytimeTikRealSuite(unittest.TestCase):

    def test_reddit_ingestion(self):
        story = fetch_reddit_storytime("curated", "r/Confession")
        self.assertIn("subreddit", story)
        self.assertEqual(story["subreddit"], "r/Confession")
        self.assertGreater(len(story["scenes"]), 0)
        self.assertTrue(story["full_voiceover"])

    def test_background_frame_generation(self):
        frame_mc = get_procedural_background_frame("minecraft", 360, 640, 5)
        self.assertEqual(frame_mc.shape, (640, 360, 3))
        frame_tunnel = get_procedural_background_frame("tunnel", 360, 640, 5)
        self.assertEqual(frame_tunnel.shape, (640, 360, 3))

    def test_split_screen_subtitled_frame(self):
        header = {"subreddit": "r/Confession", "author": "u/Test", "title": "Big secret", "upvotes": "10K"}
        frame = create_subtitled_frame("Test spoken word line", "Climax cue", active_word_idx=2, reddit_header=header, width=360, height=640)
        self.assertEqual(frame.shape, (640, 360, 3))

    def test_notion_payload_format(self):
        story = {"title": "Test Title", "hook": "Test hook", "full_voiceover": "voiceover here", "hashtags": ["#tag1"]}
        payload = format_notion_payload(story, scheduled_date="2026-11-01")
        self.assertIn("properties", payload)
        self.assertIn("Content Title", payload["properties"])
        self.assertEqual(payload["properties"]["Status"]["select"]["name"], "Ready to Post")

    def test_voice_profiles(self):
        self.assertIn("narrator_male", VOICE_PROFILES)
        self.assertIn("narrator_female", VOICE_PROFILES)
        audio = synthesize_audio("Quick test line", voice_key="narrator_male")
        self.assertIsNotNone(audio)
        self.assertGreater(len(audio), 100)

if __name__ == "__main__":
    unittest.main()
