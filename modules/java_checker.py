# java_checker.py

import os
import platform
import shutil
import tarfile
import zipfile
import requests

ADOPTIUM_API = "https://api.adoptium.net/v3/binary/latest/{version}/ga/{os}/x64/jdk/hotspot/normal/{archive_type}/jdk"

def znajdz_zainstalowane_java():
    system = platform.system()
    znalezione = []

    if system == "Windows":
        mozliwe_sciezki = [
            os.environ.get("JAVA_HOME"),
            "C:\\Program Files\\Java",
            "C:\\Program Files (x86)\\Java"
        ]
        for sciezka in mozliwe_sciezki:
            if sciezka and os.path.exists(sciezka):
                for katalog in os.listdir(sciezka):
                    pelna = os.path.join(sciezka, katalog, "bin", "java.exe")
                    if os.path.isfile(pelna):
                        znalezione.append((katalog, os.path.dirname(pelna)))

    elif system in ["Linux", "Darwin"]:
        jvm_path = "/usr/lib/jvm/"
        if os.path.exists(jvm_path):
            for katalog in os.listdir(jvm_path):
                java_bin = os.path.join(jvm_path, katalog, "bin", "java")
                if os.path.isfile(java_bin) and os.access(java_bin, os.X_OK):
                    znalezione.append((katalog, os.path.dirname(java_bin)))

        java_global = shutil.which("java")
        if java_global:
            znalezione.append(("system-java", os.path.dirname(java_global)))

    return znalezione

def wyswietl_wersje_java(wersje):
    if not wersje:
        print("Nie posiadasz żadnej zainstalowanej wersji Java.")
    else:
        print("Lista zainstalowanych wersji Java:")
        for i, (nazwa, sciezka) in enumerate(wersje, start=1):
            print(f"{i}. {nazwa} ({sciezka})")

def pobierz_i_zainstaluj_java(wersja):
    system = platform.system()
    if system == "Windows":
        os_name = "windows"
        archive_type = "zip"
        install_dir = "C:\\Program Files\\Java"
    elif system == "Linux":
        os_name = "linux"
        archive_type = "tar.gz"
        install_dir = "/usr/lib/jvm"
    else:
        print("Niestety, system nie jest wspierany.")
        return

    url = ADOPTIUM_API.format(version=wersja, os=os_name, archive_type=archive_type)
    print(f"Pobieranie Java {wersja} z:\n{url}")

    try:
        response = requests.get(url, stream=True)
        if response.status_code != 200:
            print("Nie udało się pobrać Javy. Sprawdź wersję lub połączenie internetowe.")
            return

        nazwa_pliku = f"jdk-{wersja}.{archive_type}"
        with open(nazwa_pliku, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print("Pobrano. Rozpakowywanie...")

        if not os.path.exists(install_dir):
            os.makedirs(install_dir)

        if archive_type == "zip":
            with zipfile.ZipFile(nazwa_pliku, 'r') as zip_ref:
                zip_ref.extractall(install_dir)
        else:  # tar.gz
            with tarfile.open(nazwa_pliku, "r:gz") as tar_ref:
                tar_ref.extractall(install_dir)

        print(f"Pomyślnie zainstalowano Java {wersja} do {install_dir}")
        os.remove(nazwa_pliku)

    except Exception as e:
        print(f"Błąd podczas instalacji: {e}")

def pokaz_menu():
    print("\nCo chcesz zrobić:")
    print("1. Powrót do menu")
    print("2. Zainstaluj JAVA")

    wybor = input("Wybierz opcję (1/2): ")
    if wybor == "1":
        print("Powrót do menu...")
    elif wybor == "2":
        try:
            wersja = int(input("Podaj wersję Java do instalacji (od 8 do 24): "))
            if wersja < 8 or wersja > 24:
                print("Niepoprawna wersja. Musi być od 8 do 24.")
                return
            pobierz_i_zainstaluj_java(str(wersja))
        except ValueError:
            print("Niepoprawna wartość.")
    else:
        print("Niepoprawny wybór.")

def main():
    wersje = znajdz_zainstalowane_java()
    wyswietl_wersje_java(wersje)
    pokaz_menu()

if __name__ == "__main__":
    main()
