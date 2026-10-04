import unittest
import db
import asyncpg

# First needs the test db to be created in Docker. Command:
"""
docker run --rm --name lobbytracker-test-db \
  -e POSTGRES_DB=lobbytracker_test \
  -e POSTGRES_USER=test_user \
  -e POSTGRES_PASSWORD=test_password \
  -p 127.0.0.1:5433:5432 \
  -d postgres:18
"""

DATABASE_URL = "postgresql://test_user:test_password@localhost:5433/lobbytracker_test"

class TestDatabase(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        await db.init_db(DATABASE_URL)

    async def test_concepts_table_correct(self):
        conn = await asyncpg.connect(DATABASE_URL)
        try:
            rows = await conn.fetch(
                """
                SELECT column_name
                FROM information_schema.columns
                WHERE table_schema = 'public'
                    AND table_name = 'concepts'
                ORDER BY ordinal_position
                """
            )
            self.assertEqual(
                ["id", "concept", "definition"],
                [row["column_name"] for row in rows],
            )
        finally:
            await conn.close()

    async def test_files_table_correct(self):
        conn = await asyncpg.connect(DATABASE_URL)
        try:
            rows = await conn.fetch(
                """
                SELECT column_name
                FROM information_schema.columns
                WHERE table_schema = 'public'
                    AND table_name = 'files'
                ORDER BY ordinal_position
                """
            )
            self.assertEqual(
                ["id", "filename", "author", "content"],
                [row["column_name"] for row in rows],
            )
        finally:
            await conn.close()

    async def test_goldenstandard_table_correct(self):
        conn = await asyncpg.connect(DATABASE_URL)
        try:
            rows = await conn.fetch(
                """
                SELECT column_name
                FROM information_schema.columns
                WHERE table_schema = 'public'
                    AND table_name = 'goldenstandard'
                ORDER BY ordinal_position
                """
            )
            self.assertEqual(
                ["id", "filename", "content", "statementcount"],
                [row["column_name"] for row in rows],
            )
        finally:
            await conn.close()
