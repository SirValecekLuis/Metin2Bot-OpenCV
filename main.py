import mss
import pydirectinput
import time
import random
import cv2

THRESHOLD = 0.12
MOVEMENT_LIST = ['W', 'A', 'S', 'D']
TEMPLATE = cv2.imread('metin_picture.png')


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
        pydirectinput.press('y')


def click_on_metin(top_left):
    top_left = (top_left[0] + 30, top_left[1] + 50)
    pydirectinput.moveTo(*top_left)
    pydirectinput.click()


def get_screenshot(sct):
    sct.shot(output="screen.png")
    image = cv2.imread('screen.png')

    return image


def main():
    with mss.mss() as sct:
        while True:
            image = get_screenshot(sct)

            top_left = min_max(image, [TEMPLATE])
            if top_left == -1:
                random_movement(0.5, 1)
                continue

            click_on_metin(top_left)

            time.sleep(0.3)
            random_movement(0.2, 2)

            gather_items()


if __name__ == "__main__":
    main()
