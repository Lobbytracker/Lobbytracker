import asyncio

import db.db_calls as db


class RunManager:
    """Class for managing evaluation run infromation."""

    def __init__(self, all_runs=None):
        if not all_runs:
            self.all_runs = asyncio.run(self.get_all_from_db())
        else:
            self.all_runs = all_runs

    async def get_all_from_db(self):
        """Returns all runs from the database."""
        return await db.get_runs()

    def get_next_ten_runs(self, start):
        """Returns 10 runs starting from the given index, newest run first."""

        return self.all_runs[::-1][start : start + 10]

    def get_by_ids(self, selected_ids: str):
        """Returns all runs that contain the given ids."""
        ids_to_list = [int(value.strip()) for value in str(selected_ids).split(",")]
        return [run for run in self.all_runs if run["id"] in ids_to_list]

    def get_all_ids(self):
        """Returns the ids of all runs as a set."""
        return {run["id"] for run in self.all_runs}
