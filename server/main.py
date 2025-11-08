from flask import Flask, request, jsonify
from flask_cors import CORS
import io
import json

from pdf_extractor import extract_text_and_images
from pdf_extractor import combine_videos
from gpt_analyzer import GPTAnalyzer
from veo_wrapper import VeoGenerator

app = Flask(__name__)
CORS(app)  # Allow requests from your frontend (localhost:5173, etc.)

@app.route('/generate', methods=['POST'])
def generate_video():
    if 'file' not in request.files:
        return jsonify({'error': 'No File uploaded'}), 400
    uploaded_file = request.files['file']
    questionToAnswer = request.form.get("question")
    character_name = request.form.get("character_name")
    personality = request.form.get("character_personality")
    voice_style = request.form.get("voice_style")
        # Check file type
    if uploaded_file.filename.endswith('.pdf'):
        # Extract text from PDF
        text, images = extract_text_and_images(uploaded_file)
        analyzer = GPTAnalyzer()

        summary = analyzer.analyze(
        text,
        images,
        task=f"""
            You are an AI teaching assistant that breaks complex topics down to simpler ones. Given lecture notes you must answer the question provided
            utilizing only the relevant sections of the provided lecture notes to create an answer.
            Divide the answer into short, self-contained segments that can be narrated in ~6 seconds each"
            Each segment should make sense on its own, avoid cutting sentences in awkward places, and include all essential points
            Return your output in JSON format as a list of segments:
            [
            {{'segment': 'Text for first 6-second video.'}},
            {{'segment': 'Text for second 6-second video.'}},
            ...
            ]
            There should be at max 4 summaries, which will equal 24 seconds of speaking
        """,
        question=questionToAnswer
        )
        segments = json.loads(summary)
        video_files = []
        for i, seg in enumerate(segments, 1):
            text = seg["segment"]
            veo = VeoGenerator()
            veo.generateVideo(character_name, personality, voice_style, text, "Infographic style with clear diagrams and bright colors and minimal text", i)
            video_files.append(f"{i}_video_explanation.mp4")
            # print(f"Segment {i}: {text}")
        combine_videos(video_files) # feed in something for second argument at a later point to differentiate all the files being created
    else:
        # Fallback: treat as plain text
        text = uploaded_file.read().decode('utf-8', errors='ignore')

    # Respond with extracted text
    return jsonify({'text': text})

if __name__ == '__main__':
    app.run(debug=True, port=5000)