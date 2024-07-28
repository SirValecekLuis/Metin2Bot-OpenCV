import random
import logging
import time
from typing import Sequence

import cv2
import numpy as np
import pydirectinput
from PIL import Image

logger = logging.getLogger(__name__)

THRESHOLD = 0.12
MOVEMENT_LIST = ["up", "down", "right", "left"]


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


def find_needle_in_hay(hay, needle: list) -> Sequence[int] | int:
    """Tries to find a template(needle) from image(hay)"""
    for template in needle:
        res = cv2.matchTemplate(hay, template, cv2.TM_SQDIFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        if min_val <= THRESHOLD:
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
    """Gathers item on the ground by pressing "y" in the game which is "z" in pydirecinput."""
    for _ in range(random.randrange(2, 5)):
        pydirectinput.press('z')  # Change this to Y if pickup does not work


def click_on_object_ingame(top_left, offset_x=0, offset_y=0) -> None:
    top_left = (top_left[0] + offset_x, top_left[1] + offset_y)
    pydirectinput.moveTo(*top_left)
    pydirectinput.click()


def reset_camera_to_default() -> None:
    pydirectinput.keyDown("g")
    pydirectinput.keyDown("f")
    time.sleep(3)
    pydirectinput.keyUp("g")
    pydirectinput.keyUp("f")


def check_if_click_is_not_in_forbidden_area() -> None:
    """This function ensures that the click is not near UI that can be accidentally opened."""
    ...


def print_mouse_pos() -> None:
    x, y = pydirectinput.position()
    print(f"Aktuální pozice kurzoru: X = {x}, Y = {y}")
