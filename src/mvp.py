import openai
import os
from pathlib import Path
from dotenv import load_dotenv


class LlmManager:
    def __init__(self, text_path, data):
        self.url = "https://aitta-api.csc.fi/openai/v1"
        self.model = "openai/gpt-oss-120b"
        self.text_path = Path(text_path)
        self.data = data[0:2]  # Limit to first two concepts for testing
        self.session_list = []

    def call_aitta(self):
        load_dotenv()

        key = os.getenv("AITTA_API_KEY")
        document = self.text_path.read_text(encoding="utf-8")

        client = openai.OpenAI(api_key=key, base_url=self.url)
        for row in self.data:
            concept = row["concept"]
            instructions = (
                "Determine whether the following concept appears in the document. "
                "Answer with a yes/no decision and a short quote from the document "
                f"as evidence. Concept: {concept}"
            )

            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": instructions},
                    {"role": "user", "content": document},
                ],
                model=self.model,
            )
            self.session_list.append(response.choices[0].message.content)

        return self.session_list
