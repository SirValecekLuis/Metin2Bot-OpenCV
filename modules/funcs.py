import random
import logging
import time
from typing import Sequence

import cv2
import numpy as np
import pydirectinput
from PIL import Image

pydirectinput.PAUSE = 0.01

logger = logging.getLogger(__name__)

MOVEMENT_LIST = ["up", "down", "right", "left"]
class ForbiddenArea:
    def __init__(self, top_x: int, top_y: int, bot_x: int, bot_y):
        self.top_x = top_x
        self.top_y = top_y
        self.bot_x = bot_x
        self.bot_y = bot_y

    def is_click_in_area(self, coords: tuple[int, int]) -> bool:
        """If click is in forbidden area, returns True, otherwise False"""
        return self.top_x <= coords[0] <= self.bot_x and self.top_y <= coords[1] <= self.bot_y


TOP_AREA = ForbiddenArea(0, 0, 1920, 100)
RIGHT_AREA = ForbiddenArea(1645, 0, 1920, 1080)
BOTTOM_AREA = ForbiddenArea(0, 930, 1920, 1080)
AREAS = [TOP_AREA, RIGHT_AREA, BOTTOM_AREA]

def measure_time(repeat=1, number=1):
    import timeit
    from functools import wraps

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            def timed_func():
                return func(*args, **kwargs)

            times = timeit.repeat(timed_func, repeat=repeat, number=number)

            total_time = sum(times)

            logger.info(f"Funkce '{func.__name__}' byla volána {number}x v {repeat} opakováních.")
            logger.info(f"Celkový čas: {total_time:.6f} sekund")

            return func(*args, **kwargs)

        return wrapper

    return decorator


def get_screenshot(sct, x=0, y=0, w=0, h=0, monitor_num=1, save=False, name=""):
    if x == 0 and y == 0 and w == 0 and h == 0:
        image = sct.grab(sct.monitors[monitor_num])
        image = cv2.cvtColor(np.array(image), cv2.COLOR_BGRA2BGR)
        return image

    # Much faster but painful to implement
    mon = sct.monitors[monitor_num]
    monitor = {
        "top": mon["top"] + y,
        "left": mon["left"] + x,
        "width": w,
        "height": h,
        "mon": monitor_num
    }

    image = sct.grab(monitor)
    image = cv2.cvtColor(np.array(image), cv2.COLOR_BGRA2BGR)

    if save:
        image = Image.frombytes("RGB", image.size, image.rgb)
        image.save(name)

    return image


def min_max(hay: np.ndarray, needles: list, threshold=0.12) -> Sequence[int] | int:
    """Tries to find a template(needle) from image(hay)"""
    for template in needles:
        res = cv2.matchTemplate(hay, template, cv2.TM_SQDIFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        if min_val <= threshold:
            return min_loc

    return -1


def random_movement(pause: float, times: int) -> None:
    """Will move randomly to ensure chaos and therefore unstuck a player"""
    for i in range(times):
        movement = MOVEMENT_LIST[random.randint(0, 3)]

        pydirectinput.keyDown(movement)
        time.sleep(pause)
        pydirectinput.keyUp(movement)

    return


def gather_items() -> None:
    """Gathers item on the ground by pressing "y" in the game which is "z" in pydirectinput."""
    for _ in range(random.randrange(2, 5)):
        pydirectinput.press('z')  # Change this to Y if pickup does not work


def click_on_object_ingame(top_left, offset_x=0, offset_y=0, timer=0.1, can_click_in_forbidden_area=False) -> bool:
    """
    click on screen at x, y position
    :param top_left: tuple (x, y)
    :param offset_x: move + x pixels
    :param offset_y: move + y pixels
    :param timer: time between moving mouse and clicking, should not be lower than 0.05 otherwise causes problems
    :param can_click_in_forbidden_area: When True then the click can click whenever it wants
    :return: False if click was not done, True if clicked
    """
    top_left = (top_left[0] + offset_x, top_left[1] + offset_y)

    # If the click is somewhere where we said we do not want to click, then we will refuse such a click.
    if can_click_in_forbidden_area is False:
        for area in AREAS:
            if area.is_click_in_area(top_left):
                logger.info(f"Click in forbidden area {area.top_x, area.top_y, area.bot_x, area.bot_y}")
                return False

    pydirectinput.moveTo(*top_left, attempt_pixel_perfect=True, duration=0.06)
    # If there is no timer, then the moveTo is not fast enough to move the mouse, so it may click too early
    time.sleep(timer)
    pydirectinput.click(clicks=1) # Sometimes performs double click?

    return True


def reset_camera_to_default() -> None:
    pydirectinput.keyDown("g")
    pydirectinput.keyDown("f")
    time.sleep(3)
    pydirectinput.keyUp("g")
    pydirectinput.keyUp("f")

def print_mouse_pos() -> None:
    x, y = pydirectinput.position()
    print(f"Aktuální pozice kurzoru: X = {x}, Y = {y}")
