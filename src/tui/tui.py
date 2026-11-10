from rich import box
from rich.json import JSON
from rich.table import Table
from rich.text import Text

from error_handling import BackToMenu
from tui.tui_io import TuiIO
from evaluations.f1_calculation import F1Calculator

BACK_TO_MENU_COMMANDS = {"b"}


class Tui:
    """Class for managing the text user interface."""

    def __init__(self, io=TuiIO):
        self.io = io

    def print_instructions(self, selected_model: str):
        """Display the application command menu."""
        instructions = {
            0: "Quit",
            1: "Etsi valitut konseptit tiedostosta",
            2: "Aitta prompti",
            3: "Vaihda tekoälymallia",
            4: "Tulosta golden standard tiedostoille",
            5: "Suorita batch-prosessointi",
            6: "F1 MVP",
            7: "Encoding test",
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

    def handle_error(self, error):
        """Prints an error message for the given error."""
        self.io.output(str(error))

    def ask(self, prompt: str):
        """Prompt for user input"""
        while True:
            try:
                self.print_go_back_hint()
                value = self.io.input(prompt)
            except KeyboardInterrupt:
                self.io.output("\nCtrl+C does not work here. Type b to go back.")
                continue
            if value.strip().lower() in BACK_TO_MENU_COMMANDS:
                raise BackToMenu
            return value

    def print_cancel_hint(self):
        """Print instruction for cancellation"""
        self.io.output(
            "To cancel, press [bold green]Ctrl+C, (on Windows, Ctrl+Break)[/bold green]",
            markup=True,
            style="dim",
        )

    def print_go_back_hint(self):
        """Print instruction for going back to menu."""
        self.io.output(
            "To get back to menu, press [bold green]b[/bold green]",
            markup=True,
            style="dim",
        )

    def format_document_name(self, filename: str):
        """Returns the given filename without the .txt -suffix."""

        name = filename.removesuffix(".txt")
        if "-" in name:
            name = name.split("-", 1)[1]
        return name

    def print_documents(self, documents, start: int = 0):
        """Prints the 10 first documents"""
        table = Table(
            title=f"\nDokumentit {start + 1}-{start + len(documents)}:",
            box=box.SIMPLE,
            header_style="bold cyan",
        )
        table.add_column("Dokumentin ID", style="dim", justify="right")
        table.add_column("Nimi")

        for document in documents:
            name = self.format_document_name(document["filename"])
            table.add_row(str(document["id"]), name)

        self.io.output(table)

    def print_concepts(self, concepts):
        """Prints all concepts"""
        table = Table(title="\nKonseptit:", box=box.SIMPLE, header_style="bold blue")
        table.add_column("Konseptin ID", style="dim", justify="right")
        table.add_column("Konsepti")

        for concept in concepts:
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

    def ask_document_ids(self, documents, limit=None):
        """Shows documents and returns the selected document id."""

        if not documents:
            self.io.output("Ei valittavia tiedostoja")
            return None

        valid_ids = {document["id"] for document in documents}
        start = 0

        while True:  
            document_id, start = self.show_next_documents(documents, start=start)
            if limit == 1:     
                try:
                    ids = [int(document_id)]
                except ValueError:
                    self.io.output("Väärä syöte. Anna yhden tiedoston ID tai x.")
                    continue

            if limit == None:
                try:    
                    ids = [int(part) for part in str(document_id).split(",")]
                except ValueError:
                    self.io.output("Väärä syöte. Anna ID-numerot pilkulla erotettuna.")
                    continue
            
            invalid = [i for i in ids if i not in valid_ids]
            if invalid:
                self.io.output(f"Tuntemattomat ID:t: {invalid}")
                continue

            return document_id

    def show_next_documents(self, documents, start=0, limit=None):
        """Prints the next 10 documents, returns the selected document id 
            and starting position for the next 10 documents"""
        while True:
            page = documents[start : start + 10]
            self.print_documents(page, start)


            if start + 10 < len(documents):
                if limit == 1:
                    prompt = "\nAnna tiedoston ID tai kirjoita x nähdäksesi seuraavat 10 tiedostoa: "
                if limit == None:
                    prompt = "\nAnna tiedostojen ID:t tai kirjoita x nähdäksesi seuraavat 10 tiedostoa: "
            else:
                if limit == 1:
                    prompt = "\nAnna tiedoston ID: "
                else:
                    prompt = "\nAnna tiedostojen ID:t: "

            document_id = self.ask(prompt).strip().lower()

            if document_id == "x":
                if start + 10 < len(documents):
                    start += 10
                else:
                    self.io.output("Ei enempää tiedostoja.")
            if document_id == "all":
                return ",".join({str(document["id"]) for document in documents}), start
            else:
                return document_id, start

    def ask_concept_ids(self, concepts):
        """Shows concepts and returns the concept ids."""

        if not concepts:
            self.io.output("Ei valittavia konsepteja")
            return None

        self.print_concepts(concepts)
        valid_ids = {concept["id"] for concept in concepts}

        while True:
            concept_ids = self.ask(
                "\nAnna konseptien ID numerot pilkulla erotettuna (esim. 1, 2, 3): "
            )

            try:
                ids = [int(part) for part in concept_ids.split(",")]
            except ValueError:
                self.io.output("Väärä syöte. Anna ID-numerot pilkulla erotettuna.")
                continue

            invalid = [i for i in ids if i not in valid_ids]
            if invalid:
                self.io.output(f"Tuntemattomat ID:t: {invalid}")
                continue

            return concept_ids

    def ask_golden_standards_for_documents(self, golden_standards):
        """Asks user which documents to search golden standards from"""

        if not golden_standards:
            self.io.output("Ei valittavia golden standardeja")
            return None

        while True:
            raw = self.ask("\nAnna tiedoston ID numerot (esim. 1, 2, 3): ")
            try:
                return [int(part) for part in raw.split(",")]
            except ValueError:
                self.io.output("Väärä syöte. Anna ID-numerot pilkulla erotettuna.")

    def print_output(self, output):
        """Print output as formatted JSON."""
        self.io.output(
            JSON.from_data(output, indent=2, ensure_ascii=False, highlight=True)
        )

    def calculate_f1_score(self):
        """Calsulates F1 score for the latest llm run."""
        f1_calculator = F1Calculator()
        self.io.output(f"F1 score (micro): {f1_calculator.calculate_f1_micro()}")
        self.io.output(f"F1 score (macro): {f1_calculator.calculate_f1_macro()}")
        self.io.output(f"Precision: {f1_calculator.calculate_precision()}")
        self.io.output(f"Recall: {f1_calculator.calculate_recall()}")

