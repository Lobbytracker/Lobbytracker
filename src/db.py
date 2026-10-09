import asyncio
import os

import asyncpg

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/lobbytracker",
)


async def init_db(database_url=DATABASE_URL):
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
                content TEXT,
                agreement TEXT,
                statementCount INTEGER
            )
            """)
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS llmOutput (
                id SERIAL PRIMARY KEY,
                document_id INT NOT NULL REFERENCES files(id),
                concept_id INT NOT NULL REFERENCES concepts(id),
                concept TEXT NOT NULL,
                decision TEXT NOT NULL,
                passage TEXT
            )
            """)
    finally:
        await conn.close()


async def get_concepts(database_url=DATABASE_URL):
    conn = await asyncpg.connect(database_url)
    try:
        rows = await conn.fetch("SELECT * FROM concepts ORDER BY id")
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


async def save_output(output, database_url=DATABASE_URL):
    rows = [(
        row["document_id"],
        row["concept_id"],
        row["concept"],
        row["decision"],
        row["passage"]
    ) for row in output]

    conn = await asyncpg.connect(database_url)
    try:
        await conn.executemany(
            """INSERT INTO llmOutput (
            document_id, concept_id, concept, decision, passage)
            VALUES ($1, $2, $3, $4, $5)""", rows
        )
    finally:
        await conn.close()


if __name__ == "__main__":
    asyncio.run(init_db())
