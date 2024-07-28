from modules.farm_metins import farm_metins
from modules.exp import exp
from modules.mining import start_mining
from modules.fishing import start_fishing
from log_config import setup_logger


def take_choice():
    while True:
        try:
            choice = int(input("Do you want to farm (1) or exp (2) or mine (3) or fishing(4)?\nChoice: "))
            if 1 <= choice <= 4:
                return choice
        except ValueError:
            ...


def main():
    choice = take_choice()
    if choice == 1:
        farm_metins()
    elif choice == 2:
        exp()
    elif choice == 3:
        start_mining()
    elif choice == 4:
        start_fishing()


if __name__ == "__main__":
    setup_logger()
    main()
