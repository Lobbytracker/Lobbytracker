import asyncio
import json
import os
from urllib.request import Request, urlopen

import openai
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError

from db.db_calls import create_evaluation_run, save_evaluation_run, save_output
from tui.tui_io import TuiIO

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
    """Structured result of checking a concept in a document."""
    present: bool
    passage: str | None
    agreement: bool | None


class LlmManager:
    """Call the language model and store concept analysis results."""
    def __init__(self, documents, concepts, model=DEFAULT_MODEL, io=TuiIO):
        self.io = io
        self.url = "https://aitta-api.csc.fi/openai/v1"
        self.model = model
        self.documents = documents if documents else None
        self.concepts = concepts if concepts else None
        self.session_list = []
        self.failed_api_calls = []
        self.client = self.create_client()

    def create_client(self) -> openai.OpenAI:
        """Create and return an OpenAI client configured for the Aitta API."""
        load_dotenv()

        key = os.getenv("AITTA_API_KEY")

        return openai.OpenAI(
            api_key=key,
            base_url=self.url,
            timeout=REQUEST_TIMEOUT_SECONDS,
            max_retries=0,
        )

    def create_connection(self):
        """Checks whether the selected model responds to a test request."""
        try:
            # instruction = "say hello"
            response = self.client.beta.chat.completions.parse(
                model=self.model,
                messages=[
                    {"role": "system", "content": "when i say ping, you say pong"},
                    {"role": "user", "content": "ping"},
                ],
                timeout=(60 * 2),
            )

            result = response.choices[0].message.content
            return bool(result)
        except openai.APIError as error:
            self.io.output(f"Connection failed ({type(error).__name__}): {error}")
            return False

    def API_call(self, concept, document):
        """Asks the model if the concept appears in a document and returns the result."""
        concept_definition = concept["concept"]
        stance_label = concept["stance_label"]

        instructions = (
            "Determine whether the following concept appears in the document. "
            "The stance label (Yes/No) in front of the concept tells you whether "
            "the concept promotes or opposes the climate law. "
            "If it does, give the passage from the document that expresses it, "
            "quoted exactly as written, without markdown or ellipses. "
            "The passage may endorse or reject the argument. "
            "Set agreement to true if the author endorses the argument, "
            "and false if the author rejects it. "
            "If the concept is not found, set present to false, passage to null, "
            "and agreement to null. "
            'Do not answer "yes" unless you can provide a supporting passage.\n'
            f"Concept: {stance_label}: {concept_definition}"
        )

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

    def create_evaluation_run(self):
        """Creates a new evaluation run in the database and returns the run ID."""
        prompt = "TEMPORARY PROMPT"
        run_id = asyncio.run(create_evaluation_run(self.model, prompt))
        return run_id
        

    def call_aitta(self, run_id, on_result=None):
        """Analyzes each concept in the selected document and returns results and failures."""
        document = self.documents["content"]
        document_id = self.documents["id"]

        for concept in self.concepts:
            try:
                api_call_result = self.API_call(concept, document)
            except (openai.APIError, ValidationError) as e:
                self.failed_api_calls.append((run_id, concept, document))
                self.io.output(f"Konseptin {concept['id']} käsittely epäonnistui:")
                self.io.output(json.dumps(f"{e}", indent=4, ensure_ascii=False))
                continue

            result = {
                "run_id": run_id,
                "document_id": document_id,
                "concept_id": concept["id"],
                "concept": concept["concept"],
                "present": api_call_result.present,
                "passage": api_call_result.passage if api_call_result.present else None,
                "agreement": api_call_result.agreement,
            }

            self.session_list.append(result)

            if on_result is not None:
                on_result(result)

        self.output_to_db()

        return self.session_list, self.failed_api_calls

    def completed_all(self):
        """Returns True if all API calls were successful, False otherwise."""
        if self.failed_api_calls == []:
            return True
        else:
            return False

    def output_to_db(self):
        """Saves LLM output to the database."""
        asyncio.run(save_output(self.session_list))
        asyncio.run(save_evaluation_run(run_id=self.session_list[0]["run_id"], repetitions=1, completed_all=self.completed_all()))
