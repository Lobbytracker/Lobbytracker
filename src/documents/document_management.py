import db
import asyncio

class DocumentManager:
    """Class for managing document infromation.
    """

    def __init__(self):
        self.all = asyncio.run(self.get_all_from_db())

    async def get_all_from_db(self): # pitääkö olla async?
        """Returns all documents from the database.
        """
        return (await db.get_documents())

    def format(self, filename: str):
        """Returns the given filename without the .txt -suffix.
        """

        name = filename.removesuffix(".txt")
        if "-" in name:
            name = name.split("-", 1)[1]
        return name

    def get_next_ten_docs(self, start):
        """Returns 10 documents starting from the given index.
        """

        if len(self.all[start:]) >= 10:
            end = start+10
        else:
            end = len(self.all)-start

        return (self.all[start:end])


    def get_by_ids(self, selected_ids: str):
        """Returns all documents that contain the given ids.
        """
        ids_to_list = [int(value.strip()) for value in str(selected_ids).split(",")]
        return [document for document in self.all if document["id"] in ids_to_list]