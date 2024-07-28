import mss
import time
import cv2

from game_settings import VALUES
from modules.farm_metins import get_screenshot, gather_items, random_movement, min_max, reset_camera_to_default, \
    click_on_object_ingame

VEIN_PICTURE = cv2.imread('screenshots/vein_picture.png')


def find_vein(sct) -> bool:
    """Tries to find a vein and clicks on it"""
    screenshot = get_screenshot(sct)
    top_left = min_max(screenshot, [VEIN_PICTURE])

    # If vein was not found
    if top_left == -1:
        return False

    # if was found, click on it
    click_on_object_ingame(top_left, 20, 30)
    time.sleep(VALUES["VEIN_WAIT_TIME"])
    gather_items()
    return True


def start_mining() -> None:
    print("STARTING and WAITING -> MINING")
    time.sleep(5)
    print("BOT STARTED")
    reset_camera_to_default()
    with mss.mss() as sct:
        while True:
            while find_vein(sct) is False:
                random_movement(0.3, 1)
