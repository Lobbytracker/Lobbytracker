import unittest
from unittest.mock import patch
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

    def test_format_document_name(self):
        name = "testname.txt"
        formated = self.tui.format_document_name(name)
        self.assertEqual("testname", formated)

    def test_print_failed_batch_summary(self):
        self.tui.print_failed_batch_summary([(1, 2), (3, 4)])

        self.assertEqual(1, len(self.io.outputs))
        output = " ".join(self.io.outputs[0].split())
        self.assertIn("(tiedosto ID, konsepti ID): [(1, 2), (3, 4)]", output)
