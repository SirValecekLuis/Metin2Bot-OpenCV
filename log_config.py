import logging
import os
from datetime import datetime


def get_project_root():
    current_path = os.path.abspath(__file__)
    return os.path.dirname(current_path)


def setup_logger():
    # Získání cesty k hlavnímu adresáři projektu
    project_root = get_project_root()

    # Vytvoření složky 'logs' v hlavním adresáři, pokud neexistuje
    log_dir = os.path.join(project_root, 'logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Vytvoření názvu logu s aktuálním datumem
    current_date = datetime.now().strftime("%d.%m.%Y")
    log_file = os.path.join(log_dir, f"{current_date}.log")

    with open(log_file, "a") as f:
        f.write("\nNové spuštění\n")

    # Základní konfigurace
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%d-%m-%Y %H:%M:%S',
        filename=log_file,
        filemode='a'
    )

    # Vytvoření console handleru
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Vytvoření formátovače
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%m-%Y %H:%M:%S')
    console_handler.setFormatter(formatter)

    # Přidání console handleru k root loggeru
    logging.getLogger('').addHandler(console_handler)
