from ai import LlmManager


class BatchManager:
    def __init__(self, documents, concepts, model=DEFAULT_MODEL):
        self.documents = documents[0:2]
        self.concepts = concepts[0:2]
        self.model = model
    
    def batch_call(self):
        batch_list = []
        for document in self.documents:
            for concept in self.concepts:
                batch_run = LlmManager(document, concept, DEFAULT_MODEL)
                batch_list.append(batch_run.call_aitta())
        return batch_list

