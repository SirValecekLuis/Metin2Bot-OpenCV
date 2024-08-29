import logging
import math
import random
import time
from typing import Sequence

import cv2
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed

import pydirectinput
import win32api
import win32gui
from PIL import Image

from game_classes import Area, Monitor

logger = logging.getLogger(__name__)
MOVEMENT_LIST = ["up", "down", "right", "left"]
TOP_AREA = Area(0, 0, 400, 130, "up")
RIGHT_AREA = Area(1645, 0, 1920, 1080, "right")
BOTTOM_AREA = Area(0, 930, 1920, 1080, "down")
FORBIDDEN_AREAS = [TOP_AREA, RIGHT_AREA, BOTTOM_AREA]


class GameUtils:

    @staticmethod
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

    @staticmethod
    def take_screenshot(sct, x=0, y=0, w=0, h=0, save=False, name=""):
        monitor_num = Monitor.monitor_index + 1
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

    @staticmethod
    def min_max(hay: np.ndarray, needles: list[np.ndarray], threshold=0.12) -> Sequence[int] | int:
        """Tries to find a template(needle) from image(hay)"""
        for template in needles:
            res = cv2.matchTemplate(hay, template, cv2.TM_SQDIFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

            if min_val <= threshold:
                return min_loc

        return -1

    @staticmethod
    def process_template(hay, template, threshold):
        res = cv2.matchTemplate(hay, template, cv2.TM_SQDIFF_NORMED)
        locations = np.where(res <= threshold)
        return [(int(x), int(y), float(res[y, x])) for y, x in zip(*locations)]

    @staticmethod
    def min_max_multiple(hay: np.ndarray, needles: list[np.ndarray], threshold=0.12, max_results=10) -> (
            list[tuple[int, int, float]] | int):
        """Finds multiple matches of templates in the image using multithreading."""

        all_matches = []

        with ThreadPoolExecutor() as executor:
            future_to_template = {executor.submit(GameUtils.process_template, hay, template, threshold): template for
                                  template
                                  in needles}
            for future in as_completed(future_to_template):
                all_matches.extend(future.result())

        if not all_matches:
            return -1

        # Sort by similarity (ascending, because TM_SQDIFF_NORMED - lower is better)
        all_matches.sort(key=lambda x: x[2])

        return all_matches[:max_results]

    @staticmethod
    def distance_from_center(match: tuple[int, int, float], center_x: int, center_y: int) -> float:
        """Calculates distance from a center of player"""
        x, y, _ = match
        return math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)

    @staticmethod
    def visualize_matches(screenshot: np.ndarray, matches: list[tuple[int, int, float]],
                          template_size: tuple[int, int]) -> None:
        """
        Draws rectangles around found matches on the screenshot. HELPFUL FOR DEBUGGING
        :param screenshot: Screenshot where draw found matches from min_max_multiple
        :param matches: All matches found on the screenshot from min_max_multiple
        :param template_size: Needle.shape[:2][::-1] -> all shapes have the same size prediction
        :return: None
        """
        result = screenshot.copy()
        for (x, y, score) in matches:
            top_left = (x, y)
            bottom_right = (x + template_size[0], y + template_size[1])
            cv2.rectangle(result, top_left, bottom_right, (0, 255, 0), 2)
            cv2.putText(result, f"{score:.2f}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        cv2.imshow('Results', result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    @staticmethod
    def random_movement(pause=0.3, times=1) -> None:
        """Will move randomly to ensure chaos and therefore unstuck a player"""
        for i in range(times):
            movement = MOVEMENT_LIST[random.randint(0, 3)]

            pydirectinput.keyDown(movement)
            time.sleep(pause)
            pydirectinput.keyUp(movement)

        return

    @staticmethod
    def move(direction: str, pause: float) -> bool:
        try:
            pydirectinput.keyDown(direction)
            time.sleep(pause)
            pydirectinput.keyUp(direction)
        except Exception as e:
            logger.info(f"Movement not successful, exception {e}")
            return False

        return True

    @staticmethod
    def gather_items() -> None:
        """Gathers item on the ground by pressing "y" in the game which is "z" in pydirectinput."""
        for _ in range(random.randrange(2, 5)):
            pydirectinput.press('z')  # Change this to Y if pickup does not work

    @staticmethod
    def mouse_left_click(top_left, offset_x=0, offset_y=0, can_click_in_forbidden_area=False,
                         move_towards_forbidden=False) -> bool:

        top_left = (top_left[0] + offset_x, top_left[1] + offset_y)

        # If the click is somewhere where we said we do not want to click, then we will refuse such a click.
        if can_click_in_forbidden_area is False:
            for area in FORBIDDEN_AREAS:
                if area.is_click_in_area(top_left):
                    logger.info(f"Click in forbidden area {area.top_x, area.top_y, area.bot_x, area.bot_y}")
                    if move_towards_forbidden:
                        GameUtils.move(area.direction, 0.2)
                    return False

        x, y = top_left[0] + Monitor.monitor_left(), top_left[1] + Monitor.monitor_top()

        try:
            pydirectinput.moveTo(x, y, duration=0.06)
            pydirectinput.click(clicks=1, attempt_pixel_perfect=True)
        except pydirectinput.FailSafeException:
            logger.info("Mouse out of monitor bounds")
            return False

        return True

    @staticmethod
    def press_key(key: str, times=1) -> bool:
        """Presses key and check if it didn't fail FaiLSafeException from pydirectinput"""
        try:
            pydirectinput.press(key, presses=times)
            return True
        except pydirectinput.FailSafeException:
            return False

    @staticmethod
    def write(text: str, auto_shift=False) -> bool:
        """Writes text like on keyboard"""
        try:
            pydirectinput.write(message=text, auto_shift=auto_shift)
            return True
        except pydirectinput.FailSafeException:
            return False

    @staticmethod
    def reset_camera_to_default() -> None:
        pydirectinput.keyDown("g")
        pydirectinput.keyDown("f")
        time.sleep(3)
        pydirectinput.keyUp("g")
        pydirectinput.keyUp("f")

    @staticmethod
    def print_mouse_pos() -> None:
        x, y = pydirectinput.position()
        print(f"Aktuální pozice kurzoru: X = {x}, Y = {y}")

    @staticmethod
    def detect_GM() -> None:
        ...
