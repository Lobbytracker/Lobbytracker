from config import DEFAULT_MODEL

from .ai import LlmManager


class BatchManager:  # pylint: disable=too-few-public-methods
    """Manages batch processing of documents and concepts using LlmManager."""

    def __init__(self, tui, documents, concepts, model=DEFAULT_MODEL):
        self.tui = tui  # for printing output in real-time
        self.documents = documents[:2]  # Limit for testing
        self.concepts = concepts  # Limit for testing
        self.model = model

    def batch_call(self):
        """Calls the LlmManager for each document and concept combination and returns the results."""
        batch_list = []
        failed_calls = []

        batch_run = LlmManager(None, self.concepts, self.model)
        run_id = batch_run.create_evaluation_run()
        completed_all = False

        try:
            for document in self.documents:
                document_run = LlmManager(document, self.concepts, self.model)

                results, failures = document_run.call_aitta(
                    run_id, on_result=self.tui.print_output
                )  # added tui.print_output to display results in real-time

                batch_list.extend(results)
                failed_calls.extend(failures)

            completed_all = not failed_calls

            return run_id, batch_list, failed_calls

        finally:
            batch_run.finish_evaluation_run(run_id, completed_all)
