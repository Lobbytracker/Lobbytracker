import asyncio

from ai import DEFAULT_MODEL, LlmManager, get_available_models
from tui.tui import Tui


class App:
    def __init__(self):
        self.tui = Tui()
        self.selected_model = DEFAULT_MODEL

    def print_instructions(self):
        self.tui.print_instructions(self.selected_model)

    def search_from_file(self):
        selected_documents = self.tui.get_document_by_ids()
        if not selected_documents:
            self.tui.io.output("Ei valittuja tiedostoja.")
            return

        self.tui.print_concepts()
        selected_concepts = self.tui.get_concepts_by_ids()
        if not selected_concepts:
            self.tui.io.output("Ei valittuja konsepteja.")
            return

        manager = LlmManager(
            selected_documents, selected_concepts, model=self.selected_model
        )
        session_list = manager.call_aitta(on_result=self.tui.print_output)

        return session_list

    def prompt_thing(self):
        documents = self.tui.documents.all
        concepts = self.tui.concepts.all_concepts

        manager = LlmManager(documents, concepts, model=self.selected_model)
        session_list = manager.call_aitta(on_result=self.tui.print_output)

        return session_list

    def change_model(self):
        try:
            models = get_available_models()
        except Exception as error:
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
        self.tui.golden_standards_for_documents()

    def main(self):
        commands = {
            1: self.search_from_file,
            2: self.prompt_thing,
            3: self.change_model,
            4: self.print_golden_standard,
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
    App().main()
