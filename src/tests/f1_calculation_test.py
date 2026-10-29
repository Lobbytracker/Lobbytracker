import unittest

from evaluations.f1_calculation import F1Calculator


class TestF1Calculator(unittest.TestCase):
    def setUp(self):
        self.llm_output = [(1, 1), (1, 2), (2, 2)]
        self.golden_standard = [(1, 1), (2, 2), (3, 3)]
        self.calculator = F1Calculator(self.llm_output, self.golden_standard)

    def test_encode_data(self):
        encoded_llm = self.calculator.llm_output
        encoded_golden_standard = self.calculator.golden_standard
        self.assertEqual(encoded_llm, [1, 1, 1, 0])
        self.assertEqual(encoded_golden_standard, [1, 0, 1, 1])

    def test_calculate_f1_micro(self):
        tp = 2
        fp = 1 + 1
        fn = 1 + 1
        f1_correct = tp / (tp + 0.5 * (fp + fn))
        f1_micro = self.calculator.calculate_f1_micro()
        self.assertEqual(f1_correct, f1_micro)

    def test_calculate_f1_macro(self):
        f1_label_0 = 0 / (0 + 0.5 * (1 + 1))
        f1_label_1 = 2 / (2 + 0.5 * (1 + 1))

        f1_correct = (f1_label_0 + f1_label_1) / 2
        f1_macro = self.calculator.calculate_f1_macro()
        self.assertEqual(f1_correct, f1_macro)

    def test_calculate_precision(self):
        tp = 2
        fp = 1
        precision_correct = tp / (tp + fp)
        precision = self.calculator.calculate_precision()
        self.assertEqual(precision_correct, precision)

    def test_calculate_recall(self):
        tp = 2
        fn = 1
        recall_correct = tp / (tp + fn)
        recall = self.calculator.calculate_recall()
        self.assertEqual(recall_correct, recall)
