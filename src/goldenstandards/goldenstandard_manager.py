import asyncio

import db


class GoldenStandardManager:
    """Loads and prepares golden-standard annotations for documents."""

    def __init__(self):
        pass

    def get_by_document_id(self, document_id):
        rows = asyncio.run(db.get_golden_standard_by_document_id(document_id))
        concepts_by_id = {}
        for row in rows:
            concepts = asyncio.run(db.get_concepts_by_id(row["concept_id"]))
            for concept in concepts:
                concepts_by_id[concept["id"]] = concept["concept"]

        return [
            {
                "document_id": row["document_id"],
                "concept_id": row["concept_id"],
                "concept": concepts_by_id[row["concept_id"]],
                "content": row["content"],
                "agreement": row["agreement"],
            }
            for row in rows
        ]
