def populate_evaluations_test_data():
    """Populates the evaluations test data."""
    llm_output = [
        (1, 1),
        (1, 2),
        (2, 1),
        (2, 2),
        (3, 1),
        (3, 2),
        (4, 1),
        (4, 2),
    ]
    golden_standard = [
        (1, 1),
        (6, 2),
        (2, 5),
        (67, 69),
        (3, 1),
        (21, 7),
        (6, 1),
        (8, 2),
        (6, 7),
        (6, 9),
    ]

    return llm_output, golden_standard


def populate_concepts_test_data():
    """Populates the concepts test data."""
    concepts = [
        {
            "id": 1,
            "stance_label": "YES",
            "concept": "Improving cat girls rights leads to a more sustainable future.",
        },
        {
            "id": 2,
            "stance_label": "NO",
            "concept": "Cat girls are a threat to the environment and should be banned.",
        },
        {
            "id": 3,
            "stance_label": "YES",
            "concept": "Cat girls are a valuable part of society and should be protected.",
        },
        {
            "id": 4,
            "stance_label": "NO",
            "concept": "Cat girls are a waste of resources and should be eliminated.",
        },
        {
            "id": 5,
            "stance_label": "NO",
            "concept": "Unaligned AI will destroy the society so there is no point in saving the environment.",
        },
        {
            "id": 6,
            "stance_label": "YES",
            "concept": "One Tung Tung Tung Sahur a day will lower emissions.",
        },
        {
            "id": 7,
            "stance_label": "YES",
            "concept": "Tralalero Tralala is a product of Climate Change and just the tip of the iceberg.",
        },
    ]
    return concepts


def populate_documents_test_data():
    """Populates the documents test data."""
    documents = [
        {
            "id": 1,
            "document_id": 11,
            "fileName": "file1.txt",
            "author": "Tung Tung Tung Sahur",
            "content": "With the rise of brainrot, it is important to consider the impact of AI on the environment. "
            "AI-generated slop is a valuable part of society and should be protected.",
        },
        {
            "id": 2,
            "document_id": 12,
            "fileName": "file2.txt",
            "author": "Tralalero Tralala",
            "content": "The rise of brainrot is a threat to the environment and should be banned. "
            "AI-generated slop is a waste of resources and should be eliminated.",
        },
        {
            "id": 3,
            "document_id": 13,
            "fileName": "file3.txt",
            "author": "Cat Girl Rights Activist",
            "content": "Cat girls are a valuable part of society and should be protected. "
            "They help to lower emissions and improve the environment.",
        },
    ]
    return documents
