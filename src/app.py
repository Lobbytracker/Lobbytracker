import asyncio

from mvp import LlmManager
from db import get_documents, get_concepts


async def get_data():
    documents = await get_documents()
    concepts = await get_concepts()

    return documents, concepts


def instructions():
    print("0. Quit")
    print("1. Dataset files")
    print("2. Codebooks")
    print("3. Etsi valitut konseptit tiedostosta")
    print("4. Aitta prompti")


def print_files():
    pass


def codebooks():
    pass


def choose_file():
    pass


def choose_concepts(concepts: list, concept_ids: str) -> list:
    selected_ids = [int(value.strip()) for value in concept_ids.split(",")]

    selected_concepts = []
    for concept in concepts:
        if concept["id"] in selected_ids:
            selected_concepts.append(concept)

    return selected_concepts

async def run_selected_concepts():
    documents, concepts = await get_data()

    concept_ids = input("Anna konseptien ID numerot (esim. 1, 2, 3): ")
    selected_concepts = choose_concepts(concepts, concept_ids)

    manager = LlmManager(documents, selected_concepts)
    session_list = manager.call_aitta()
    print(session_list)
    return session_list


async def prompts():
    documents, concepts = await get_data()

    manager = LlmManager(documents, concepts)
    session_list = manager.call_aitta()
    print(session_list)

    return session_list


def main():
    commands = {1: print_files, 2: codebooks, 3: run_selected_concepts, 4: prompts}
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
