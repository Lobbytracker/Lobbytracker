from config import DEFAULT_MODEL, BATCH_MAX_RERUNS

from .ai import LlmManager


class BatchManager:  # pylint: disable=too-few-public-methods
    """Manages batch processing of documents and concepts using LlmManager."""

    def __init__(self, tui, documents, concepts, model=DEFAULT_MODEL):
        self.tui = tui
        self.documents = documents
        self.concepts = concepts
        self.model = model

    def batch_call(self):
        """Runs the batch, then reruns failed pairs up to BATCH_MAX_RERUNS times."""
        batch_list = []
        failed_pairs = []  # list of (document_id, concept_id)

        batch_run = LlmManager(None, self.concepts, self.model)
        run_id = batch_run.create_evaluation_run()
        completed_all = False

        try:
            for document in self.documents:
                manager = LlmManager(document, self.concepts, self.model)
                results, failures = manager.call_aitta(
                    run_id, on_result=self.tui.print_output
                )
                batch_list.extend(results)
                failed_pairs.extend(failures)

            self.tui.print_batch_summary(len(batch_list), len(failed_pairs))
            if failed_pairs:
                self.tui.print_failed_batch_summary(failed_pairs)

            for rerun in range(1, BATCH_MAX_RERUNS + 1):
                if not failed_pairs:
                    break
                self.tui.print_rerun_notice(rerun, BATCH_MAX_RERUNS, len(failed_pairs))
                results, failed_pairs = self._rerun_pairs(run_id, failed_pairs)
                batch_list.extend(results)
                self.tui.print_batch_summary(len(batch_list), len(failed_pairs))
                if failed_pairs:
                    self.tui.print_failed_batch_summary(failed_pairs)

            completed_all = not failed_pairs
            return run_id, batch_list, failed_pairs
        finally:
            batch_run.finish_evaluation_run(run_id, completed_all)

    def _rerun_pairs(self, run_id, pairs):
        """Reruns (document_id, concept_id) pairs; returns (results, still_failed)."""
        documents = {d["id"]: d for d in self.documents}
        concepts = {c["id"]: c for c in self.concepts}

        concepts_by_document = {}
        for document_id, concept_id in pairs:
            concepts_by_document.setdefault(document_id, []).append(concepts[concept_id])

        results, still_failed = [], []
        for document_id, document_concepts in concepts_by_document.items():
            manager = LlmManager(documents[document_id], document_concepts, self.model)
            new_results, failures = manager.call_aitta(
                run_id, on_result=self.tui.print_output
            )
            results.extend(new_results)
            still_failed.extend(failures)
        return results, still_failed
