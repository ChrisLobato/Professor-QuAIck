# gpt_analyzer.py
import base64
from openai import OpenAI
import os

class GPTAnalyzer:
    """Analyzes extracted PDF content using OpenAI GPT."""
    
    def __init__(self, model="gpt-4.1-mini"):
        openAI_key = os.getenv("GPT_API_KEY")
        self.client = OpenAI(api_key=openAI_key)
        self.model = model

    def analyze(self, text, images=None, task="Summarize this PDF", question="summarize"):
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
                    {"type": "input_text", "text": f"Question: {question}\nLecture Notes: {text[:8000]}"}
                ]
            }
        ]

        response = self.client.responses.create(
            model=self.model,
            input=input_content
        )

        return response.output_text
