from rich.console import Console

console = Console()


class TuiIO:
    """Provides console input and output for the TUI."""
    @staticmethod
    def input(message: str):
        """Prompt for input and return the user's response."""
        return console.input(message)

    @staticmethod
    def output(message, style=None, markup=False, highlight=False):
        """Print a message to the console with optional Rich formatting."""
        return console.print(message, style=style, markup=markup, highlight=highlight)
