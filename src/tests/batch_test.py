import unittest
from unittest.mock import patch

from batch import BatchManager


class TestBatchManager(unittest.TestCase):
    @patch("batch.LlmManager")
    def test_batch_call_passes_single_document_and_concept(self, llm_manager):
        documents = [{"id": 1, "content": "first"}, {"id": 2, "content": "second"}]
        concepts = [
            {"id": 10, "concept": "first concept"},
            {"id": 20, "concept": "second concept"},
        ]
        model = "test-model"

        llm_manager.return_value.call_aitta.return_value = ["result"]

        result = BatchManager(documents, concepts, model).batch_call()

        self.assertEqual([["result"]] * 4, result)
        self.assertEqual(
            [
                unittest.mock.call([document], [concept], model)
                for document in documents
                for concept in concepts
            ],
            llm_manager.call_args_list,
        )
        self.assertEqual(4, llm_manager.return_value.call_aitta.call_count)


if __name__ == "__main__":
    unittest.main()
