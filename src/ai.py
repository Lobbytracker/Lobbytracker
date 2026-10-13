import asyncio
import json
import os
from typing import Literal
from urllib.request import Request, urlopen

import openai
from dotenv import load_dotenv
from pydantic import BaseModel

from db import save_output

AITTA_URL = "https://aitta-api.csc.fi"
DEFAULT_MODEL = "openai/gpt-oss-120b"
REQUEST_TIMEOUT_SECONDS = 300


def get_available_models():
    """Return model IDs from Aitta that support chat completion."""
    load_dotenv()

    headers = {}
    key = os.getenv("AITTA_API_KEY")
    if key:
        headers["Authorization"] = f"Bearer {key}"

    request = Request(f"{AITTA_URL}/model", headers=headers)
    with urlopen(request, timeout=10) as response:
        payload = json.load(response)

    model_ids = []
    for item in payload.get("_links", {}).get("item", []):
        details_request = Request(f"{AITTA_URL}{item['href']}", headers=headers)
        try:
            with urlopen(details_request, timeout=10) as response:
                details = json.load(response)
        except OSError:
            continue

        if "openai-chat-completion" in details.get("capabilities", []):
            model_ids.append(item["name"])

    return model_ids


class ConceptResult(BaseModel):
       decision: Literal["yes", "no"]
       passage: str | None

class LlmManager:
    def __init__(self, documents, concepts, model=DEFAULT_MODEL):
        self.url = "https://aitta-api.csc.fi/openai/v1"
        self.model = model
        self.documents = documents[0]  # first document for testing
        self.concepts = concepts[0:2]  # Limit to first two concepts for testing
        self.session_list = []
        self.client = self.create_client()

    def create_client(self) -> openai.OpenAI:
        load_dotenv()

        key = os.getenv("AITTA_API_KEY")

        return openai.OpenAI(
            api_key=key,
            base_url=self.url,
            timeout=REQUEST_TIMEOUT_SECONDS,
            max_retries=0,
        )

    def API_call(self, concept, document):
        concept_definition = concept["concept"]
       # concept_id = concept["id"]

        instructions = (
            "Determine whether the following concept appears in the document. "
            "If it does, give the passage from the document that expresses it, "
            "quoted exactly as written, without markdown or ellipses. "
            "If it does not, give null. "
            'Do not answer "yes" unless you can provide a supporting passage.\n'
            f"Concept: {concept_definition}"
        )                  

        self.create_client()

        response = self.client.beta.chat.completions.parse(
            messages=[
                {"role": "system", "content": instructions},
                {"role": "user", "content": document},
            ],
            model=self.model,
            response_format=ConceptResult,
        )

        result = response.choices[0].message.parsed

        return result
    

    def call_aitta(self):

        if not self.client:
            self.create_client()

        document = self.documents["content"]
        document_id = self.documents["id"]

    
        for concept in self.concepts:
            result = self.API_call(concept, document)

            self.session_list.append({
                "document_id": document_id,
                "concept_id": concept["id"],
                "concept": concept["concept"],
                "decision": result.decision,
                "passage": result.passage,
            })

        self.output_to_db()

        return self.session_list

    def output_to_db(self):
        asyncio.run(save_output(self.session_list))
