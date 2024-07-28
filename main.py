from modules.farm_metins import farm_metins
from modules.exp import exp
from modules.mining import start_mining


def take_choice():
    while True:
        try:
            choice = int(input("Do you want to farm (1) or exp (2) or mine (3)?\nChoice: "))
            if 1 <= choice <= 3:
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


if __name__ == "__main__":
    main()
