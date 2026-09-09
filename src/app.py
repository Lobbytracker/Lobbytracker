import ai

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

def main():
    commands = {1: print_files,
                2: codebooks,
                3: choose_file,
                4: ai.aitta_prompts}
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