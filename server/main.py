from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os

from pdf_extractor import extract_text_and_images, combine_videos
from gpt_analyzer import GPTAnalyzer
from veo_wrapper import VeoGenerator

app = Flask(__name__)
CORS(app)  # Allow requests from your frontend (localhost:5173, etc.)

# --- Route: Generate video from uploaded PDF ---
@app.route('/generate', methods=['POST'])
def generate_video():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    uploaded_file = request.files['file']
    question_to_answer = request.form.get("question", "")
    character_name = request.form.get("character_name", "Professor AI")
    personality = request.form.get("character_personality", "helpful and clear")
    voice_style = request.form.get("voice_style", "neutral")

    # --- If PDF file uploaded ---
    if uploaded_file.filename.endswith('.pdf'):
        # Extract text and images
        text, images = extract_text_and_images(uploaded_file)

        # Run GPT analysis to create 6-sec segments
        analyzer = GPTAnalyzer()
        summary = analyzer.analyze(
            text,
            images,
            task="""
                You are an AI teaching assistant that breaks complex topics down to simpler ones.
                Given lecture notes, you must answer the question provided using only the relevant
                sections of the provided notes.
                Divide the answer into short, self-contained segments that can be narrated in ~6 seconds each.
                Each segment should make sense on its own, avoid cutting sentences awkwardly,
                and include all essential points.
                Return your output in JSON format as a list of segments:
                [
                    {"segment": "Text for first 6-second video."},
                    {"segment": "Text for second 6-second video."},
                    ...
                ]
                There should be at most 4 summaries, totalling around 24 seconds of speaking.
            """,
            question=question_to_answer
        )

        # Convert GPT JSON into Python list
        try:
            segments = json.loads(summary)
        except Exception as e:
            return jsonify({'error': f'GPT returned invalid JSON: {str(e)}'}), 500

        # Generate videos for each segment using Gemini Veo
        os.makedirs("videos", exist_ok=True)
        video_files = []
        veo = VeoGenerator()

        for i, seg in enumerate(segments, 1):
            if i == 2:
                break
            text_segment = seg.get("segment", "")
            print(f"🎬 Generating segment {i}: {text_segment[:60]}...")
            save_path = veo.generateVideo(
                character_name,
                personality,
                voice_style,
                text_segment,
                "Infographic style with clear diagrams, bright colors, minimal text",
                i
            )
            video_files.append(save_path)

        # Combine all generated clips
        final_path = combine_videos(video_files)
        final_url = f"http://localhost:5000/videos/{os.path.basename(final_path)}"

        print(f"✅ Final combined video ready at: {final_url}")

        return jsonify({
            'text': text,
            'video_url': final_url
        })

    # --- If text file uploaded instead ---
    else:
        text = uploaded_file.read().decode('utf-8', errors='ignore')
        return jsonify({'text': text, 'video_url': None})


# --- Route: Serve generated videos ---
@app.route('/videos/<path:filename>')
def serve_video(filename):
    return send_from_directory(os.path.dirname(__file__), filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
