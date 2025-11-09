import base64
from openai import OpenAI
import os

class GPTAnalyzer:
    """Analyzes extracted PDF content using OpenAI GPT (multimodal safe)."""

    def __init__(self, model="gpt-4o-mini"):  # ✅ multimodal-capable
        openai_key = os.getenv("GPT_API_KEY")
        self.client = OpenAI(api_key=openai_key)
        self.model = model

    def analyze(self, text, images=None, task="Summarize this PDF", question="summarize"):
        """
        Analyze lecture text + (optionally) images.
        Falls back to text-only if multimodal call fails.
        """
        image_inputs = []
        if images:
            for img in images[:3]: 
                try:
                    b64 = base64.b64encode(img["bytes"]).decode("utf-8")
                    mime_type = f"image/{img.get('ext', 'jpeg')}"
                    data_uri = f"data:{mime_type};base64,{b64}"
                    image_inputs.append({
                        "type": "input_image",
                        "image_url": data_uri
                    })
                except Exception as e:
                    print(f"⚠️ Skipping image on page {img.get('page', '?')}: {e}")

        input_content = [
            {
                "role": "system",
                "content": [
                    {"type": "input_text", "text": task}
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": f"Question: {question}\nLecture Notes: {text[:8000]}"
                    }
                ] + image_inputs  # attach images if any
            }
        ]

        try:
            print(f"🧠 Sending to GPT model {self.model} with {len(image_inputs)} image(s)...")
            response = self.client.responses.create(
                model=self.model,
                input=input_content
            )
            print("✅ GPT multimodal response received.")
            return response.output_text

        except Exception as e:
            print(f"⚠️ GPT multimodal call failed: {e}")
            print("↩️ Falling back to text-only mode...")

            # 3️⃣ Retry with text-only input
            text_only_input = [
                {
                    "role": "system",
                    "content": [
                        {"type": "input_text", "text": task}
                    ]
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": f"Question: {question}\nLecture Notes: {text[:8000]}"
                        }
                    ]
                }
            ]

            response = self.client.responses.create(
                model=self.model,
                input=text_only_input
            )
            print("✅ GPT text-only response received (fallback).")
            return response.output_text
