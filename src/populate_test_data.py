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
