import unittest

from documents.document_management import DocumentManager


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.documents = []

        for i in range(15):
            self.documents.append(
                {
                    "id": i,
                    "document_id": i + 10,
                    "fileName": f"file{i}.txt",
                    "author": "me",
                    "content": "hello this is a file.",
                }
            )

        self.manager = DocumentManager(all_documents=self.documents)

    def test_get_ten_docs(self):
        start = 2
        correct = self.documents[start : start + 10]
        self.assertEqual(correct, self.manager.get_next_ten_docs(start))

    def test_get_by_ids(self):
        correct = self.documents[2:5]
        ids = self.manager.get_by_ids("2,3,4")
        self.assertEqual(correct, ids)

    def test_get_all_ids(self):
        correct = {doc["id"] for doc in self.documents}
        self.assertEqual(correct, self.manager.get_all_ids())
