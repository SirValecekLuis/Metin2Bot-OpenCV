import time
import pydirectinput

from game_settings import VALUES


def exp():
    print("BOT STARTED - WAIT")
    time.sleep(5)
    print("BOT STARTED")
    if VALUES["HOLD_ALT"] == 1:
        pydirectinput.keyDown("alt")

    pydirectinput.keyDown("space")
    while True:
        try:
            for _ in range(3):
                pydirectinput.press("2")
            time.sleep(5)
        except KeyboardInterrupt:
            pydirectinput.keyUp("alt")
            exit(0)
