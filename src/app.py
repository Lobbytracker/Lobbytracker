import asyncio

from mvp import DEFAULT_MODEL, LlmManager, get_available_models
from db import get_documents, get_concepts

selected_model = DEFAULT_MODEL


async def get_data():
    documents = await get_documents()
    concepts = await get_concepts()

    return documents, concepts


def instructions():
    print("0. Quit")
    print("1. Etsi valitut konseptit tiedostosta")
    print("2. Aitta prompti")
    print("3. Vaihda tekoälymallia")


def print_documents(documents: list):
    print("\nEnsimmäiset 10 dokumenttia:")
    for document in documents[:10]:
        print(f"ID: {document['id']}, Nimi: {document['filename']}")


def print_concepts(concepts: list):
    print("\n10 ensimmäistä konseptia:")
    for concept in concepts[:10]:
        print(f"ID: {concept['id']}, Konsepti: {concept['concept']}")


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


def change_model():
    global selected_model

    try:
        models = get_available_models()
    except Exception as error:
        print(f"Mallien hakeminen epäonnistui: {error}")
        return

    if not models:
        print("Aitta ei palauttanut yhtään mallia.")
        return

    if selected_model not in models:
        print(f"Nykyinen malli ei ole Aittan katalogissa: {selected_model}")

    print("\nSaatavilla olevat mallit:")
    for index, model in enumerate(models, start=1):
        marker = " (käytössä)" if model == selected_model else ""
        print(f"{index}. {model}{marker}")

    try:
        choice = int(input("Valitse mallin numero: "))
        selected_model = models[choice - 1]
    except (ValueError, IndexError):
        print("Virheellinen valinta.")
        return

    print(f"Käytettävä malli: {selected_model}")


async def select_and_run():
    documents, concepts = await get_data()

    print_documents(documents)

    file_ids = input("Anna tiedoston ID numerot (esim. 1, 2, 3): ")
    selected_documents = choose_file(documents, file_ids)

    print_concepts(concepts)
    concept_ids = input("Anna konseptien ID numerot (esim. 1, 2, 3): ")
    selected_concepts = choose_concepts(concepts, concept_ids)

    if not selected_documents:
        print("Ei valittuja tiedostoja.")
        return

    manager = LlmManager(selected_documents, selected_concepts, selected_model)
    session_list = manager.call_aitta()
    print(session_list)
    return session_list


async def prompts():
    documents, concepts = await get_data()

    manager = LlmManager(documents, concepts, selected_model)
    session_list = manager.call_aitta()
    print(session_list)

    return session_list


def main():
    commands = {1: select_and_run, 2: prompts, 3: change_model}
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
