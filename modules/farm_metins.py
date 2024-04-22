import mss
import pydirectinput
import time
import random
import cv2
import numpy as np
from PIL import Image

from game_settings import VALUES

THRESHOLD = 0.12
MOVEMENT_LIST = ["up", "down", "right", "left"]
TEMPLATE = cv2.imread('./metin_picture.png')


def min_max(image, templates: list):
    for template in templates:
        res = cv2.matchTemplate(image, template, cv2.TM_SQDIFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        print(min_val)
        if min_val <= THRESHOLD:
            return min_loc

    return -1


def random_movement(pause: float, times: int):
    for i in range(times):
        movement = MOVEMENT_LIST[random.randint(0, 3)]

        pydirectinput.keyDown(movement)
        time.sleep(pause)
        pydirectinput.keyUp(movement)

    return


def gather_items():
    for _ in range(random.randrange(2, 5)):
        pydirectinput.press('z')  # Change this to Y if pickup does not work


def click_on_metin(sct):
    image = get_screenshot(sct, "./screen.png")
    top_left = min_max(image, [TEMPLATE])
    if top_left == -1:
        return -1
    offset_x, offset_y = 30, 50
    top_left = (top_left[0] + offset_x, top_left[1] + offset_y)
    pydirectinput.moveTo(*top_left)
    pydirectinput.click()
    return 0


def get_screenshot(sct, name: str, x=0, y=0, w=0, h=0, monitor_num=1, save=False):
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

    if save:
        image = Image.frombytes("RGB", image.size, image.rgb)
        image.save(name)

    image = cv2.cvtColor(np.array(image), cv2.COLOR_BGRA2BGR)

    return image


def check_if_clicked():
    # TODO: implement this
    ...

def farm_metins():
    print("STARTING and WAITING")
    time.sleep(5)
    print("BOT STARTED")
    metin_wait = round(VALUES["HP_METIN"] / (VALUES["DAMAGE_METIN"] * 2) - 2)
    # This is to set up camera straight up above you and zoom out max
    pydirectinput.keyDown("g")
    pydirectinput.keyDown("f")
    time.sleep(3)
    pydirectinput.keyUp("g")
    pydirectinput.keyUp("f")

    with mss.mss() as sct:
        while True:
            while click_on_metin(sct) != 0:
                random_movement(0.5, 1)

            time.sleep(0.5)
            gather_items()  # Sometimes metin is already destroyed
            check_if_clicked()
            click_on_metin(sct)
            time.sleep(1)
            gather_items()  # Sometimes metin is already destroyed
            random_movement(0.3, 2)  # When 2 metins are behind each other, this helps

            time.sleep(metin_wait)
            gather_items()
