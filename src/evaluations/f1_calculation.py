from sklearn.metrics import precision_recall_fscore_support
import db

from encoding import DataEncoding


class F1Calculator:
    def __init__(self, golden_standard, llm_output):
        self.golden_standard = golden_standard
        self.llm_output = llm_output

    def encode_data(self):
        pass

    def calculate_f1(self):
        pass

    def calculate_precision(self):
        pass

    def calculate_recall(self):
        pass
