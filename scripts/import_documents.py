import csv
import os
from pathlib import Path

import asyncpg
from dotenv import load_dotenv

load_dotenv()

DATA_CSV = Path.home() / "data-repo" / "ilmastolaki_lausunnot" / "documents.csv"


async def import_documents():
    conn = await asyncpg.connect(os.environ["DATABASE_URL"])

    with DATA_CSV.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            await conn.execute(
                """
                INSERT INTO files (
                    id, title, author, source, section, notes, type, date,
                    fileName, statement_count, ocr_damaged, ocr_repairs
                )
                VALUES (
                    $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12
                )
                ON CONFLICT (id) DO UPDATE SET
                    title = EXCLUDED.title,
                    author = EXCLUDED.author,
                    source = EXCLUDED.source,
                    section = EXCLUDED.section,
                    notes = EXCLUDED.notes,
                    type = EXCLUDED.type,
                    date = EXCLUDED.date,
                    fileName = EXCLUDED.fileName,
                    statement_count = EXCLUDED.statement_count,
                    ocr_damaged = EXCLUDED.ocr_damaged,
                    ocr_repairs = EXCLUDED.ocr_repairs
                """,
                int(row["id"]),
                row.get("title"),
                row.get("author"),
                row.get("source"),
                row.get("section"),
                row.get("notes"),
                row.get("type"),
                int(row["date"]) if row.get("date") else None,
                row.get("filename"),
                int(row["statement_count"]) if row.get("statement_count") else None,
                row["ocr_damaged"].strip().lower() == "true" if row.get("ocr_damaged") else False,
                int(row["ocr_repairs"]) if row.get("ocr_repairs") else 0,
            )

    await conn.close()


if __name__ == "__main__":
    import asyncio
    asyncio.run(import_documents())