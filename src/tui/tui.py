from rich import box
from rich.json import JSON
from rich.table import Table
from rich.text import Text

from concepts.concept_management import ConceptManager
from documents.document_management import DocumentManager
from goldenstandards.goldenstandard_manager import GoldenStandardManager
from tui.tui_io import TuiIO


class Tui:
    """Class for managing the text user interface."""

    def __init__(self, io=TuiIO):
        self.io = io
        self.documents = DocumentManager()
        self.concepts = ConceptManager()
        self.golden_standard = GoldenStandardManager()

    def print_instructions(self, selected_model: str):
        instructions = {
            0: "Quit",
            1: "Etsi valitut konseptit tiedostosta",
            2: "Aitta prompti",
            3: "Vaihda tekoälymallia",
            4: "Tulosta golden standard tiedostoille",
        }

        self.io.output(
            f"\nNykyinen tekoälymalli: [bold green]{selected_model}[/bold green]\n",
            markup=True,
        )

        table = Table(
            title="Lobbytracker", show_header=True, header_style="bold magenta"
        )
        table.add_column("Komento", style="dim", justify="right")
        table.add_column("Toiminto")

        for key, val in instructions.items():
            table.add_row(str(key), Text(val))

        self.io.output(table)

    def print_documents(self, start: int = 0):
        """Prints the 10 first documents"""
        files = self.documents.all[start : start + 10]

        table = Table(
            title=f"\nDokumentit {start + 1}-{start + len(files)}:",
            box=box.SIMPLE,
            header_style="bold cyan",
        )
        table.add_column("Dokumentin ID", style="dim", justify="right")
        table.add_column("Nimi")

        for document in files:
            name = self.documents.format(document["filename"])
            table.add_row(str(document["id"]), name)

        self.io.output(table)

        return start + 10 < len(self.documents.all)

    def print_concepts(self):
        """Prints all concepts"""
        table = Table(title="\nKonseptit:", box=box.SIMPLE, header_style="bold blue")
        table.add_column("Konseptin ID", style="dim", justify="right")
        table.add_column("Konsepti")

        for concept in self.concepts.all_concepts:
            table.add_row(str(concept["id"]), concept["concept"])

        self.io.output(table)

    def print_golden_standard(self, standards: list):
        """Prints golden standards for given files
        TODO: virheenhallinta
        """
        table = Table(
            title="\nTiedostojen Golden Standard:",
            box=box.SIMPLE,
            header_style="bold blue",
        )
        table.add_column("Konseptin ID", style="dim", justify="right")
        table.add_column("Konsepti")

        for document in standards:
            table.add_section()
            table.add_row(
                "",
                Text(
                    (f"Document ID: {document[0]['document_id']!s}"), style="bold cyan"
                ),
            )
            table.add_section()

            for standard in document:
                table.add_row(str(standard["concept_id"]), standard["concept"])

        self.io.output(table)

    def print_available_models(self, models: list, selected_model: str):
        """Prints the available models in a table."""
        table = Table(
            title="\nSaatavilla olevat mallit:",
            box=box.SIMPLE,
            header_style="bold yellow",
        )
        table.add_column("Mallin ID", style="dim", justify="right")
        table.add_column("Mallin nimi")

        for index, model in enumerate(models, start=1):
            if model == selected_model:
                table.add_row(
                    str(index), Text(model + " (käytössä)", style="bold green")
                )
            else:
                table.add_row(str(index), Text(model))

        self.io.output(table)

    def get_document_by_ids(self):
        """Asks user for document ids and returns the documents"""

        start = 0
        while True:
            documents = self.documents.get_next_ten_docs(start)
            self.print_documents(start)
            if len(documents) >= 10:
                prompt = "\nAnna tiedoston ID numerot (esim. 1, 2, 3), tai kirjoita x nähdäksesi seuraavat 10 tiedostoa: "
            else:
                prompt = "\nAnna tiedoston ID numerot (esim. 1, 2, 3): "

            answer = self.io.input(prompt).strip().lower()

            if answer == "x":
                if len(documents) >= 10:
                    start += 10
                else:
                    self.io.output("Ei enempää tiedostoja.")
                continue

            try:
                ids = [int(part) for part in answer.split(",")]
            except ValueError:
                self.io.output(
                    "Väärä syöte. Anna ID-numerot pilkulla erotettuna tai x."
                )
                continue

            valid_ids = self.documents.get_all_ids()
            invalid = [i for i in ids if i not in valid_ids]
            if invalid:
                self.io.output(f"Tuntemattomat ID:t: {invalid}")
                continue
            return self.documents.get_by_ids(answer)

    def get_concepts_by_ids(self):
        """Asks user for concept ids and returns the concepts."""

        while True:
            concept_ids = self.io.input(
                "\nAnna konseptien ID numerot pilkulla erotettuna (esim. 1, 2, 3): "
            )

            try:
                ids = [int(part) for part in concept_ids.split(",")]
            except ValueError:
                self.io.output("Väärä syöte. Anna ID-numerot pilkulla erotettuna.")
                continue
            valid_ids = self.concepts.get_all_ids()
            invalid = [i for i in ids if i not in valid_ids]
            if invalid:
                self.io.output(f"Tuntemattomat ID:t: {invalid}")
                continue

            return self.concepts.select_concepts(concept_ids)

    def golden_standards_for_documents(self):
        """Prints golden standard concepts for the chosen documents"""
        document_ids = self.io.input(
            "\nAnna tiedoston ID numerot (esim. 1, 2, 3), tai kirjoita x nähdäksesi seuraavat 10 tiedostoa: "
        )
        document_ids = [int(id) for id in document_ids.split(",")]
        golden_standards = [
            self.golden_standard.get_by_document_id(id) for id in document_ids
        ]
        self.print_golden_standard(golden_standards)

    def print_output(self, output):
        self.io.output(
            JSON.from_data(output, indent=2, ensure_ascii=False, highlight=True)
        )
