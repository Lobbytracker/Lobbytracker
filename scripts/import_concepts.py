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

required_columns = {"concept", "definition"}


def get_concept_data_path() -> Path:
    data_repo = DATA_REPO_PATH.expanduser().resolve()
    concept_data_path = data_repo / CONCEPTDATA_FILENAME

    if not concept_data_path.is_file():
        raise FileNotFoundError(f"Concept data CSV not found at {concept_data_path}")

    return concept_data_path    

def read_concept_data(concept_data_path: Path) -> list[tuple]:
    pass # TODO: implement


