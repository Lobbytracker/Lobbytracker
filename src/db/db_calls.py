import os

import asyncpg

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/lobbytracker",
)


async def get_concepts(database_url=DATABASE_URL):
    conn = await asyncpg.connect(database_url)
    try:
        rows = await conn.fetch("SELECT * FROM concepts ORDER BY id")
        return rows
    finally:
        await conn.close()


async def get_concepts_by_id(concept_id, database_url=DATABASE_URL):
    conn = await asyncpg.connect(database_url)
    try:
        rows = await conn.fetch(
            "SELECT id, concept, stance_label FROM concepts WHERE id = $1", concept_id
        )
        return rows
    finally:
        await conn.close()


async def get_documents(database_url=DATABASE_URL):
    conn = await asyncpg.connect(database_url)
    try:
        rows = await conn.fetch("SELECT * FROM files ORDER BY id")
        return rows
    finally:
        await conn.close()


async def get_golden_standard(database_url=DATABASE_URL):
    conn = await asyncpg.connect(database_url)
    try:
        rows = await conn.fetch("SELECT * FROM goldenStandard ORDER BY id")
        return rows
    finally:
        await conn.close()


async def get_golden_standard_by_document_id(document_id, database_url=DATABASE_URL):
    conn = await asyncpg.connect(database_url)
    try:
        rows = await conn.fetch(
            "SELECT * FROM goldenStandard WHERE document_id = $1 ORDER BY id",
            document_id,
        )
        return rows
    finally:
        await conn.close()


async def get_llm_output(database_url=DATABASE_URL):
    conn = await asyncpg.connect(database_url)
    try:
        rows = await conn.fetch("SELECT * FROM llmOutput ORDER BY id")
        return rows
    finally:
        await conn.close()


async def save_output(output, database_url=DATABASE_URL):
    rows = [
        (
            row["run_id"],
            row["document_id"],
            row["concept_id"],
            row["present"],
            row["passage"],
            row["agreement"],
        )
        for row in output
    ]

    conn = await asyncpg.connect(database_url)
    try:
        await conn.executemany(
            """INSERT INTO llmOutput (
            run_id, document_id, concept_id, present, passage, agreement)
            VALUES ($1, $2, $3, $4, $5, $6)""",
            rows,
        )
    finally:
        await conn.close()


async def create_evaluation_run(model, prompt, database_url=DATABASE_URL):
    """Creates a new evaluation run in the database and returns the run ID."""
    conn = await asyncpg.connect(database_url)
    try:
        return await conn.fetchval(
            """INSERT INTO evaluationRuns (model, prompt, start_time, end_time, completed_all)
            VALUES ($1, $2, NOW(), NOW(), FALSE)
            RETURNING id""",
            model,
            prompt,
        )
    finally:
        await conn.close()


async def save_evaluation_run(
    run_id, repetitions, completed_all, database_url=DATABASE_URL
):
    """Updates the evaluation run with the given ID in the database."""
    conn = await asyncpg.connect(database_url)
    try:
        await conn.execute(
            """UPDATE evaluationRuns SET end_time = NOW(), repetitions = $2, completed_all = $3
            WHERE id = $1""",
            run_id,
            repetitions,
            completed_all,
        )
    finally:
        await conn.close()

async def retrieve_document_concept_pair(
        run_id, database_url=DATABASE_URL
):
    """Retrieves run_id, document_id and concept_id pair from llmoutput table"""
    conn = await asyncpg.connect(database_url)
    try:
        pairs = await conn.execute(
            """SELECT run_id, document_id, concept_id FROM llmOutput WHERE run_id=$1""",
            run_id,
        )
        return pairs
    finally:
        await conn.close()

async def get_latest_run_id(database_url=DATABASE_URL
):
    """Retrieves the latest run_id"""
    conn = await asyncpg.connect(database_url)
    try:
        run_id = await conn.execute(
            """SELECT MAX(id) FROM evaluationRuns"""
        )
        return run_id
    finally:
        await conn.close()