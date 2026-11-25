import asyncio

from config import TEST_DATABASE_URL
from db.initialize_db import init_db

if __name__ == "__main__":
    asyncio.run(init_db(TEST_DATABASE_URL))
