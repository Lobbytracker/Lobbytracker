import asyncio
import asyncpg

from db.db_calls import add_prompt
from ai.ai import LlmManager, get_available_models
from ai.batch import BatchManager
from config import DEFAULT_MODEL, MIN_PROMPT_LENGTH
from error_handling import BackToMenu


class App:
    """Coordinates the application's menu actions and services."""

    def __init__(self, tui, documents, concepts, golden_standards, runs):
        self.tui = tui
        self.documents = documents
        self.concepts = concepts
        self.golden_standards = golden_standards
        self.runs = runs
        self.selected_model = DEFAULT_MODEL

    def print_instructions(self):
        """Displays the command menu."""
        self.tui.print_instructions(self.selected_model)

    def search_from_file(self):
        """Search selected documents using selected concepts."""
        document_ids = self.tui.ask_document_ids(self.documents.all_documents, limit=1)
        if document_ids is None:
            return None

        selected_documents = self.documents.get_by_ids(document_ids)
        concept_ids = self.tui.ask_concept_ids(self.concepts.all_concepts)

        if concept_ids is None:
            return None

        selected_concepts = self.concepts.select_concepts(concept_ids)
        self.tui.print_cancel_hint()
        manager = LlmManager(
            selected_documents[0], selected_concepts, model=self.selected_model
        )
        run_id = manager.create_evaluation_run()
        completed_all = False

        try:
            results, failures = manager.call_aitta(
                run_id, on_result=self.tui.print_output
            )

            completed_all = manager.completed_all()

        finally:
            manager.finish_evaluation_run(run_id, completed_all)

        self.calculate_f1(run_id)
        return results, failures

    def prompt_thing(self):
        """Runs a test analysis on the first document and two concepts."""
        self.tui.print_cancel_hint()
        documents = self.documents.all_documents[
            0
        ]  # limit to first document for testing
        concepts = self.concepts.all_concepts[
            0:2
        ]  # limit to first two concepts for testing

        manager = LlmManager(documents, concepts, model=self.selected_model)
        run_id = manager.create_evaluation_run()
        completed_all = False

        try:
            results, failures = manager.call_aitta(
                run_id, on_result=self.tui.print_output
            )

            completed_all = manager.completed_all()

        finally:
            manager.finish_evaluation_run(run_id, completed_all)

        self.calculate_f1(run_id)
        return results, failures

    def add_prompt(self):
        """Lets the user add a new prompt."""
        while True:
            input_prompt = self.tui.ask("Kirjoita uusi prompti: ").strip()

            if not any(char.isalpha() for char in input_prompt):
                self.tui.io.output(
                    "Promptin täytyy sisältää tekstiä, ei pelkkiä numeroita tai välilyöntejä."
                )
                continue

            if len(input_prompt) < MIN_PROMPT_LENGTH:
                self.tui.io.output(
                    f"Promptin täytyy olla vähintään {MIN_PROMPT_LENGTH} merkkiä pitkä."
                )
                continue

            try:
                prompt_id = asyncio.run(add_prompt(input_prompt))
            except asyncpg.exceptions.UniqueViolationError:
                self.tui.io.output("Tämä prompti on jo olemassa.")
                continue

            self.tui.io.output(f"Prompti lisätty (id {prompt_id}).")
            return

    def change_model(self):
        """Lets the user choose and test an available AI model."""
        try:
            models = get_available_models()
        except (ConnectionError, TimeoutError, OSError) as error:
            self.tui.io.output(f"Mallien hakeminen epäonnistui: {error}")
            return

        if not models:
            self.tui.io.output("Aitta ei palauttanut yhtään mallia.")
            return

        if self.selected_model not in models:
            self.tui.io.output(
                f"Nykyinen malli ei ole Aittan katalogissa: {self.selected_model}"
            )

        self.tui.print_available_models(models, self.selected_model)

        try:
            choice = int(self.tui.ask("Valitse mallin numero: "))
            connect = LlmManager(None, None, models[choice - 1]).create_connection()
            if not connect:
                self.tui.io.output("Valittuun malliin ei saatu yhteyttä.")
            else:
                self.selected_model = models[choice - 1]
                self.tui.io.output(f"Käytettävä malli: {self.selected_model}")
        except (ValueError, IndexError):
            self.tui.io.output("Virheellinen valinta.")
            return

    def print_golden_standard(self):
        """Displays golden standard records for selected documents."""
        document_ids = self.tui.ask_golden_standards_for_documents(
            self.golden_standards.all_golden_standards
        )

        if document_ids is None:
            return

        golden_standards = [
            self.golden_standards.get_by_document_id(id) for id in document_ids
        ]

        self.tui.print_golden_standard(golden_standards)

    def print_runs(self):
        """Displays evaluation runs."""
        runs = self.runs.get_preview_info()
        run_ids = self.tui.ask_run_ids(runs)
        if run_ids is not None:
            for run_id in run_ids.split(","):
                self.calculate_f1(int(run_id))

    def compare_runs(self):
        """Displays the evaluation run summaries."""
        runs = self.runs.get_preview_info()
        run_ids = self.tui.ask_run_ids(runs)
        if run_ids is not None:
            summary_info = self.runs.get_summary_info(run_ids)
            self.tui.print_run_summary(summary_info)

    def call_batch(self):
        """Calls the BatchManager to process documents and concepts in batch mode."""
        documents = self.documents.all_documents
        document_ids = self.tui.ask_document_ids(documents, limit=None)
        selected_documents = self.documents.get_by_ids(document_ids)
        concepts = self.concepts.all_concepts
        self.tui.print_cancel_hint()
        batch_manager = BatchManager(
            self.tui, selected_documents, concepts, self.selected_model
        )
        run_id, results, failures = batch_manager.batch_call()
        self.tui.print_batch_summary(len(results), len(failures), failures)
        self.calculate_f1(run_id)

    def calculate_f1(self, run_id=None):
        """Calculates the F1 score for the given evaluation run."""
        run_output = asyncio.run(self.runs.run_has_output(run_id))
        if run_output:
            self.tui.calculate_f1_score(run_id)
        else:
            self.tui.io.output(f"Ajolla {run_id} ei ole tuloksia.")

    def main(self):
        """Runs the application command loop."""
        commands = {
            1: self.search_from_file,
            2: self.add_prompt,
            3: self.prompt_thing,
            4: self.change_model,
            5: self.print_golden_standard,
            6: self.call_batch,
            7: self.print_runs,
            8: self.compare_runs,
        }

        while True:
            self.print_instructions()
            try:
                command = int(input("\nAnna komento: "))
            except ValueError:
                print("Väärä syöte. Syötä vain jokin komentonumero.")
                continue
            if command == 0:
                break
            if command not in commands:
                print("Tuntematon komento, syötä jokin ohjelman komennoista.")
                continue
            executable = commands[command]
            try:
                if asyncio.iscoroutinefunction(executable):
                    asyncio.run(executable())
                else:
                    executable()
            except BackToMenu as e:
                self.tui.handle_error(e)
            except KeyboardInterrupt:
                self.tui.io.output("Operation cancelled.")
