import asyncio
import os
import sys
from pathlib import Path

import asyncpg
import pandas as pd

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "******localhost:5432/lobbytracker",
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_REPO_PATH = Path(
    os.getenv("DATA_REPO_PATH", PROJECT_ROOT / "data-repo" / "ilmastolaki_lausunnot")
)
STATEMENTS_FILENAME = os.getenv("STATEMENTS_FILENAME", "statements.csv")
REQUIRED_COLUMNS = {"document_id", "concept", "agreement"}
CONTENT_COLUMNS = {"content", "coded_text"}

sys.path.insert(0, str(PROJECT_ROOT / "src"))
from concepts.concept_management import ConceptManager


def get_statements_path() -> Path:
    data_repo = DATA_REPO_PATH.expanduser().resolve()
    statements_path = data_repo / STATEMENTS_FILENAME

    if not statements_path.is_file():
        raise FileNotFoundError(f"Statements CSV not found at {statements_path}")

    return statements_path


def get_concept_key(raw_concept: str, row_number: int) -> tuple[str, str]:
    stance_label, separator, concept = raw_concept.partition(":")
    stance_label = stance_label.strip()
    concept = concept.strip()

    if not separator or stance_label not in {"YES", "NO"}:
        raise ValueError(
            f"Concept must start with 'YES:' or 'NO:' on CSV row {row_number}"
        )
    if not concept:
        raise ValueError(f"Missing concept on CSV row {row_number}")

    return stance_label, concept


def read_statements(
    statements_path: Path, concepts: list
) -> tuple[list[tuple[int, int, str, str | None, int]], int]:
    dataframe = pd.read_csv(
        statements_path,
        usecols=lambda column: column in REQUIRED_COLUMNS | CONTENT_COLUMNS,
        dtype=str,
    )
    missing = REQUIRED_COLUMNS - set(dataframe.columns)
    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}. "
            f"Available columns: {list(dataframe.columns)}"
        )

    content_column = next(
        (column for column in ("content", "coded_text") if column in dataframe.columns),
        None,
    )
    if content_column is None:
        raise ValueError(
            "Missing required content column: expected 'content' or 'coded_text'. "
            f"Available columns: {list(dataframe.columns)}"
        )

    dataframe = dataframe.fillna("")
    concept_ids = {
        (concept["stance_label"], concept["concept"]): concept["id"]
        for concept in concepts
    }

    records = []
    skipped = 0
    for index, row in dataframe.iterrows():
        row_number = index + 2
        raw_concept = (row["concept"] or "").strip()
        if not raw_concept:
            skipped += 1
            continue

        raw_document_id = (row["document_id"] or "").strip()
        if not raw_document_id:
            raise ValueError(f"Missing document_id on CSV row {row_number}")
        try:
            source_document_id = int(raw_document_id)
        except ValueError as error:
            raise ValueError(
                f"Invalid document_id on CSV row {row_number}: {raw_document_id!r}"
            ) from error

        concept_key = get_concept_key(raw_concept, row_number)
        concept_id = concept_ids.get(concept_key)
        if concept_id is None:
            raise ValueError(
                f"Concept {raw_concept!r} was not found in the concepts table "
                f"on CSV row {row_number}"
            )

        agreement = (row["agreement"] or "").strip() or None
        content = row[content_column]
        records.append((source_document_id, concept_id, content, agreement, row_number))

    return records, skipped


async def import_statements(concepts: list) -> None:
    statements_path = get_statements_path()
    statements, skipped = read_statements(statements_path, concepts)

    conn = await asyncpg.connect(DATABASE_URL)
    try:
        files = await conn.fetch("SELECT id, document_id FROM files")
        file_ids = {}
        for file in files:
            source_document_id = file["document_id"]
            if source_document_id in file_ids:
                raise ValueError(
                    "Multiple files have the same document_id "
                    f"{source_document_id}"
                )
            file_ids[source_document_id] = file["id"]

        rows = []
        for source_document_id, concept_id, content, agreement, row_number in statements:
            document_id = file_ids.get(source_document_id)
            if document_id is None:
                raise ValueError(
                    f"document_id {source_document_id} from statements CSV row "
                    f"{row_number} was not found in files.document_id"
                )
            rows.append((document_id, concept_id, content, agreement))

        async with conn.transaction():
            await conn.executemany(
                """
                INSERT INTO goldenStandard (document_id, concept_id, content, agreement)
                VALUES ($1, $2, $3, $4)
                """,
                rows,
            )
    finally:
        await conn.close()

    print(
        f"Imported {len(rows)} statements from {statements_path}; "
        f"skipped {skipped} rows with an empty concept."
    )


def main() -> None:
    concept_manager = ConceptManager()
    asyncio.run(import_statements(concept_manager.all_concepts))


if __name__ == "__main__":
    main()