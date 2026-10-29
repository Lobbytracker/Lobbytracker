try:
    from .encoding import DataEncoding
except ImportError:
    from encoding import DataEncoding
from sklearn.metrics import f1_score, precision_score, recall_score


class F1Calculator:
    """Calculates F1 score, precision and recall for the given LLM output and goldenstandard."""

    def __init__(self, llm_output, golden_standard):
        self.llm_output = self.encode_data(llm_output, golden_standard)[0]
        self.golden_standard = self.encode_data(llm_output, golden_standard)[1]

    def encode_data(self, llm_output, golden_standard):
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


if __name__ == "__main__":
    from src.populate_test_data import populate_evaluations_test_data

    llm_output, golden_standard = populate_evaluations_test_data()
    f1_calculator = F1Calculator(llm_output, golden_standard)
    print("F1 score (micro):", f1_calculator.calculate_f1_micro())
    print("F1 score (macro):", f1_calculator.calculate_f1_macro())
    print("Precision:", f1_calculator.calculate_precision())
    print("Recall:", f1_calculator.calculate_recall())
