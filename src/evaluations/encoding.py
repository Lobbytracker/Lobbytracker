class DataEncoding:
    """Encodes the given LLM outputs and goldenstandard."""

    def __init__(self, llm_output, goldenstandard):
        self.llm_output = self.remove_duplicates(llm_output)
        self.goldenstandard = self.remove_duplicates(goldenstandard)

    def remove_duplicates(self, pairs):
        """Removes duplicate pairs from a list."""
        pairs = list(set(pairs))
        return pairs

    def encode_data(self, llm_output, golden_standart):
        """Encodes the given llm output and goldenstandard data.
        Returns (document,concept) pairs, coded LLM output and coded goldenstandard."""
        encoded_output = []
        encoded_goldestandard = []
        pair = []

        while len(llm_output) > 0: # Finds true positives and false positives
            first = llm_output.pop(0)
            encoded_output.append(1)
            pair.append(first)
            if first in golden_standart:
                encoded_goldestandard.append(1) 
                golden_standart.remove(first)
            else:
                encoded_goldestandard.append(0)

        if len(golden_standart) > 0: # Finds false negatives
            encoded_output += len(golden_standart)*[0]
            encoded_goldestandard += len(golden_standart)*[1]
            pair += golden_standart

        return (pair, encoded_output, encoded_goldestandard)
