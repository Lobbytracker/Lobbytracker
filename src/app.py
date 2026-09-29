import asyncio
from pathlib import Path

from mvp import LlmManager
from db import get_concepts


async def get_data():
    concepts = await get_concepts()

    return concepts


DATA_DIR = (
    Path(__file__).resolve().parents[1]
    / "data-repo"
    / "ilmastolaki_lausunnot"
    / "mvp_data"
)


def instructions():
    print("0. Quit")
    print("1. Dataset files")
    print("2. Codebooks")
    print("3. Etsi konseptit tiedostosta")
    print("4. Aitta prompti")


def print_files():
    pass


def codebooks():
    pass


def choose_file():
    print("Choose file")


async def prompts():
    data = await get_data()
    manager = LlmManager(DATA_DIR / "001-AKAVA.txt", data)
    session_list = manager.call_aitta()
    print(session_list)
    return session_list


def main():
    commands = {1: print_files, 2: codebooks, 3: choose_file, 4: prompts}
    instructions()
    while True:
        command = int(input("\nAnna komento: "))
        if command == 0:
            break
        if command not in commands:
            instructions()
        else:
            executable = commands[command]
            if asyncio.iscoroutinefunction(executable):
                asyncio.run(executable())
            else:
                executable()


if __name__ == "__main__":
    main()
