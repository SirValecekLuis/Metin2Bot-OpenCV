import logging
import time
import pydirectinput

from game_settings import VALUES
from game_utils import GameUtils
from game_classes import Monitor, GameState

logger = logging.getLogger(__name__)


class ExpBot(Monitor, GameState):

    def __init__(self):
        Monitor.__init__(self)
        GameState.__init__(self)

    def run(self):
        logger.info("STARTING AND WAITING -> EXP")
        time.sleep(5)
        logger.info("BOT STARTED")
        if VALUES["HOLD_ALT"] == 1:
            pydirectinput.keyDown("alt")

        pydirectinput.keyDown("space")

        while True:
            if GameState.bot_is_running:
                try:
                    for _ in range(3):
                        pydirectinput.press("2")
                    time.sleep(5)
                except KeyboardInterrupt:
                    pydirectinput.keyUp("alt")
                    exit(0)
