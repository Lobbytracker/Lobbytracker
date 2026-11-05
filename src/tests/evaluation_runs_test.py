import unittest

from populate_test_data import (
    populate_evaluation_runs_test_data,
    populate_llm_output_test_data,
)

class TestEvaluationRuns(unittest.TestCase):
    def setUp(self):
        self.evaluation_runs = populate_evaluation_runs_test_data()
        self.llm_output = populate_llm_output_test_data()

    def test_llm_output_belongs_to_defined_evaluation_run(self):
        run_ids = {run["id"] for run in self.evaluation_runs}

        for output in self.llm_output:
            self.assertIn(output["run_id"], run_ids)

    def test_evaluation_runs_have_required_fields(self):
        required_fields = {
            "id",
            "model",
            "prompt",
            "start_time",
            "end_time",
            "repetitions",
            "completed_all",
        }

        for run in self.evaluation_runs:
            self.assertTrue(required_fields.issubset(run.keys()))

    def test_llm_output_has_required_fields(self):
        required_fields = {
            "id",
            "run_id",
            "document_id",
            "concept_id",
            "present",
            "passage",
            "agreement",
        }

        for output in self.llm_output:
            self.assertTrue(required_fields.issubset(output.keys()))

    def test_llm_output_passage_agreement_consistency(self):
        for output in self.llm_output:
            if output["present"] is False:
                self.assertIsNone(output["passage"])
                self.assertIsNone(output["agreement"])

    def test_llm_output_passage_agreement_consistency_present(self):
        for output in self.llm_output:
            if output["present"] is True:
                self.assertIsNotNone(output["passage"])
                self.assertIsNotNone(output["agreement"])

    def test_evaluation_runs_have_unique_ids(self):
        run_ids = [run["id"] for run in self.evaluation_runs]
        self.assertEqual(len(run_ids), len(set(run_ids)))

    def test_llm_output_linked_to_run_id(self):
        run_ids = {run["id"] for run in self.evaluation_runs}

        for output in self.llm_output:
            self.assertIn(output["run_id"], run_ids)