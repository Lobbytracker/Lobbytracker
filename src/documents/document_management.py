import asyncio

import db


class DocumentManager:
    """Class for managing document infromation."""

    def __init__(self, all_documents=None):
        if not all_documents:
            self.all_documents = asyncio.run(self.get_all_from_db())
        else:
            self.all_documents = all_documents

    async def get_all_from_db(self):  # pitääkö olla async?
        """Returns all documents from the database."""
        return await db.get_documents()

    def get_next_ten_docs(self, start):
        """Returns 10 documents starting from the given index."""

        if len(self.all_documents[start:]) >= 10:
            end = start + 10
        else:
            end = len(self.all_documents) - start

        return self.all_documents[start:end]

    def get_by_ids(self, selected_ids: str):
        """Returns all documents that contain the given ids."""
        ids_to_list = [int(value.strip()) for value in str(selected_ids).split(",")]
        return [
            document for document in self.all_documents if document["id"] in ids_to_list
        ]

    def get_all_ids(self):
        """Returns the ids of all documents as a set."""
        return {document["id"] for document in self.all_documents}
