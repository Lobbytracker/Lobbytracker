import asyncio

import db.db_calls as db


class DataEncoding:
    """Encodes the given LLM outputs and goldenstandard."""

    def __init__(self, run_id=None, llm_output=None, goldenstandard=None):
        if llm_output is None and goldenstandard is None:
            self.llm_output, self.goldenstandard = asyncio.run(self._load_pairs(run_id))
        else:
            self.llm_output, self.goldenstandard = (
                self.remove_duplicates(llm_output),
                self.remove_duplicates(goldenstandard),
            )

    async def _load_pairs(self, run_id=None):
        """Fetches (document_id, concept_id) pairs for the given run and
        the matching golden standard pairs."""
        try:
            if run_id is None:
                result = await db.get_latest_run_id()
                run_id = result[0]["max"]
            else:
                try:
                    run_id = int(run_id)
                except (TypeError, ValueError) as exc:
                    raise ValueError(f"Invalid run id: {run_id}") from exc
                result = await db.get_run_by_id(run_id)
                if result is None:
                    raise ValueError(f"Run id not found: {run_id}")
        except (TypeError, ValueError, KeyError, IndexError) as e:
            print(f"Error occurred while fetching run: {e}")
            return [], []

        llm_pairs = await db.retrieve_document_concept_pair(run_id)
        golden_pairs = []
        for document_id in {doc for doc, _, _ in llm_pairs}:
            rows = await db.get_golden_standard_by_document_id(document_id)
            golden_pairs += [(row["document_id"], row["concept_id"]) for row in rows]

        return llm_pairs, golden_pairs

    def remove_duplicates(self, llm_pairs):
        """Removes duplicate pairs from a list."""
        return list(dict.fromkeys(llm_pairs))  # set maybe instead?

    def encode_data(self):
        """Encodes the given llm output and goldenstandard data.
        Returns (document,concept) pairs, coded LLM output and coded goldenstandard."""
        encoded_output = []
        encoded_goldenstandard = []
        pair = []

        llm_output = list(self.llm_output)
        goldenstandard = list(self.goldenstandard)

        for first in llm_output:  # true positives and false positives
            pair.append(first)
            document_id, concept_id, present = first

            if present:
                encoded_output.append(1)
            else:
                encoded_output.append(0)

            if (document_id, concept_id) in goldenstandard:
                encoded_goldenstandard.append(1)
            else:
                encoded_goldenstandard.append(0)

        return (pair, encoded_output, encoded_goldenstandard)
