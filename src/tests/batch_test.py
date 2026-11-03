import unittest
from unittest.mock import patch

import populate_test_data
from ai.batch import BatchManager


class TestBatchManager(unittest.TestCase):
    @patch("ai.batch.LlmManager")
    def test_batch_call_passes_one_document_and_concept(self, llm_manager):
        document = populate_test_data.populate_documents_test_data()[
            :1
        ]  # select the first document
        concept = populate_test_data.populate_concepts_test_data()[
            :1
        ]  # select the first concept
        model = "test-model"

        llm_manager.return_value.call_aitta.return_value = ["result"]

        result = BatchManager(document, concept, model).batch_call()

        self.assertEqual(result, [["result"]])

    def test_batch_call_passes_multiple_documents_and_concepts(self):
        documents = populate_test_data.populate_documents_test_data()[:2]
        concepts = populate_test_data.populate_concepts_test_data()[:2]
        model = "test-model"

        with patch("ai.batch.LlmManager") as llm_manager:
            llm_manager.return_value.call_aitta.return_value = ["result"]

            result = BatchManager(documents, concepts, model).batch_call()

            self.assertEqual(result, [["result"], ["result"], ["result"], ["result"]])


if __name__ == "__main__":
    unittest.main()
