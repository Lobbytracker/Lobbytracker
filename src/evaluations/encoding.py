class DataEncoding:
    """Encodes the given LLM outputs and goldenstandard."""

    def __init__(self, llm_output, goldenstandard):
        self.llm_output = self.remove_duplicates(llm_output)
        self.goldenstandard = self.remove_duplicates(goldenstandard)

    def remove_duplicates(self, pairs):
        """Removes duplicate pairs from a list."""
        return list(dict.fromkeys(pairs))

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
