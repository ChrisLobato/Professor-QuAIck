from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
import re

from pdf_extractor import extract_text_and_images, combine_videos
from gpt_analyzer import GPTAnalyzer
from veo_wrapper import VeoGenerator

app = Flask(__name__)
CORS(app)  # Allow requests from frontend (localhost:5173, etc.)


# --- Helper: Save extracted images to local folder ---
def save_images_locally(images, folder="videos/images"):
    os.makedirs(folder, exist_ok=True)
    saved_paths = []
    for img in images:
        filename = f"page{img['page']}_img{img['index']}.{img['ext']}"
        filepath = os.path.join(folder, filename)
        try:
            with open(filepath, "wb") as f:
                f.write(img["bytes"])
            saved_paths.append(filepath)
        except Exception as e:
            print(f"⚠️ Failed to save image {filename}: {e}")
    print(f"✅ Saved {len(saved_paths)} image(s) to {folder}")
    return saved_paths


# --- Route: Generate video from uploaded PDF ---
@app.route("/generate", methods=["POST"])
def generate_video():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    uploaded_file = request.files["file"]
    question_to_answer = request.form.get("question", "")
    character_name = request.form.get("character_name", "Professor AI")
    personality = request.form.get("character_personality", "helpful and clear")
    voice_style = request.form.get("voice_style", "neutral")

    # --- If PDF file uploaded ---
    if uploaded_file.filename.endswith(".pdf"):
        # 1️⃣ Extract text and images
        text, images = extract_text_and_images(uploaded_file)
        image_paths = save_images_locally(images)

        # 2️⃣ Run GPT analysis
        analyzer = GPTAnalyzer()
        summary = analyzer.analyze(
            text,
            images,
            task="""
                You are an AI teaching assistant that breaks complex topics down into clear explanations.
                Use both the text and figures provided in the lecture notes to answer the question.
                When relevant, reference diagrams (e.g., 'as shown in the figure below').
                Return up to 4 short narration segments (~6 seconds each) as valid JSON:
                [
                    {"segment": "Text for segment 1"},
                    {"segment": "Text for segment 2"}
                ]
            """,
            question=question_to_answer,
        )

        # 3️⃣ Clean and parse GPT JSON output
        cleaned_summary = re.sub(r"```(?:json)?|```", "", summary).strip()
        try:
            segments = json.loads(cleaned_summary)
        except Exception as e:
            print("❌ JSON parsing failed:", e)
            print("Raw GPT output (first 400 chars):", summary[:400])
            return jsonify({
                "error": f"GPT returned invalid JSON: {str(e)}"
            }), 500

        # 4️⃣ Generate videos for each segment
        os.makedirs("videos", exist_ok=True)
        veo = VeoGenerator()
        video_files = []

        for i, seg in enumerate(segments, 1):
            # if i == 2:  # limit to 4 short clips max
            #     break

            text_segment = seg.get("segment", "").strip()
            if not text_segment:
                continue

            print(f"🎬 Generating segment {i}: {text_segment[:80]}...")
            save_path = veo.generateVideo(
                character_name,
                personality,
                voice_style,
                text_segment,
                "Infographic style with clear diagrams and vibrant visuals",
                i,
                image_paths=image_paths,  # for prompt context
            )

            # ✅ Add the generated file if it exists
            if save_path and os.path.exists(save_path):
                video_files.append(save_path)
                print(f"✅ Added to combine list: {save_path}")
            else:
                print(f"⚠️ Skipping segment {i} — no valid video file returned.")

        # 5️⃣ Combine generated clips
        final_path = combine_videos(video_files)

        if not final_path:
            print("⚠️ Skipping final combination — no video files were generated.")
            return jsonify({
                "text": text,
                "video_url": None,
                "warning": "No video clips were generated successfully."
            }), 200

        final_url = f"http://localhost:5000/videos/{os.path.basename(final_path)}"
        print(f"✅ Final combined video ready at: {final_url}")

        return jsonify({
            "text": text,
            "video_url": final_url
        })

    # --- If text file uploaded instead ---
    else:
        text = uploaded_file.read().decode("utf-8", errors="ignore")
        return jsonify({"text": text, "video_url": None})


# --- Route: Serve generated videos ---
@app.route("/videos/<path:filename>")
def serve_video(filename):
    video_dir = os.path.join(os.path.dirname(__file__), "videos")
    if not os.path.exists(os.path.join(video_dir, filename)):
        return jsonify({"error": "Video not found"}), 404
    return send_from_directory(video_dir, filename, mimetype="video/mp4")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
