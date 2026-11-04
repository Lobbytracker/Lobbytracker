import asyncio
import os

import asyncpg

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/lobbytracker",
)


async def init_db(database_url=DATABASE_URL):
    """Initializes the database."""
    conn = await asyncpg.connect(database_url)

    try:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS concepts (
                id SERIAL PRIMARY KEY,
                stance_label TEXT,
                concept TEXT
            )
            """)
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS files (
                id SERIAL PRIMARY KEY,
                document_id INTEGER NOT NULL,
                fileName TEXT,
                author TEXT,
                content TEXT
            )
            """)
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS goldenStandard (
                id SERIAL PRIMARY KEY, 
                document_id INT NOT NULL REFERENCES files(id),
                concept_id INT NOT NULL REFERENCES concepts(id), 
                passage TEXT,
                agreement TEXT
            )
            """)
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS evaluationRuns (
                id SERIAL PRIMARY KEY,
                model TEXT NOT NULL,
                prompt TEXT NOT NULL,
                start_time TIMESTAMP NOT NULL,
                end_time TIMESTAMP NOT NULL,
                repetitions INT, 
                completed_all BOOLEAN NOT NULL
            )
            """)
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS llmOutput (
                id SERIAL PRIMARY KEY,
                run_id INT NOT NULL REFERENCES evaluationRuns(id),
                document_id INT NOT NULL REFERENCES files(id),
                concept_id INT NOT NULL REFERENCES concepts(id),
                present BOOLEAN,
                passage TEXT,
                agreement BOOLEAN, 
                CHECK (present OR agreement IS NULL)
            )
            """)
    finally:
        await conn.close()


if __name__ == "__main__":
    asyncio.run(init_db())
