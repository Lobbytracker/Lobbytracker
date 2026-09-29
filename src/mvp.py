import openai
import os
import csv
from pathlib import Path
from dotenv import load_dotenv


class LlmManager:
    def __init__(self, text_path, data):
        self.url = "https://aitta-api.csc.fi/openai/v1"
        self.model = "openai/gpt-oss-120b"
        self.text_path = Path(text_path)
        self.data = data

    def call_aitta(self):
        load_dotenv()

        key = os.getenv("AITTA_API_KEY")
        document = self.text_path.read_text(encoding="utf-8")
        concepts = [row["concept"] for row in self.data]
        concepts = concepts[:3]  # Limit to first 3 concepts for demonstration

        instructions = (
            "Determine whether the concept appears in the document. "
            "Answer with the concept_id, a yes/no decision, and a short quote "
            "from the document as evidence. Concepts:\n" + "\n".join(concepts)
        )

        client = openai.OpenAI(api_key=key, base_url=self.url)
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": instructions},
                {"role": "user", "content": document},
            ],
            model=self.model,
            stream=True,
        )

        return chat_completion
