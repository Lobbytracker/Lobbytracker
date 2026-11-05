class BackToMenu(Exception):
    """Raised when the user wants to return to the main menu."""

    def __init__(self):
        super().__init__("Returning to the main menu.")
