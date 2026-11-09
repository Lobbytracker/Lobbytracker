import asyncio

import db.db_calls as db

class DataEncoding:
    """Encodes the given LLM outputs and goldenstandard."""

    def __init__(self, llm_output=None, goldenstandard=None):
        self.llm_output = self.retrieve_llm_pairs() #if not llm_output else self.remove_duplicates(llm_output)
        self.goldenstandard = self.retrieve_golden_pairs(self.llm_output) # if not goldenstandard else self.remove_duplicates(goldenstandard)

    async def get_run_id(self):
        result = await db.get_latest_run_id()
        return result[0]["max"]

    async def get_pairs(self,run_id):
        pairs = await db.get_golden_standard_by_document_id(run_id)
        return pairs

    def retrieve_llm_pairs(self):
        """Retrieves llmOutput pairs by run_id"""
        run_id = self.get_run_id()
        llm_pairs = self.get_pairs(run_id)
        return llm_pairs

    def retrieve_golden_pairs(self, llm_pairs):
        """Retrieves goldenStandard pairs"""
        found = []
        golden_pairs = []
        for pair in llm_pairs:
            if pair[0] not in found:
                found.append(pair[0])
                golden_pair = asyncio.run(db.get_golden_standard_by_document_id(pair[0]))
                golden_pairs += [(item["doceumnet_id"], item["condept_id"]) for item in golden_pair]
        return golden_pairs

    def remove_duplicates(self, llm_pairs):
        """Removes duplicate pairs from a list."""
        return list(dict.fromkeys(llm_pairs))

    def encode_data(self):
        """Encodes the given llm output and goldenstandard data.
        Returns (document,concept) pairs, coded LLM output and coded goldenstandard."""
        encoded_output = []
        encoded_goldestandard = []
        pair = []

        while len(self.llm_output) > 0:  # Finds true positives and false positives
            first = self.llm_output.pop(0)
            encoded_output.append(1)
            pair.append(first)
            if first in self.goldenstandard:
                encoded_goldestandard.append(1)
                self.goldenstandard.remove(first)
            else:
                encoded_goldestandard.append(0)

        if len(self.goldenstandard) > 0:  # Finds false negatives
            encoded_output += len(self.goldenstandard) * [0]
            encoded_goldestandard += len(self.goldenstandard) * [1]
            pair += self.goldenstandard

        return (pair, encoded_output, encoded_goldestandard)
