import logging
import time

import keyboard
import win32api
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
    timer_is_on = False
    bot_running_time = 0
    turn_off_after_hours = 0

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

    @staticmethod
    def check_bot_timer():
        if GameState.timer_is_on:
            if time.time() - GameState.bot_running_time > GameState.turn_off_after_hours:
                GameState.bot_is_running = False


class Monitor:
    monitors = win32api.EnumDisplayMonitors()
    monitor_index = 0

    def __init__(self):
        self.sct = mss()

    @staticmethod
    def monitor_width() -> int:
        _, _, screen_right, _ = Monitor.monitors[Monitor.monitor_index][2]
        return screen_right

    @staticmethod
    def monitor_height() -> int:
        _, _, _, screen_bottom = Monitor.monitors[Monitor.monitor_index][2]
        return screen_bottom

    @staticmethod
    def monitor_top() -> int:
        _, screen_top, _, _ = Monitor.monitors[Monitor.monitor_index][2]
        return screen_top

    @staticmethod
    def monitor_left() -> int:
        screen_left, _, _, _ = Monitor.monitors[Monitor.monitor_index][2]
        return screen_left
