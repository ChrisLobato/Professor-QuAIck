import time
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
load_dotenv()

class VeoGenerator:
    def __init__(self):
        gemini_key = os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=gemini_key)


    def generateVideo(self, character_name, personality, voice, dialogue_text, video_style, chunk_i):
        prompt = f"""Generate a video with the following parameters,
        subject: {character_name} narrating the dialogue with a {personality} personality, and a {voice} voice
        dialogue: {dialogue_text}
        style: {video_style}
        """
        

        operation = self.client.models.generate_videos(
            model="veo-3.1-generate-preview",
            prompt=prompt,
        )

        # Poll the operation status until the video is ready.
        while not operation.done:
            print("Waiting for video generation to complete...")
            time.sleep(10)
            operation = self.client.operations.get(operation)

        # Download the generated video.
        generated_video = operation.response.generated_videos[0]
        self.client.files.download(file=generated_video.video)
        generated_video.video.save(str(chunk_i)+"_video_explanation.mp4")
        print(chunk_i,"Generated video saved to video_explanation.mp4")