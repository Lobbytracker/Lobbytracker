import unittest

import populate_test_data
from concepts.concept_management import ConceptManager


class TestConceptManager(unittest.TestCase):
    def setUp(self):
        self.concepts = populate_test_data.populate_concepts_test_data()
        self.manager = ConceptManager(all_concepts=self.concepts)

    def test_select_one_concepts(self):
        selected = self.manager.select_concepts("2")
        self.assertEqual([self.concepts[1]], selected)

    def test_select_many_concepts(self):
        selected = self.manager.select_concepts("1,3")
        self.assertEqual([self.concepts[0], self.concepts[2]], selected)

    def test_get_all_ids(self):
        selected = self.manager.get_all_ids()
        self.assertEqual({1, 2, 3, 4, 5, 6, 7}, selected)
