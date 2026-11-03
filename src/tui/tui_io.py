from rich.console import Console

console = Console()

class BackToMenu(Exception):
    """Raised when the user wants to return to the main menu."""

class TuiIO:
    @staticmethod
    def input(message: str):
        return console.input(message)

    @staticmethod
    def output(message, style=None, markup=False, highlight=False):
        return console.print(message, style=style, markup=markup, highlight=highlight)
