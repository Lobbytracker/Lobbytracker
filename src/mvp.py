import openai
import os
from urllib.request import Request, urlopen
import json
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Literal

AITTA_URL = "https://aitta-api.csc.fi"
DEFAULT_MODEL = "openai/gpt-oss-120b"
REQUEST_TIMEOUT_SECONDS = 300


def get_available_models():
    """Return model IDs advertised by Aitta's model endpoint."""
    load_dotenv()

    headers = {}
    key = os.getenv("AITTA_API_KEY")
    if key:
        headers["Authorization"] = f"Bearer {key}"

    request = Request(f"{AITTA_URL}/model", headers=headers)
    with urlopen(request, timeout=10) as response:
        payload = json.load(response)

    if isinstance(payload, dict):
        models = payload.get("data", payload.get("models"))
        if models is None:
            models = payload.get("_links", {}).get("item", [])
    else:
        models = payload

    model_ids = []
    for model in models:
        if isinstance(model, str):
            model_id = model
            model_info = {}
        else:
            model_id = model.get("id") or model.get("name")
            model_info = model

        if not model_info.get("capabilities") and isinstance(model, dict):
            href = model.get("href")
            if href:
                details_request = Request(f"{AITTA_URL}{href}", headers=headers)
                try:
                    with urlopen(details_request, timeout=10) as response:
                        model_info = json.load(response)
                except OSError:
                    continue

        if (
            model_id
            and "openai-chat-completion" in model_info.get("capabilities", [])
            and model_id not in model_ids
        ):
            model_ids.append(model_id)

    return model_ids


class ConceptResult(BaseModel):
       decision: Literal["yes", "no"]
       passage: str | None

class LlmManager:
    def __init__(self, documents, concepts, model=DEFAULT_MODEL):
        self.url = "https://aitta-api.csc.fi/openai/v1"
        self.model = model
        self.documents = documents[0]["content"]  # first document for testing
        self.concepts = concepts[0:2]  # Limit to first two concepts for testing
        self.session_list = []

    def call_aitta(self):
        load_dotenv()

        key = os.getenv("AITTA_API_KEY")
        document = self.documents

        client = openai.OpenAI(
            api_key=key,
            base_url=self.url,
            timeout=REQUEST_TIMEOUT_SECONDS,
            max_retries=0,
        )
        for row in self.concepts:
            concept = row["concept"]
            concept_id = row["id"]

            instructions = (
                "Determine whether the following concept appears in the document. "
                "If it does, give the passage from the document that expresses it, "
                "quoted exactly as written, without markdown or ellipses. "
                "If it does not, give null. "
                'Do not answer "yes" unless you can provide a supporting passage.\n'
                f"Concept: {concept}"
            )       

            response = client.beta.chat.completions.parse(
                messages=[
                    {"role": "system", "content": instructions},
                    {"role": "user", "content": document},
                ],
                model=self.model,
                response_format=ConceptResult,
            )

            result = response.choices[0].message.parsed

            self.session_list.append({
                "concept_id": concept_id,
                "concept": concept,
                "decision": result.decision,
                "passage": result.passage,
            })

        return self.session_list
