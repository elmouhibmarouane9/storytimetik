from flask import Flask, request, jsonify
import os
from utils.content_generator import fetch_trending_topics, generate_seo_article
from utils.story_engine import generate_story_script, analyze_hook_strength

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "app": "storytimetik-api", "version": "2.5.0"})

@app.route('/render-video', methods=['POST'])
def render_video_endpoint():
    data = request.get_json(silent=True) or {}
    story_data = data.get('story')
    if not story_data or 'scenes' not in story_data:
        archetype = data.get('archetype', 'confession')
        story_data = generate_story_script(archetype=archetype)
    
    fps = int(data.get('fps', 15))
    import tempfile
    output_mp4 = os.path.join(tempfile.gettempdir(), 'rendered_api_story.mp4')
    from utils.video_compiler import assemble_story_video
    success = assemble_story_video(story_data['scenes'], output_mp4, fps=fps)
    return jsonify({
        "status": "success" if success else "error",
        "video_path": output_mp4 if success else None,
        "exists": os.path.exists(output_mp4)
    })

@app.route('/trends', methods=['GET'])
def trends():
    topics = fetch_trending_topics()
    return jsonify({"trends": topics, "count": len(topics)})

@app.route('/generate-article', methods=['POST'])
def generate_article_endpoint():
    data = request.get_json(silent=True) or {}
    topic = data.get('topic', 'AI Passive Income 2026')
    keywords = data.get('keywords', ['passive income', 'creator economy', 'AI tools'])
    api_key = data.get('api_key') or os.getenv('OPENAI_API_KEY')
    result = generate_seo_article(topic=topic, keywords=keywords, api_key=api_key)
    return jsonify({"status": "success", "data": result})

@app.route('/generate-story', methods=['POST'])
def generate_story_endpoint():
    data = request.get_json(silent=True) or {}
    archetype = data.get('archetype', 'confession')
    premise = data.get('premise')
    seconds = int(data.get('pacing_seconds', 60))
    story = generate_story_script(archetype=archetype, custom_premise=premise, pacing_seconds=seconds)
    return jsonify({"status": "success", "story": story})

@app.route('/analyze-hook', methods=['POST'])
def analyze_hook_endpoint():
    data = request.get_json(silent=True) or {}
    hook = data.get('hook', '')
    analysis = analyze_hook_strength(hook)
    return jsonify({"status": "success", "analysis": analysis})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
