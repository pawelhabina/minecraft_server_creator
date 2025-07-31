# main.py

import platform
from colorama import init, Fore, Style
from modules import java_checker, install_mc, config_editor, start_script

init(autoreset=True)


def print_header():
    banner = f"""
{Fore.MAGENTA}{Style.BRIGHT}
  __  __  _____    _____ ______ _   _ 
 |  \/  |/ ____|  / ____|  ____| \ | |
 | \  / | |      | |  __| |__  |  \| |
 | |\/| | |      | | |_ |  __| | . ` |
 | |  | | |____  | |__| | |____| |\  |
 |_|  |_|\_____|  \_____|______|_| \_|
      {Style.RESET_ALL}{Fore.YELLOW}Tworzenie serwerów Minecraft – MC_GEN v0.1
{Style.RESET_ALL}
"""
    print(banner)

def get_os():
    os_name = platform.system()
    print(f"{Fore.CYAN}[i]{Style.RESET_ALL} Wykryty system operacyjny: {os_name}")
    return os_name

def get_user_choice(prompt: str, options: list):
    print(f"\n{Fore.YELLOW}{prompt}{Style.RESET_ALL}")
    for i, opt in enumerate(options, 1):
        print(f"  {i}. {opt}")
    while True:
        choice = input("Wybierz opcję (numer): ")
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return options[int(choice) - 1]
        print(f"{Fore.RED}Nieprawidłowy wybór. Spróbuj ponownie.{Style.RESET_ALL}")


def main():
    print_header()

    choice = get_user_choice("Co chcesz zrobić?", [
        "Stwórz serwer",
        "Sprawdź JAVA",
        "Edytuj config",
        "Stwórz plik startowy"
    ])

    if choice == "Stwórz serwer":
        install_mc.main()
    elif choice == "Sprawdź JAVA":
        java_checker.main()
    elif choice == "Edytuj config":
        config_editor.main()
    elif choice == "Stwórz plik startowy":
        start_script.main()


if __name__ == "__main__":
    main()
