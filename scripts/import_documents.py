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
METADATA_FILENAME = os.getenv("METADATA_FILENAME", "documents.csv")
DOCUMENTS_DIR = os.getenv("DOCUMENTS_DIR", "plain")

REQUIRED_COLUMNS = {"author", "filename"}


def get_data_paths() -> tuple[Path, Path]:
    data_repo = DATA_REPO_PATH.expanduser().resolve()
    metadata_path = data_repo / METADATA_FILENAME
    documents_path = (data_repo / DOCUMENTS_DIR).resolve()

    if not metadata_path.is_file():
        raise FileNotFoundError(f"Metadata CSV not found at {metadata_path}")
    if not documents_path.is_dir():
        raise FileNotFoundError(f"Documents directory not found at {documents_path}")

    return metadata_path, documents_path


def read_documents(metadata_path: Path, documents_path: Path) -> list[tuple]:
    dataframe = pd.read_csv(
        metadata_path, usecols=lambda column: column in REQUIRED_COLUMNS
    )
    missing = REQUIRED_COLUMNS - set(dataframe.columns)
    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}. "
            f"Available columns: {list(dataframe.columns)}"
        )

    dataframe["filename"] = dataframe["filename"].fillna("").astype(str).str.strip()
    dataframe["author"] = dataframe["author"].fillna("").astype(str).str.strip()

    records = []
    for row_number, row in dataframe.iterrows():
        filename = row["filename"]
        if not filename:
            raise ValueError(f"Missing filename on CSV row {row_number + 2}")

        document_path = (documents_path / filename).resolve()
        if documents_path not in document_path.parents:
            raise ValueError(f"Filename escapes the data repository: {filename}")
        if not document_path.is_file():
            raise FileNotFoundError(f"Document file not found: {document_path}")

        records.append(
            (
                filename,
                row["author"],
                document_path.read_text(encoding="utf-8"),
            )
        )

    return records


async def import_documents():
    metadata_path, documents_path = get_data_paths()
    documents = read_documents(metadata_path, documents_path)

    conn = await asyncpg.connect(DATABASE_URL)

    try:
        await conn.executemany(
            """
            INSERT INTO files (filename, author, content)
            VALUES ($1, $2, $3)
            """,
            documents,
        )
    finally:
        await conn.close()

    print(f"Imported {len(documents)} documents from {metadata_path}.")


if __name__ == "__main__":
    asyncio.run(import_documents())
