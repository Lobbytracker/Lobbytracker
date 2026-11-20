import asyncio
import json
import os
from urllib.request import Request, urlopen

import openai
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError

from config import (
    AITTA_URL,
    DEFAULT_MODEL,
    MAX_API_CALL_ATTEMPTS,
    REQUEST_TIMEOUT_SECONDS,
)
from db.db_calls import create_evaluation_run, save_evaluation_run, save_output
from tui.tui_io import TuiIO


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


class LlmManager:  # pylint: disable=too-many-instance-attributes
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

    def build_system_prompt(self, concept=None):
        """Returns prompt body for eval run and prompt+concept for system message"""
        prompt_body = (
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
            'Do not answer "yes" unless you can provide a supporting passage.'
        )

        if concept is None:
            return prompt_body

        return (
            f"{prompt_body}\nConcept: {concept['stance_label']}: {concept['concept']}"
        )

    def api_call(self, concept, document):
        """Asks the model if the concept appears in a document and returns the result."""
        response = self.client.beta.chat.completions.parse(
            messages=[
                {"role": "system", "content": self.build_system_prompt(concept)},
                {"role": "user", "content": document},
            ],
            model=self.model,
            response_format=ConceptResult,
        )

        result = response.choices[0].message.parsed

        return result

    def create_evaluation_run(self):
        """Creates a new evaluation run in the database and returns the run ID."""
        prompt = self.build_system_prompt()
        run_id = asyncio.run(create_evaluation_run(self.model, prompt))
        return run_id

    def finish_evaluation_run(self, run_id, completed_all):
        """Save the final state of the evaluation run"""
        asyncio.run(
            save_evaluation_run(
                run_id=run_id,
                repetitions=1,
                completed_all=completed_all,
            )
        )

    def call_aitta(self, run_id, on_result=None):
        """Analyzes each concept in the selected document and returns results and failures."""
        document = self.documents["content"]
        document_id = self.documents["id"]
        for concept in self.concepts:
            api_call_result = None
            for attempt in range(MAX_API_CALL_ATTEMPTS):
                print(f"Processing concept {concept['id']} (attempt {attempt + 1})...")
                try:
                    api_call_result = self.api_call(concept, document)
                    break
                except (openai.APIError, ValidationError) as e:
                    self.io.output(
                        f"Concept {concept['id']} attempt {attempt + 1} failed: {e}"
                    )
            failed = api_call_result is None
            result = {
                "run_id": run_id,
                "document_id": document_id,
                "concept_id": concept["id"],
                "concept": concept["concept"],
                "status": "failed" if failed else "passed",
                "present": None if failed else api_call_result.present,
                "passage": (
                    None if failed or not api_call_result.present
                    else api_call_result.passage
                ),
                "agreement": None if failed else api_call_result.agreement,
            }
            self.output_to_db(result)  # saved for both passed and failed
            if failed:
                self.failed_api_calls.append((run_id, concept, document))
                continue
            self.session_list.append(result)
            if on_result is not None:
                on_result(result)
        return self.session_list, self.failed_api_calls

    def completed_all(self):
        """Returns True if all API calls were successful, False otherwise."""
        return not self.failed_api_calls

    def output_to_db(self, result):
        """Saves LLM output to the database."""
        asyncio.run(save_output([result]))
