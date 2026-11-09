try:
    from .encoding import DataEncoding
except ImportError:
    from encoding import DataEncoding
from sklearn.metrics import f1_score, precision_score, recall_score


class F1Calculator:
    """Calculates F1 score, precision and recall for the given LLM output and goldenstandard."""

    def __init__(self, llm_output=None, golden_standard=None):
        if llm_output != None and golden_standard != None:
            encoded = self.encode_data(llm_output, golden_standard)
            self.llm_output = encoded[0]
            self.golden_standard = encoded[1]
        else:
            encoded = self.encode_data()
            self.llm_output, self.golden_standard = encoded[0], encoded[1]

    def encode_data(self,llm_output=None,  golden_standard=None):
        """Encodes the given llm output and goldenstandard data."""
        encoded_data = DataEncoding(llm_output, golden_standard).encode_data()
        encoded_llm = encoded_data[1]
        encoded_golden_standard = encoded_data[2]
        return encoded_llm, encoded_golden_standard

    def calculate_f1_micro(self):
        """Calculates the F1 score for the given LLM output and goldenstandard
        using micro averaging."""
        return f1_score(self.golden_standard, self.llm_output, average="micro")

    def calculate_f1_macro(self):
        """Calculates the F1 score for the given LLM output and goldenstandard
        using macro averaging."""
        return f1_score(self.golden_standard, self.llm_output, average="macro")

    def calculate_precision(self):
        """Calculates the precision for the given LLM output and goldenstandard."""
        return precision_score(self.golden_standard, self.llm_output, average="binary")

    def calculate_recall(self):
        """Calculates the recall for the given LLM output and goldenstandard."""
        return recall_score(self.golden_standard, self.llm_output, average="binary")

if __name__=="__main__":
    llm_output = [(1, 4), (1, 6), (1, 17), (1, 20), (1, 23), (1, 24)]
    golden_standard = [(1, 4), (1, 19), (1, 23), (1, 17), (1, 6), (1, 9)]
    calculator = F1Calculator(llm_output, golden_standard)
    print(calculator.calculate_f1_micro())
