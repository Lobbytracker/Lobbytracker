import asyncio
import os
from pathlib import Path

import asyncpg
import pandas as pd

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/lobbytracker",
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_REPO_PATH = Path(
    os.getenv("DATA_REPO_PATH", PROJECT_ROOT / "data-repo" / "ilmastolaki_lausunnot")
)
CONCEPTDATA_FILENAME = os.getenv("CONCEPTDATA_FILENAME", "concepts.csv")

REQUIRED_COLUMNS = {"concept"}


def get_concept_data_path() -> Path:
    data_repo = DATA_REPO_PATH.expanduser().resolve()
    concept_data_path = data_repo / CONCEPTDATA_FILENAME

    if not concept_data_path.is_file():
        raise FileNotFoundError(f"Concept data CSV not found at {concept_data_path}")

    return concept_data_path


def read_concept_data(concept_data_path: Path) -> list[tuple]:
    dataframe = pd.read_csv(
            concept_data_path, usecols=lambda column: column in REQUIRED_COLUMNS
        )
    missing = REQUIRED_COLUMNS - set(dataframe.columns)
    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}. "
            f"Available columns: {list(dataframe.columns)}"
        )

    dataframe["concept"] = dataframe["concept"].fillna("").astype(str).str.strip()

    records = []
    for row_number, row in dataframe.iterrows():
        concept = remove_prefix(row["concept"])
        if not concept:
            raise ValueError(f"Missing concept on CSV row {row_number + 2}")

        records.append((concept,))

    return records


def remove_prefix(concept: str) -> str:
    return (concept.removeprefix("YES:").removeprefix("NO:").strip())


async def import_concepts():
    concept_path = get_concept_data_path()
    concepts = read_concept_data(concept_path)
    print(concepts)

    conn = await asyncpg.connect(DATABASE_URL)

    try:
        await conn.executemany(
            """
            INSERT INTO concepts (concept)
            VALUES ($1)
            """,
            concepts,
        )
    finally:
        await conn.close()

    print(f"Imported {len(concepts)} concepts from {concept_path}.")


if __name__ == "__main__":
    asyncio.run(import_concepts())
