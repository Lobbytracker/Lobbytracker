import unittest
from concepts.concept_management import ConceptManager



class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.concepts = [
            {"id": 1,"stance_label": "Yes","concept": "This is a test"},
            {"id": 2,"stance_label": "No","concept": "This is a test nro 2"},
            {"id": 3,"stance_label": "Yes","concept": "This is another test"} 
        ]
        self.manager = ConceptManager(all_concepts=self.concepts)

    def test_select_one_concepts(self):
        selected = self.manager.select_concepts("2")
        self.assertEqual([self.concepts[1]], selected)

    def test_select_many_concepts(self):
        selected = self.manager.select_concepts("1,3")
        self.assertEqual([self.concepts[0], self.concepts[2]], selected)

    def test_get_all_ids(self):
        selected = self.manager.get_all_ids()
        self.assertEqual({1,2,3}, selected)
