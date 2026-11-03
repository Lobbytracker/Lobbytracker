import unittest

from documents.document_management import DocumentManager
from populate_test_data import populate_documents_test_data


class TestDocumentManager(unittest.TestCase):
    def setUp(self):
        self.documents = populate_documents_test_data()

        self.manager = DocumentManager(all_documents=self.documents)

    def test_get_three_docs(self):
        start = 0
        correct = self.documents[start : start + 3]
        self.assertEqual(correct, self.manager.get_next_ten_docs(start))

    def test_get_by_ids(self):
        correct = self.documents[0:3]
        ids = self.manager.get_by_ids("1,2,3")
        self.assertEqual(correct, ids)

    def test_get_all_ids(self):
        correct = {doc["id"] for doc in self.documents}
        self.assertEqual(correct, self.manager.get_all_ids())
