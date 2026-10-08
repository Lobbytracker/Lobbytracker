import asyncio

from ai import DEFAULT_MODEL, LlmManager, get_available_models
from tui.tui import Tui


class App:
    INSTRUCTIONS = {
        0: "Quit",
        1: "Etsi valitut konseptit tiedostosta",
        2: "Aitta prompti",
        3: "Vaihda tekoälymallia"
    }

    def __init__(self):
        self.tui = Tui()
        self.selected_model = DEFAULT_MODEL

    def print_instructions(self):
        self.tui.io.output(f"\nNykyinen tekoälymalli: {self.selected_model}\n")

        for key, val in self.INSTRUCTIONS.items():
            print((f"{key}. {val}"))

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
            selected_documents, selected_concepts, model=self.selected_model)
        session_list = manager.call_aitta()
        self.tui.print_output(session_list)

        return session_list

    def prompt_thing(self):
        documents = self.tui.documents.all
        concepts = self.tui.concepts.all_concepts

        manager = LlmManager(documents, concepts, model=self.selected_model)
        session_list = manager.call_aitta()
        self.tui.print_output(session_list)

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
            self.tui.io.output(f"Nykyinen malli ei ole Aittan katalogissa: {self.selected_model}")

        self.tui.io.output("\nSaatavilla olevat mallit:")
        for index, model in enumerate(models, start=1):
            marker = " (käytössä)" if model == self.selected_model else ""
            self.tui.io.output(f"{index}. {model}{marker}")

        try:
            choice = int(input("Valitse mallin numero: "))
        except (ValueError, IndexError):
            self.tui.io.output("Virheellinen valinta.")
            return

        self.selected_model = models[choice - 1]
        self.tui.io.output(f"Käytettävä malli: {self.selected_model}")

    def main(self):
        commands = {
            1: self.search_from_file,
            2: self.prompt_thing,
            3: self.change_model
        }

        while True:
            self.print_instructions()
            command = int(input("\nAnna komento: "))
            if command == 0:
                break
            if command not in self.INSTRUCTIONS:
                continue
            else:
                executable = commands[command]
                if asyncio.iscoroutinefunction(executable):
                    asyncio.run(executable())
                else:
                    executable()

if __name__ == "__main__":
    App().main()
