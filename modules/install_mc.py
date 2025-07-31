# install_mc.py

import platform
import subprocess
import shutil
from colorama import init, Fore, Style

def get_os():
    os_name = platform.system()
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

def check_java():
    java_path = shutil.which("java")
    if java_path:
        print(f"{Fore.GREEN}[✓]{Style.RESET_ALL} Java znaleziona: {java_path}")
        try:
            result = subprocess.run(["java", "-version"], capture_output=True, text=True)
            print(f"{Fore.CYAN}[i]{Style.RESET_ALL} Wersja Javy:")
            print((result.stderr or result.stdout).strip())
        except Exception as e:
            print(f"{Fore.RED}[!] Błąd podczas sprawdzania wersji Javy: {e}{Style.RESET_ALL}")
        return True
    else:
        print(f"{Fore.RED}[!] Java nie została znaleziona w systemie.{Style.RESET_ALL}")
        return False


def main():
    os_name = get_os()

    engine = get_user_choice("Wybierz silnik:", [
                                                "Vanilla", 
                                                "Paper", 
                                                "Leaf",
                                                "Forge",
                                                "Fabric",
                                                ])
    
    version = input(f"\n{Fore.YELLOW}Podaj wersję Minecrafta (np. 1.20.1): {Style.RESET_ALL}").strip()

    print(f"{Fore.CYAN}[i]{Style.RESET_ALL} Wybrany silnik: {Fore.GREEN}{engine}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}[i]{Style.RESET_ALL} Wybrana wersja: {Fore.GREEN}{version}{Style.RESET_ALL}")

    has_java = check_java()
    if not has_java:
        get_user_choice("Co chcesz zrobić:", [
                                                "Zainstaluj Javę", 
                                                "Wybierz własną ścieżkę do Javy", 
                                                "Nie rób nic",
                                                ])

    # TODO: Pobieranie pliku serwera na podstawie wersji + silnika


if __name__ == "__main__":
    main()
