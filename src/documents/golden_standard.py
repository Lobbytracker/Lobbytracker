import pandas as pd
from concepts.concept_management import ConceptManager

def golden_standards_from_file():
    all = (ConceptManager().all_concepts)
    all = [(concept['id'], concept['concept']) for concept in all]
    
    with open("./src/documents/testi.csv", "r") as file:
        data = pd.read_csv(file)

    golden_standard = []
    for _, row in data.iterrows():
        concept_text = (row['concept'].split(":")[1])[1:]
        concept_id = [con_id for (con_id, con_text) in all if concept_text == con_text][0]

        new_concept = {
            "concept_id":concept_id,
            "concept": row['concept'],
            "decision": row['agreement'],
            "passage": row['coded_text']
        }
        golden_standard.append(new_concept)

    return golden_standard

all = golden_standards_from_file()

for i in all:
    for key, val in i.items():
        print(f"{key}: {val}")
    print()