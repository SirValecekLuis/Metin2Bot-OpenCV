import logging

import mss
import time
import cv2

from game_settings import VALUES
from modules.funcs import get_screenshot, min_max, random_movement, click_on_object_ingame, reset_camera_to_default, \
    gather_items

METIN_PICTURE = cv2.imread('screenshots/metin_picture.png')
METIN_POINT_ON_MAP = cv2.imread('screenshots/white_pixel.png')


logger = logging.getLogger(__name__)


# def calculate_vector_to_metin(screenshot) -> tuple[int, int] | int:
#     min_loc = min_max(screenshot, [METIN_POINT_ON_MAP])
#
#     if min_loc == -1:
#         return -1
#
#     vector = (min_loc[0] - VALUES["MINIMAP_CURSOR_X"], min_loc[1] - VALUES["MINIMAP_CURSOR_Y"])
#     return vector


# def move_to_metin_based_on_vector(vector) -> None:
#     x, y = vector
#     distance = abs(x) + abs(y)
#     travel_time_secs = distance / VALUES["MOVEMENT_SPEED"]
#
#     # TODO: Fix this
#     if y == 0:
#         x_fraction = 1
#     elif abs(x) >= abs(y):
#         x_fraction = abs(y / x)
#     else:
#         x_fraction = abs(x / y)
#
#     y_fraction = 1 - x_fraction if x_fraction != 1 else 1
#
#     # If the vector is 45 °, then it is 1/2 time going x and 1/2 time going y
#     # else get a fraction of how much time travel x and y
#     if x_fraction == 1 and y_fraction == 1:
#         x_travel_time = travel_time_secs / 0.5
#         y_travel_time = x_travel_time
#     else:
#         x_travel_time = travel_time_secs * x_fraction
#         y_travel_time = travel_time_secs * y_fraction
#
#     logger.info(distance, travel_time_secs, x_fraction, y_fraction, x_travel_time, y_travel_time)
#
#     movement_x = "right" if x <= 0 else "left"
#     movement_y = "up" if y <= 0 else "down"
#
#     # Move x axis for x_travel_time
#     pydirectinput.keyDown(movement_x)
#     time.sleep(x_travel_time)
#     pydirectinput.keyUp(movement_x)
#
#     # Move y axis for y_travel_time
#     pydirectinput.keyDown(movement_y)
#     time.sleep(y_travel_time)
#     pydirectinput.keyUp(movement_y)


def find_and_destroy_metin(sct) -> bool:
    """Tries to click on the metin based on coordinates from the screenshot."""

    screenshot = get_screenshot(sct)
    top_left = min_max(screenshot, [METIN_PICTURE])

    # If we failed to find a metin on the place, we will try to move
    # Otherwise click on metin and destroy it
    if top_left == -1:

        # # Get way where to go
        # vector = calculate_vector_to_metin(screenshot)
        #
        # logger.info(vector)
        #
        # # If white pixel was not found, that means there is no metin around on the map and will try to move randomly to find
        # if vector == -1:
        #     return False
        #
        # # When we found a vector where the metin is, we will move
        # move_to_metin_based_on_vector(vector)

        # TODO: fix this, this is temporary to work
        random_movement(0.3, 1)

        # After moving, we will try to again find a metin
        screenshot = get_screenshot(sct)
        top_left = min_max(screenshot, [METIN_PICTURE])

        if top_left == -1:
            return False

        # When the metin is found, we will click on it
        click_on_object_ingame(top_left, 30, 50)

        # Say that the metin was clicked successfully
        return True

    else:
        # When the metin is found, we will click on it
        click_on_object_ingame(top_left, 30, 50)

        # Say that the metin was clicked successfully
        return True


def check_if_clicked():
    # TODO: implement this and check if the metin is clicked on and if yes then continue if not then try to click again
    #   It would be nice to check when the metin is destroyed (the black bar from metin disappears and by that we know
    #   the metin is destroyed)
    ...


def farm_metins():
    # TODO: only do a job if bot is selected, probably ask OS what window is picked and if not metin, then do not run
    # TODO: try to get screenshot from the game even if the game is not on screen? I have no idea if I can send signals
    #   to the game or not

    logger.info("STARTING and WAITING -> FARMING")
    time.sleep(5)
    logger.info("BOT STARTED")
    metin_wait = round(VALUES["HP_METIN"] / (VALUES["DAMAGE_METIN"] * 2) - 2)
    if metin_wait <= 0:
        metin_wait = 1
    # This is to set up camera straight up above you and zoom out max
    reset_camera_to_default()

    with mss.mss() as sct:
        while True:
            while find_and_destroy_metin(sct) is False:
                random_movement(0.3, 1)

            # time.sleep(0.5)
            # gather_items()  # Sometimes metin is already destroyed
            # check_if_clicked()
            # click_on_metin(sct)
            # time.sleep(1)
            gather_items()  # Sometimes metin is already destroyed
            random_movement(0.3, 2)  # When 2 metins are behind each other, this helps

            time.sleep(metin_wait)
            gather_items()
