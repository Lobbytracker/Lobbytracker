from .ai import DEFAULT_MODEL, LlmManager


class BatchManager:
    """Manages batch processing of documents and concepts using LlmManager."""

    def __init__(self, tui, documents, concepts, model=DEFAULT_MODEL):
        self.tui = tui  # for printing output in real-time
        self.documents = documents[0:2]  # Limit for testing
        self.concepts = concepts[0:2]  # Limit for testing
        self.model = model

    def batch_call(self):
        """Calls the LlmManager for each document and concept combination and returns the results."""
        batch_list = []
        batch_run = LlmManager(None, self.concepts, self.model)
        run_id = batch_run.create_evaluation_run()

        for document in self.documents:
            document_run = LlmManager(document, self.concepts, self.model)
            batch_list.extend(
                document_run.call_aitta(run_id, on_result=self.tui.print_output)
            )
            # added tui.print_output to display results in real-time

        return batch_list
