import json

from tui.tui_io import TuiIO
from documents.document_management import DocumentManager
from concepts.concept_management import ConceptManager


class Tui:
    """Class for managing the text user interface.
    """

    def __init__(self, io=TuiIO):
        self.io = io
        self.documents = DocumentManager()
        self.concepts = ConceptManager()

    def print_documents(self, start: int = 0):
        """Prints the 10 first documents
        """
        files = self.documents.all[start : start + 10]
        self.io.output(f"\nDokumentit {start + 1}-{start + len(files)}:")

        for document in files:
            name = self.documents.format(document["filename"])
            self.io.output(f"ID: {document['id']}, Nimi: {name}")

        return start + 10 < len(self.documents.all)

    def print_concepts(self):
        """Prints all concepts
        """
        self.io.output("\nKonseptit:")
        for concept in self.concepts.all_concepts:
            self.io.output(f"ID: {concept['id']}, {concept['concept']}")

    def get_document_by_ids(self):
        """Asks user for document ids and returns the documents
        """
        
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
            return self.documents.get_by_ids(answer)

    def get_concepts_by_ids(self):
        """TODO: virheenhallinta
        """
        concept_ids = self.io.input("\nAnna konseptien ID numerot (esim. 1, 2, 3): ")
        return self.concepts.select_concepts(concept_ids)

    def print_output(self, output):
        self.io.output(json.dumps(output, indent=2, ensure_ascii=False))
