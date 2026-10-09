import asyncio
import csv
import os
from pathlib import Path

import asyncpg

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://localhost:5432/lobbytracker",
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_REPO_PATH = Path(
    os.getenv("DATA_REPO_PATH", PROJECT_ROOT / "data-repo" / "ilmastolaki_lausunnot")
)
CONCEPTDATA_FILENAME = os.getenv("CONCEPTDATA_FILENAME", "concepts.csv")
REQUIRED_COLUMNS = {"concept_id", "concept"}


def get_concept_data_path() -> Path:
    path = DATA_REPO_PATH.expanduser().resolve() / CONCEPTDATA_FILENAME
    if not path.is_file():
        raise FileNotFoundError(f"Concept data CSV not found at {path}")
    return path


def read_concept_data(path: Path) -> list[tuple[int, str, str]]:
    records = []
    seen_ids = set()

    with path.open(newline="", encoding="utf-8-sig") as csv_file:
        reader = csv.DictReader(csv_file)
        if reader.fieldnames is None:
            raise ValueError(f"Concept CSV has no header: {path}")

        missing_columns = REQUIRED_COLUMNS - set(reader.fieldnames)
        if missing_columns:
            raise ValueError(
                f"Missing required columns: {sorted(missing_columns)}. "
                f"Available columns: {reader.fieldnames}"
            )

        for row_number, row in enumerate(reader, start=2):
            try:
                concept_id = int(row["concept_id"])
            except (TypeError, ValueError) as error:
                raise ValueError(
                    f"Invalid concept_id on CSV row {row_number}"
                ) from error

            if concept_id in seen_ids:
                raise ValueError(
                    f"Duplicate concept_id {concept_id} on CSV row {row_number}"
                )
            seen_ids.add(concept_id)

            raw_concept = (row["concept"] or "").strip()
            if raw_concept.startswith("YES:"):
                stance_label = "YES"
            elif raw_concept.startswith("NO:"):
                stance_label = "NO"
            else:
                raise ValueError(
                    f"Concept must start with 'YES:' or 'NO:' on CSV row {row_number}"
                )

            concept = raw_concept.split(":", maxsplit=1)[1].strip()
            if not concept:
                raise ValueError(f"Missing concept name on CSV row {row_number}")

            records.append((concept_id, stance_label, concept))

    return records


async def import_concepts() -> None:
    concept_path = get_concept_data_path()
    concepts = read_concept_data(concept_path)
    if not concepts:
        raise ValueError(f"No concepts found in {concept_path}")

    conn = await asyncpg.connect(DATABASE_URL)
    try:
        async with conn.transaction():
            await conn.executemany(
                """
                INSERT INTO concepts (concept_id, stance_label, concept)
                VALUES ($1, $2, $3)
                ON CONFLICT (concept_id) DO UPDATE
                SET stance_label = EXCLUDED.stance_label,
                    concept = EXCLUDED.concept
                """,
                concepts,
            )
    finally:
        await conn.close()

    print(f"Imported {len(concepts)} concepts from {concept_path}.")


if __name__ == "__main__":
    asyncio.run(import_concepts())
