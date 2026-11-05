import unittest
from unittest.mock import Mock, patch

import populate_test_data
from ai.batch import BatchManager


class TestBatchManager(unittest.TestCase):
    def setUp(self):
        self.documents = populate_test_data.populate_documents_test_data()
        self.concepts = populate_test_data.populate_concepts_test_data()
        self.tui = Mock()
        self.manager = BatchManager(self.tui, self.documents, self.concepts)

    @patch("ai.batch.LlmManager")
    def test_batch_call_returns_results(self, llm_manager):
        llm_manager.return_value.create_evaluation_run.return_value = 1
        llm_manager.return_value.call_aitta.return_value = ["result"]

        result = self.manager.batch_call()

        self.assertEqual(["result", "result"], result)

    @patch("ai.batch.LlmManager")
    def test_batch_call_passes_evaluation_run_id(self, llm_manager):
        llm_manager.return_value.create_evaluation_run.return_value = 1
        llm_manager.return_value.call_aitta.return_value = []

        self.manager.batch_call()

        calls = llm_manager.return_value.call_aitta.call_args_list

        self.assertEqual(2, len(calls))
        self.assertEqual(1, calls[0].args[0])
        self.assertEqual(1, calls[1].args[0])

    @patch("ai.batch.LlmManager")
    def test_batch_call_processes_two_documents(self, llm_manager):
        llm_manager.return_value.create_evaluation_run.return_value = 1
        llm_manager.return_value.call_aitta.return_value = []

        self.manager.batch_call()

        calls = llm_manager.call_args_list

        self.assertEqual(3, len(calls))
        self.assertIsNone(calls[0].args[0])
        self.assertEqual(self.documents[0], calls[1].args[0])
        self.assertEqual(self.documents[1], calls[2].args[0])
        self.assertEqual(self.concepts, calls[1].args[1])
        self.assertEqual(self.concepts, calls[2].args[1])