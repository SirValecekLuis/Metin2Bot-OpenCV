import logging

import cv2
import mss
import pydirectinput
import time

from modules.funcs import get_screenshot, find_needle_in_hay, click_on_object_ingame
from log_config import setup_logger

FISHING_TEXT = cv2.imread('screenshots/fish_window_text.png')
FISH_PIXEL = cv2.imread('screenshots/fish_pixel.png')
CIRCLE_DIAM = 64

logger = logging.getLogger(__name__)


def find_pos_of_fish_window(sct) -> tuple[int, int]:
    # Get screenshot and find where fish window is
    while True:
        screenshot = get_screenshot(sct)
        fishing_text = find_needle_in_hay(screenshot, [FISHING_TEXT])
        if fishing_text != -1:
            return fishing_text


def catch_fish(sct) -> None:
    """This function will try to get a screenshot and catch a fish."""
    FISHING_TEXT_POS = find_pos_of_fish_window(sct)
    FISHING_TEXT_POS_NORM = (FISHING_TEXT_POS[0] + 16 - CIRCLE_DIAM, FISHING_TEXT_POS[1] + 136 - CIRCLE_DIAM)

    while True:
        start_time = time.time()
        # Get screenshot and find where fish window is
        screenshot = get_screenshot(sct, FISHING_TEXT_POS_NORM[0], FISHING_TEXT_POS_NORM[1], CIRCLE_DIAM * 2,
                                    CIRCLE_DIAM * 2)

        # Try if there is a fish in the circle
        fish_in_circle = find_needle_in_hay(screenshot, [FISH_PIXEL])

        # If the fish was not found, try to print the screen again and find the fish again
        if fish_in_circle == -1:
            continue

        normalized_pos = (FISHING_TEXT_POS[0] + 16 - CIRCLE_DIAM, FISHING_TEXT_POS[1] + 136 - CIRCLE_DIAM)
        normalized_pos = (normalized_pos[0] + fish_in_circle[0], normalized_pos[1] + fish_in_circle[1])

        # We found a fish, and we will click on the fish
        click_on_object_ingame(normalized_pos)
        logger.info("Fish found and clicked")
        end_time = time.time() - start_time

    logger.info("Fish window closed")


def fish_window_opened(sct) -> bool:
    # Get a screenshot and find if the fish window is opened
    screenshot = get_screenshot(sct)
    fishing_text = find_needle_in_hay(screenshot, [FISHING_TEXT])
    if fishing_text == -1:
        return False

    return True


def start_fishing() -> None:
    logger.info("STARTING and WAITING -> FISHING")
    time.sleep(5)
    logger.info("BOT STARTED")
    with mss.mss() as sct:
        while True:
            pydirectinput.press("space", interval=0.1)
            while not fish_window_opened(sct):
                logger.info("fish window not opened, checking again.")
                time.sleep(0.05)
            logger.info("fish window opened, trying to catch a fish")
            catch_fish(sct)
            time.sleep(3)


if __name__ == "__main__":
    setup_logger()
    start_fishing()
