from app import App
from concepts.concept_management import ConceptManager
from documents.document_management import DocumentManager
from goldenstandards.goldenstandard_manager import GoldenStandardManager
from tui.tui import Tui
from tui.tui_io import BackToMenu


if __name__ == "__main__":
    app = App(
        tui=Tui(),
        back_to_menu = BackToMenu,
        documents=DocumentManager(),
        concepts=ConceptManager(),
        golden_standards=GoldenStandardManager(),
    )
    app.main()
