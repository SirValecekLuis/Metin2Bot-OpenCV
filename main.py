import logging
import time

import win32api

from game_classes import Monitor, GameState
from modules.farm_metins import MetinFarmer
from modules.exp import ExpBot
from modules.mining import MiningBot
from modules.fishing import FishingBot
from log_config import setup_logger

logger = logging.getLogger(__name__)


def take_choice() -> int:
            while True:
                try:
                    choice = int(input("Do you want to farm (1) or exp (2) or mine (3) or fishing(4)?\nChoice: "))
                    if choice < 1 or choice > 4:
                        continue
                except ValueError:
                    continue

            while True:
                try:
                    Monitor.monitor_index = int(input("Monitor? Index from 0: "))
                    if Monitor.monitor_index >= len(win32api.EnumDisplayMonitors()):
                        logger.error(f"Screen {Monitor.monitor_index} does not exist.")
                        exit(1)
                    break
                except ValueError:
                    continue

            while True:
                timer_choice = input("Do you want a timer? (y) or (n): ").lower()
                if timer_choice == "n":
                    GameState.timer_is_on = False
                elif timer_choice == "y":
                    GameState.timer_is_on = True
                else:
                    continue
                break

            while True and GameState.timer_is_on is True:
                try:
                    hours = int(input("How many hours?: "))
                    mins = int(input("How many minutes?: "))
                    secs = int(input("How many seconds?: "))

                    GameState.turn_off_after_hours = hours + (mins / 60) + (secs / 3600)
                except ValueError:
                    continue

            return choice



def main():
    choice = take_choice()
    GameState.bot_running_time = time.time()
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
