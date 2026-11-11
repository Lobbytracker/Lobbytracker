import unittest
from tui.tui import Tui
from rich.table import Table
from rich.text import Text
from rich.console import Console


class IoStub:
    def __init__(self):
        self.inputs = []
        self.outputs = []
        self.console = Console()

    def input(self, text):
        self.inputs.append(text)

    def output(self, item, style=None, markup=False, highlight=False):
        with self.console.capture() as capture:
            self.console.print(item, style=style, markup=markup, highlight=highlight)
        self.outputs.append(capture.get())


class TestTui(unittest.TestCase):
    def setUp(self):
        self.io = IoStub()
        self.tui = Tui(io=self.io)
        self.console = Console()

    def test_print_instructions(self):
        instructions = {
            0: "Quit",
            1: "Etsi valitut konseptit tiedostosta",
            2: "Aitta prompti",
            3: "Vaihda tekoälymallia",
            4: "Tulosta golden standard tiedostoille",
            5: "Suorita batch-prosessointi",
            6: "Laske F1-arvo viimeisimmälle ajolle",
            7: "Encoding test",
        }
        self.tui.print_instructions(selected_model="testmodel")

        correct = []

        correct_table = Table(
            title="Lobbytracker", show_header=True, header_style="bold magenta"
        )
        correct_table.add_column("Komento", style="dim", justify="right")
        correct_table.add_column("Toiminto")

        for key, val in instructions.items():
            correct_table.add_row(str(key), Text(val))

        with self.console.capture() as capture:
            self.console.print(
                f"\nNykyinen tekoälymalli: [bold green]testmodel[/bold green]\n",
                markup=True,
            )
        correct.append(capture.get())

        with self.console.capture() as capture:
            self.console.print(correct_table)
        correct.append(capture.get())

        self.assertEqual(correct, self.io.outputs)

    def test_format_document_name(self):
        name = "testname.txt"
        formated = self.tui.format_document_name(name)
        self.assertEqual("testname", formated)
