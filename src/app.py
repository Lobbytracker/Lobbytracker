import asyncio

from mvp import LlmManager
from db import get_documents, get_concepts


async def get_data():
    documents = await get_documents()
    concepts = await get_concepts()

    return documents, concepts


def instructions():
    print("0. Quit")
    print("1. Etsi valitut konseptit tiedostosta")
    print("2. Aitta prompti")


def choose_file(documents: list, file_id: int) -> list:
    selected_ids = [int(value.strip()) for value in str(file_id).split(",")]
    return [document for document in documents if document["id"] in selected_ids]


def choose_concepts(concepts: list, concept_ids: str) -> list:
    selected_ids = [int(value.strip()) for value in concept_ids.split(",")]

    selected_concepts = []
    for concept in concepts:
        if concept["id"] in selected_ids:
            selected_concepts.append(concept)

    return selected_concepts


# async def run_selected_concepts():
#    documents, concepts = await get_data()

#    concept_ids = input("Anna konseptien ID numerot (esim. 1, 2, 3): ")
#    selected_concepts = choose_concepts(concepts, concept_ids)

#    manager = LlmManager(documents, selected_concepts)
#    session_list = manager.call_aitta()
#    print(session_list)
#    return session_list


async def select_and_run():
    documents, concepts = await get_data()

    file_ids = input("Anna tiedoston ID numerot (esim. 1, 2, 3): ")
    selected_documents = choose_file(documents, file_ids)

    concept_ids = input("Anna konseptien ID numerot (esim. 1, 2, 3): ")
    selected_concepts = choose_concepts(concepts, concept_ids)

    if not selected_documents:
        print("Ei valittuja tiedostoja.")
        return

    manager = LlmManager(selected_documents, selected_concepts)
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
    commands = {1: select_and_run, 2: prompts}
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
