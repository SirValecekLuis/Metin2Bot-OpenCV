import mss
import pydirectinput
import time
import random
import cv2

THRESHOLD = 0.12
MOVEMENT_LIST = ["up", "down", "right", "left"]
TEMPLATE = cv2.imread('./metin_picture.png')
FILE_NAME = "./game_settings.py"
VALUES = dict()


def min_max(image, templates):
    for template in templates:
        res = cv2.matchTemplate(image, template, cv2.TM_SQDIFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

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
    image = get_screenshot(sct)
    top_left = min_max(image, [TEMPLATE])
    if top_left == -1:
        return -1
    offset_x, offset_y = 30, 50
    top_left = (top_left[0] + offset_x, top_left[1] + offset_y)
    pydirectinput.moveTo(*top_left)
    pydirectinput.click()
    return 0


def get_screenshot(sct):
    sct.shot(output="./screen.png")
    image = cv2.imread('./screen.png')

    return image


def get_values_from_file():
    try:
        with open(FILE_NAME, "r") as f:
            text = f.readlines()
            for line in text:
                if line.startswith("#"):
                    continue
                line = line.replace(" ", "").strip("\n").split("=")
                if len(line) == 2:
                    VALUES[line[0]] = float(line[1])
    except Exception as e:
        print("Chyba se souborem / v souboru.\n", e)
        exit(-1)


def farm_metins():
    print("STARTING and WAITING")
    time.sleep(5)
    print("BOT STARTED")
    get_values_from_file()
    metin_wait = round(VALUES["HP_METIN"] / (VALUES["DAMAGE_METIN"] * 2))
    # This is to set up camera straight up above you and zoom out max
    pydirectinput.keyDown("g")
    pydirectinput.keyDown("f")
    time.sleep(3)
    pydirectinput.keyUp("g")
    pydirectinput.keyUp("f")

    with mss.mss() as sct:
        while True:
            while click_on_metin(sct) != 0:
                random_movement(0.5, 4)

            time.sleep(0.5)
            click_on_metin(sct)
            time.sleep(1)
            random_movement(0.3, 4)  # When 2 metins are behind each other, this helps

            time.sleep(metin_wait)
            gather_items()
