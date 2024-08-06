import logging

import keyboard
from mss import mss

logger = logging.getLogger(__name__)


class Area:
    def __init__(self, top_x: int, top_y: int, bot_x: int, bot_y, direction: str):
        self.top_x = top_x
        self.top_y = top_y
        self.bot_x = bot_x
        self.bot_y = bot_y
        self.direction = direction

        self.sct = mss()
        self.monitor = self.sct.monitors[1]
        self.screen_width = self.monitor["width"]
        self.screen_height = self.monitor["height"]

    def is_click_in_area(self, coords: tuple[int, int]) -> bool:
        """
        If click is in forbidden area or outside screen boundaries, returns True, otherwise False
        """
        x, y = coords

        if x < 0 or x >= self.screen_width or y < 0 or y >= self.screen_height:
            return True  # Out of screen

        if self.top_x <= x <= self.bot_x and self.top_y <= y <= self.bot_y:
            return True  # In forbidden area

        return False  # Click is valid


class GameState:
    bot_is_running = False
    def __init__(self):
        keyboard.add_hotkey("F11", self.start)
        keyboard.add_hotkey("F12", self.pause)

    @staticmethod
    def start():
        if GameState.bot_is_running is False:
            logger.info("Bot unpaused")
            GameState.bot_is_running = True

    @staticmethod
    def pause():
        if GameState.bot_is_running is True:
            logger.info("Bot paused")
            GameState.bot_is_running = False


class Monitor:

    def __init__(self):
        self.sct = mss()

    @property
    def monitor_width(self) -> int:
        if self.sct is not None:
            return self.sct.monitors[1]["width"]
        return 0

    @property
    def monitor_height(self) -> int:
        if self.sct is not None:
            return self.sct.monitors[1]["height"]
        return 0
