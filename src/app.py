from pathlib import Path

from mvp import LlmManager

DATA_DIR = Path(__file__).resolve().parents[1] / "data-repo" / "ilmastolaki_lausunnot" / "mvp_data"

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

def prompts():
    manager = LlmManager(
        DATA_DIR / "001-AKAVA.txt",
        DATA_DIR / "concept.csv",
    )
    chat_completions = manager.call_aitta()

    for chunk in chat_completions:
            if chunk.choices[0].delta.content is not None:
                print(chunk.choices[0].delta.content, end='', flush=True)

def main():
    commands = {1: print_files,
                2: codebooks,
                3: choose_file,
                4: prompts}
    instructions()
    while True:
        command = int(input("\nAnna komento: "))
        if command == 0:
                break
        if command not in commands:
            instructions()
        else:
            executable = commands[command]
            executable()

if __name__ == "__main__":
    main()