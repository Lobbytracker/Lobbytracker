import asyncio
import os

import asyncpg

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/lobbytracker",
)

async def connect_db():
    conn = await asyncpg.connect(DATABASE_URL)

    try:
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS concepts (
                id SERIAL PRIMARY KEY,
                concept TEXT,
                definition TEXT
            )
            """
        )
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS files (
                id SERIAL PRIMARY KEY, 
                fileName TEXT, 
                author TEXT, 
                content TEXT
            )
            """
        )
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS goldenStandard (
                id SERIAL PRIMARY KEY, 
                fileName TEXT, 
                content TEXT, 
                statementCount INTEGER
            )
            """
        )
    finally:
        await conn.close()




if __name__ == "__main__":
    asyncio.run(connect_db())


# docker run --name lobbytracker-postgres \
#   -e POSTGRES_USER=postgres \
#   -e POSTGRES_PASSWORD=postgres \
#   -e POSTGRES_DB=lobbytracker \
#   -p 5432:5432 \
#   -d postgres:16