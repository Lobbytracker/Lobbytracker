import openai
import os
from urllib.request import Request, urlopen
import json
from dotenv import load_dotenv

AITTA_URL = "https://aitta-api.csc.fi"
DEFAULT_MODEL = "openai/gpt-oss-120b"
REQUEST_TIMEOUT_SECONDS = 120


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

        return "\n".join(self.session_list)
