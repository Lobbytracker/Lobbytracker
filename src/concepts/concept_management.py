import db
import asyncio

class ConceptManager:
    """Class for managing concept infromations.
    """

    def __init__(self, all_concepts=None):
        if not all_concepts:
            self.all_concepts = self.get_all_from_db()
        else:
            self.all_concepts = all_concepts

    def get_all_from_db(self): # pitääkö olla async?
        """Returns all concepts from the database.
        """
        return (asyncio.run(db.get_concepts()))

    def select_concepts(self, concept_ids: str):
        """Gets all concepts with the given ids.
        """

        selected_ids = [int(value.strip()) for value in concept_ids.split(",")]

        selected_concepts = [concept for concept in self.all_concepts if concept["id"] in selected_ids]

        return selected_concepts

    def get_all_ids(self):
        """Returns the ids of all concepts as a set.
        """
        return {concept["id"] for concept in self.all_concepts}