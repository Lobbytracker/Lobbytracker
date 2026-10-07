from golden_standard import golden_standards_from_file

class ConceptComparing:
    def __init__(self):
        self.golden_standard = golden_standards_from_file() # 4,19,23,17,6,9  <- noi löytyy ekasta tiedostosta golden standardin mukaan
        # for i in self.golden_standard:
        #     print(i, end="\n\n")

    def compare_concept(self,concept):
        for i in self.golden_standard:
            if concept["concept_id"] == i["concept_id"] and concept["decision"] == i["decision"]:
                return True
        return False
            
    def compare_many(self, concepts):
        answer = {
            "found": 0,
            "matches": []
        }

        for concept in concepts:
            if self.compare_concept(concept):
                answer["found"] += 1
                answer["matches"].append(concept)

        return answer


