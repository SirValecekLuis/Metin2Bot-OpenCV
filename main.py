from modules.farm_metins import farm_metins
from modules.exp import exp


def take_choice():
    while True:
        try:
            choice = int(input("Do you want to farm (1) or exp? (2)\nChoice: "))
            if choice == 1 or choice == 2:
                return choice
        except ValueError:
            ...


def main():
    choice = take_choice()
    if choice == 1:
        farm_metins()
    elif choice == 2:
        exp()


if __name__ == "__main__":
    main()
