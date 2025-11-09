import time
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
load_dotenv()

import os

class VeoGenerator:
    def __init__(self):
        gemini_key = os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=gemini_key)
        os.makedirs("videos", exist_ok=True)  # <--- create folder if missing

    def generateVideo(
        self,
        character_name,
        personality,
        voice,
        dialogue_text,
        video_style,
        chunk_i,
        image_paths=None,  # ✅ allow images to be passed in
    ):
        """
        Generate an AI lecture video clip.
        Optionally includes extracted images from the source PDF as visual inspiration.
        """

        # 🧠 Construct prompt dynamically
        prompt = f"""Generate a video with the following parameters:
        - Character: {character_name}, speaking with a {personality} personality and a {voice} voice.
        - Dialogue: {dialogue_text}
        - Visual style: {video_style}.
        """

        # 🖼️ If we have image paths, mention them in the visual guidance
        if image_paths and len(image_paths) > 0:
            joined_images = ", ".join(image_paths[:3])  # limit to first 3 for prompt size
            prompt += f"\nIncorporate visuals or themes inspired by the following images: {joined_images}"

        # 🎬 Generate the video
        print(f"🎨 Sending prompt to Veo with {len(image_paths) if image_paths else 0} image(s)...")
        operation = self.client.models.generate_videos(
            model="veo-3.1-generate-preview",
            prompt=prompt,
        )

        while not operation.done:
            print("Waiting for video generation to complete...")
            time.sleep(10)
            operation = self.client.operations.get(operation)

        # 🧩 Save generated video
        generated_video = operation.response.generated_videos[0]
        self.client.files.download(file=generated_video.video)

        save_path = os.path.join("videos", f"{chunk_i}_video_explanation.mp4")
        generated_video.video.save(save_path)

        print(f"✅ Video {chunk_i} saved at {save_path}")
        return save_path
