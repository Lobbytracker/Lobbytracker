from ntpath import join

import openai
import os
from dotenv import load_dotenv


class LlmManager:
    def __init__(self, documents, concepts):
        self.url = "https://aitta-api.csc.fi/openai/v1"
        self.model = "openai/gpt-oss-120b"
        self.documents = documents[0]["content"]  # first document for testing
        self.concepts = concepts[0:5]  # Limit to first two concepts for testing
        self.session_list = []

    def call_aitta(self):
        load_dotenv()

        key = os.getenv("AITTA_API_KEY")
        document = self.documents

        client = openai.OpenAI(api_key=key, base_url=self.url)
        for row in self.concepts:
            concept = row["concept"]
            concept_id = row["id"]
            instructions = (f"""
                Determine whether the following concept appears in the document.
                Answer with a yes/no decision and a passage from the document
                which matches the concept as evidence. Concept: {concept}.
                Give the output in json form. Do not return "yes" unless you can
                provide a supporting passage.

                Output format:

                {{
                    "{concept_id}:": {{
                    "concept": "{concept}",
                    "decision": "yes" or "no",
                    "passage": "verbatim supported passage" or null
                    }}
                }}
            """
            )

            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": instructions},
                    {"role": "user", "content": document},
                ],
                model=self.model,
            )
            self.session_list.append(response.choices[0].message.content)

        return "\n".join(self.session_list)
