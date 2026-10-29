import asyncio

from ai import DEFAULT_MODEL, LlmManager, get_available_models
from batch import BatchManager
from concepts.concept_management import ConceptManager
from documents.document_management import DocumentManager
from goldenstandards.goldenstandard_manager import GoldenStandardManager
from tui.tui import Tui


class App:
    def __init__(self, tui, documents, concepts, golden_standards):
        self.tui = tui
        self.documents = documents
        self.concepts = concepts
        self.golden_standards = golden_standards
        self.selected_model = DEFAULT_MODEL

    def print_instructions(self):
        self.tui.print_instructions(self.selected_model)

    def search_from_file(self):
        """Search selected documents using selected concepts."""
        document_ids = self.tui.ask_document_ids(self.documents.all_documents)
        if document_ids is None:
            return None

        selected_documents = self.documents.get_by_ids(document_ids)

        concept_ids = self.tui.ask_concept_ids(self.concepts.all_concepts)
        if concept_ids is None:
            return None

        selected_concepts = self.concepts.select_concepts(concept_ids)

        manager = LlmManager(
            selected_documents, selected_concepts, model=self.selected_model
        )
        session_list = manager.call_aitta(on_result=self.tui.print_output)

        return session_list

    def prompt_thing(self):
        documents = self.documents.all_documents
        concepts = self.concepts.all_concepts

        manager = LlmManager(documents, concepts, model=self.selected_model)
        session_list = manager.call_aitta(on_result=self.tui.print_output)

        return session_list

    def change_model(self):
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
            choice = int(input("Valitse mallin numero: "))
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
        document_ids = self.tui.ask_golden_standards_for_documents(
            self.golden_standards.all_golden_standards
        )

        golden_standards = [
            self.golden_standards.get_by_document_id(id) for id in document_ids
        ]

        self.tui.print_golden_standard(golden_standards)

    def call_batch(self):
        documents = self.documents.all_documents
        concepts = self.concepts.all_concepts
        batch_manager = BatchManager(documents, concepts, self.selected_model)
        result = batch_manager.batch_call()
        self.tui.print_output(result)

    def main(self):
        commands = {
            1: self.search_from_file,
            2: self.prompt_thing,
            3: self.change_model,
            4: self.print_golden_standard,
            5: self.call_batch,
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
            else:
                executable = commands[command]
                if asyncio.iscoroutinefunction(executable):
                    asyncio.run(executable())
                else:
                    executable()


if __name__ == "__main__":
    app = App(
        tui=Tui(),
        documents=DocumentManager(),
        concepts=ConceptManager(),
        golden_standards=GoldenStandardManager(),
    )

    app.main()
