import logging
from typing import Sequence

import cv2
import mss
import pydirectinput
import time

from modules.funcs import get_screenshot, min_max, click_on_object_ingame
from log_config import setup_logger
from game_settings import VALUES

FISHING_TEXT = cv2.imread('screenshots/fish_window_text.png')
FISH_PIXEL = cv2.imread('screenshots/fish_pixel.png')
CIRCLE_DIAM = 64

logger = logging.getLogger(__name__)
TIME_BEFORE_REFRESH = 22

def fish_window_pos(sct) -> Sequence[int] | int:
    # Get screenshot and find where fish window is
    screenshot = get_screenshot(sct)
    fishing_text = min_max(screenshot, [FISHING_TEXT])
    return fishing_text


def catch_fish(sct, fishing_text_pos: Sequence[int]) -> None:
    """This function will try to get a screenshot and catch a fish."""

    while True:
        # We will look if the window is still opened and if not, we can think we have caught
        new_screenshot = get_screenshot(sct, fishing_text_pos[0], fishing_text_pos[1], FISHING_TEXT.shape[1],
                                        FISHING_TEXT.shape[0])

        # We will screenshot the place where "Fishing" text should be, if is not there then window closed
        is_opened = min_max(FISHING_TEXT, [new_screenshot])

        # Therefore, we will end the loop and will try to catch a new fish
        if is_opened == -1:
            break

        # Get normalized position (relative 0, 0 towards our fishing window)
        fishing_text_pos_norm = (fishing_text_pos[0] + 16 - CIRCLE_DIAM, fishing_text_pos[1] + 136 - CIRCLE_DIAM)

        # Get a screenshot and find where is fish
        screenshot = get_screenshot(sct, fishing_text_pos_norm[0], fishing_text_pos_norm[1], CIRCLE_DIAM * 2,
                                    CIRCLE_DIAM * 2)

        # Try if there is a fish in the circle
        fish_in_circle = min_max(screenshot, [FISH_PIXEL])

        # If the fish was not found, try to print-screen again and find the fish again
        if fish_in_circle == -1:
            continue

        # Position of fish
        normalized_pos = (fishing_text_pos_norm[0] + fish_in_circle[0], fishing_text_pos_norm[1] + fish_in_circle[1])

        # We found a fish, and we will click on the fish, we do not need to check forbidden areas
        click_on_object_ingame(normalized_pos, timer=0.05, can_click_in_forbidden_area=True)

        # A small pause as the program is too fast
        time.sleep(0.3)

    logger.info("Fish window closed")


def start_fishing() -> None:
    logger.info("STARTING and WAITING -> FISHING")
    time.sleep(5)
    logger.info("BOT STARTED")

    with mss.mss() as sct:
        last_time_fish = time.time()
        while True:
            # Try to catch a fish
            pydirectinput.press("space", presses=5)
            # Try to find if a window opened
            fish_window = fish_window_pos(sct)
            # Looking until a window is opened
            while fish_window == -1:
                fish_window = fish_window_pos(sct)
                pydirectinput.press("space")
                time.sleep(0.2)
                # There is an unknown bug in the game when sometimes the window bugs itself and needs restart
                if time.time() - last_time_fish > TIME_BEFORE_REFRESH:
                    pydirectinput.press("enter")
                    # ? -> _ in CZ keyboard
                    # { -> / in CZ keyboard
                    pydirectinput.write("{", auto_shift=True)
                    pydirectinput.write("rewarp")
                    pydirectinput.write("?", auto_shift=True)
                    pydirectinput.write("user")
                    pydirectinput.press("enter")
                    last_time_fish = time.time()
            # Try to catch a fish when I detect an opened window
            logger.info("fish window opened, trying to catch a fish")
            catch_fish(sct, fish_window)
            time.sleep(VALUES["FISHING_WAIT_TIME"])
            last_time_fish = time.time()


if __name__ == "__main__":
    setup_logger()
    start_fishing()
