from modules.farm_metins import MetinFarmer
from modules.exp import ExpBot
from modules.mining import MiningBot
from modules.fishing import FishingBot
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
        bot = MetinFarmer()
        bot.run()
    elif choice == 2:
        bot = ExpBot()
        bot.run()
    elif choice == 3:
        bot = MiningBot()
        bot.run()
    elif choice == 4:
        bot = FishingBot()
        bot.run()


if __name__ == "__main__":
    setup_logger()
    main()
