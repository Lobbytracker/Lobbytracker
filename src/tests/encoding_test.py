import unittest

from evaluations.encoding import DataEncoding


class TestEncoding(unittest.TestCase):
    def setUp(self):
        llm_output = [(1, 1), (1, 2), (2, 2)]
        golden_standard = [(1, 1), (2, 2), (3, 3)]

    def test_encoding_true_positives(self):
        llm_output = [(1, 1), (1, 2), (2, 2)]
        golden_standard = [(1, 1), (1, 2), (2, 2)]
        encoder = DataEncoding(llm_output, golden_standard)
        encoded_data = encoder.encode_data()
        self.assertEqual(encoded_data[0], [(1, 1), (1, 2), (2, 2)])
        self.assertEqual(encoded_data[1], [1, 1, 1])
        self.assertEqual(encoded_data[2], [1, 1, 1])

    def test_encoding_false_positives(self):
        llm_output = [(1, 4), (1, 2), (2, 2)]
        golden_standard = [(1, 1), (3, 3)]
        encoder = DataEncoding(llm_output, golden_standard)
        encoded_data = encoder.encode_data()
        self.assertEqual(encoded_data[0], [(1, 4), (1, 2), (2, 2), (1, 1), (3, 3)])
        self.assertEqual(encoded_data[1], [1, 1, 1, 0, 0])
        self.assertEqual(encoded_data[2], [0, 0, 0, 1, 1])

    def test_encoding_false_negatives(self):
        llm_output = [(1, 2), (2, 2)]
        golden_standard = [(1, 1), (3, 3), (6, 7)]
        encoder = DataEncoding(llm_output, golden_standard)
        encoded_data = encoder.encode_data()
        self.assertEqual(encoded_data[0], [(1, 2), (2, 2), (1, 1), (3, 3), (6, 7)])
        self.assertEqual(encoded_data[1], [1, 1, 0, 0, 0])
        self.assertEqual(encoded_data[2], [0, 0, 1, 1, 1])

    def test_encoding_mixed(self):
        llm_output = [(1, 2), (6, 9), (3, 3)]
        golden_standard = [(4, 20), (3, 3), (6, 7), (6, 9)]
        encoder = DataEncoding(llm_output, golden_standard)
        encoded_data = encoder.encode_data()
        self.assertEqual(encoded_data[0], [(1, 2), (6, 9), (3, 3), (4, 20), (6, 7)])
        self.assertEqual(encoded_data[1], [1, 1, 1, 0, 0])
        self.assertEqual(encoded_data[2], [0, 1, 1, 1, 1])

    def test_empty_llm_output(self):
        llm_output = []
        golden_standard = [(4, 20), (3, 3), (6, 7), (6, 9)]
        encoder = DataEncoding(llm_output, golden_standard)
        encoded_data = encoder.encode_data()
        self.assertEqual(encoded_data[0], [(4, 20), (3, 3), (6, 7), (6, 9)])
        self.assertEqual(encoded_data[1], [0, 0, 0, 0])
        self.assertEqual(encoded_data[2], [1, 1, 1, 1])

    def test_empty_golden_standard(self):
        llm_output = [(4, 20), (3, 3), (6, 7), (6, 9)]
        golden_standard = []
        encoder = DataEncoding(llm_output, golden_standard)
        encoded_data = encoder.encode_data()
        self.assertEqual(encoded_data[0], [(4, 20), (3, 3), (6, 7), (6, 9)])
        self.assertEqual(encoded_data[1], [1, 1, 1, 1])
        self.assertEqual(encoded_data[2], [0, 0, 0, 0])

    def test_duplicate_handling(self):
        llm_output = [(1, 1), (1, 2), (2, 2), (1, 1), (2, 2)]
        golden_standard = [(7, 7), (7, 7), (7, 7), (6, 1)]
        encoder = DataEncoding(llm_output, golden_standard)
        self.assertEqual(encoder.llm_output, [(1, 1), (1, 2), (2, 2)])
        self.assertEqual(encoder.goldenstandard, [(7, 7), (6, 1)])
