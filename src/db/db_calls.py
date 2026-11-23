import asyncpg

from config import DATABASE_URL


async def get_concepts(database_url=DATABASE_URL):
    """Retrieve all concepts, ordered by ID"""
    conn = await asyncpg.connect(database_url)
    try:
        rows = await conn.fetch("SELECT * FROM concepts ORDER BY id")
        return rows
    finally:
        await conn.close()


async def get_concepts_by_id(concept_id, database_url=DATABASE_URL):
    """Retrieve concepts by ID."""
    conn = await asyncpg.connect(database_url)
    try:
        rows = await conn.fetch(
            "SELECT id, concept, stance_label FROM concepts WHERE id = $1", concept_id
        )
        return rows
    finally:
        await conn.close()


async def get_documents(database_url=DATABASE_URL):
    """Retrieve all documents, ordered by ID."""
    conn = await asyncpg.connect(database_url)
    try:
        rows = await conn.fetch("SELECT * FROM files ORDER BY id")
        return rows
    finally:
        await conn.close()


async def get_golden_standard(database_url=DATABASE_URL):
    """Retrieve all golden standard records, ordered by ID."""
    conn = await asyncpg.connect(database_url)
    try:
        rows = await conn.fetch("SELECT * FROM goldenStandard ORDER BY id")
        return rows
    finally:
        await conn.close()


async def get_golden_standard_by_document_id(document_id, database_url=DATABASE_URL):
    """Retrieve golden standard rows for a document, ordered by ID."""
    conn = await asyncpg.connect(database_url)
    try:
        rows = await conn.fetch(
            "SELECT * FROM goldenStandard WHERE document_id = $1 ORDER BY id",
            document_id,
        )
        return rows
    finally:
        await conn.close()


async def get_runs(database_url=DATABASE_URL):
    """Retrieves all evaluation runs, ordered by ID."""
    conn = await asyncpg.connect(database_url)
    try:
        rows = await conn.fetch("SELECT * FROM evaluationRuns ORDER BY id")
        return rows
    finally:
        await conn.close()


async def count_documents_in_run(run_id, database_url=DATABASE_URL):
    """Counts the number of documents in a given evaluation run."""
    conn = await asyncpg.connect(database_url)
    try:
        count = await conn.fetchval(
            "SELECT COUNT(DISTINCT document_id) FROM llmOutput WHERE run_id = $1",
            run_id,
        )
        return count
    finally:
        await conn.close()


async def count_concepts_in_run(run_id, database_url=DATABASE_URL):
    """Counts the number of concepts in a given evaluation run."""
    conn = await asyncpg.connect(database_url)
    try:
        count = await conn.fetchval(
            "SELECT COUNT(DISTINCT concept_id) FROM llmOutput WHERE run_id = $1",
            run_id,
        )
        return count
    finally:
        await conn.close()


async def count_runtime_in_run(run_id, database_url=DATABASE_URL):
    """Counts the runtime of a given evaluation run."""
    conn = await asyncpg.connect(database_url)
    try:
        runtime = await conn.fetchval(
            "SELECT EXTRACT(EPOCH FROM (end_time - start_time)) FROM evaluationRuns WHERE id = $1",
            run_id,
        )
        return runtime
    finally:
        await conn.close()


async def get_llm_output(database_url=DATABASE_URL):
    """Retrieves all LLM output rows, ordered by ID."""
    conn = await asyncpg.connect(database_url)
    try:
        rows = await conn.fetch("SELECT * FROM llmOutput ORDER BY id")
        return rows
    finally:
        await conn.close()


async def save_output(output, database_url=DATABASE_URL):
    """Saves the LLM output rows to the database."""
    rows = [
        (
            row["run_id"],
            row["document_id"],
            row["concept_id"],
            row["present"],
            row["passage"],
            row["agreement"],
            row["status"],
        )
        for row in output
    ]

    conn = await asyncpg.connect(database_url)
    try:
        await conn.executemany(
            """INSERT INTO llmOutput (
            run_id, document_id, concept_id, present, passage, agreement, status)
            VALUES ($1, $2, $3, $4, $5, $6, $7)""",
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


async def retrieve_document_concept_pair(run_id, database_url=DATABASE_URL):
    """Retrieves run_id, document_id and concept_id pair from llmoutput table"""
    conn = await asyncpg.connect(database_url)
    try:
        pairs = await conn.fetch(
            """SELECT run_id, document_id, concept_id, present FROM llmOutput WHERE run_id=$1""",
            run_id,
        )
        return [
            (row["document_id"], row["concept_id"], row["present"]) for row in pairs
        ]
    finally:
        await conn.close()


async def get_latest_run_id(database_url=DATABASE_URL):
    """Retrieves the latest run_id"""
    conn = await asyncpg.connect(database_url)
    try:
        run_id = await conn.fetch("""SELECT MAX(id) FROM evaluationRuns""")
        return run_id
    finally:
        await conn.close()


async def get_run_by_id(run_id, database_url=DATABASE_URL):
    """Retrieves a specific run by ID."""
    conn = await asyncpg.connect(database_url)
    try:
        run = await conn.fetchrow(
            """SELECT * FROM evaluationRuns WHERE id = $1""", run_id
        )
        return run
    finally:
        await conn.close()


async def run_has_output(run_id, database_url=DATABASE_URL):
    """Checks if a run has output in the database."""
    conn = await asyncpg.connect(database_url)
    try:
        count = await conn.fetchval(
            "SELECT COUNT(*) FROM llmOutput WHERE run_id = $1", run_id
        )
        return count > 0
    finally:
        await conn.close()

async def get_failed_outputs(run_id, database_url=DATABASE_URL):
    """Gets llm failed outputs based on run_id"""
    conn = await asyncpg.connect(database_url)
    try:
        fails = await conn.fetch(
            """
            SELECT document_id, concept_id
            FROM llmOutput
            WHERE status = 'failed' AND run_id = $1
            ORDER BY document_id, concept_id
            """,
            run_id,
        )
        return fails, len(fails)
    finally:
        await conn.close()

async def get_prompts(database_url=DATABASE_URL):
    """Retrieves prompts from database."""
    conn = await asyncpg.connect(database_url)
    try:
        return await conn.fetch(
            "SELECT id, prompt FROM prompts ORDER BY id"
        )
    finally:
        await conn.close()
