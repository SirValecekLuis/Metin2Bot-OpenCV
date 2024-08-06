import logging
from typing import Sequence
import cv2
import time
from game_utils import GameUtils
from game_classes import Monitor, GameState
from game_settings import VALUES


class FishingBot(Monitor, GameState):
    def __init__(self):
        Monitor.__init__(self)
        GameState.__init__(self)

        self.FISHING_TEXT = cv2.imread('screenshots/fish_window_text.png')
        self.FISH_PIXEL = cv2.imread('screenshots/fish_pixel.png')
        self.CIRCLE_DIAM = 64
        self.logger = logging.getLogger(__name__)
        self.TIME_BEFORE_REFRESH = 15
        self.TIME_AFTER_REFRESH = 20

    def get_fish_window_pos(self) -> Sequence[int] | int:
        # Get screenshot and find where fish window is
        screenshot = GameUtils.take_screenshot(self.sct)
        fishing_text = GameUtils.min_max(screenshot, [self.FISHING_TEXT])
        return fishing_text

    def catch_fish(self, fishing_text_pos: Sequence[int]) -> None:
        """This function will try to get a screenshot and catch a fish."""

        while True:
            if GameState.bot_is_running is False:
                return

            # We will look if the window is still opened and if not, we can think we have caught
            new_screenshot = GameUtils.take_screenshot(self.sct, fishing_text_pos[0], fishing_text_pos[1],
                                                       self.FISHING_TEXT.shape[1],
                                                       self.FISHING_TEXT.shape[0])

            # We will screenshot the place where "Fishing" text should be, if is not there then window closed
            is_opened = GameUtils.min_max(self.FISHING_TEXT, [new_screenshot])

            # Therefore, we will end the loop and will try to catch a new fish
            if is_opened == -1:
                break

            # Get normalized position (relative 0, 0 towards our fishing window)
            fishing_text_pos_norm = (
                fishing_text_pos[0] + 16 - self.CIRCLE_DIAM, fishing_text_pos[1] + 136 - self.CIRCLE_DIAM)

            # Get a screenshot and find where is fish
            screenshot = GameUtils.take_screenshot(self.sct, fishing_text_pos_norm[0], fishing_text_pos_norm[1],
                                                   self.CIRCLE_DIAM * 2,
                                                   self.CIRCLE_DIAM * 2)

            # Try if there is a fish in the circle
            fish_in_circle = GameUtils.min_max(screenshot, [self.FISH_PIXEL])

            # If the fish was not found, try to print-screen again and find the fish again
            if fish_in_circle == -1:
                continue

            # Position of fish
            normalized_pos = (
                fishing_text_pos_norm[0] + fish_in_circle[0], fishing_text_pos_norm[1] + fish_in_circle[1])

            # We found a fish, and we will click on the fish, we do not need to check forbidden areas
            GameUtils.mouse_left_click(normalized_pos, timer=0.05, can_click_in_forbidden_area=True)

            # A small pause as the program is too fast
            time.sleep(0.3)

        # Window is closed
        self.logger.info("Fish window closed")
        time.sleep(VALUES["FISHING_WAIT_TIME"])

    def main_loop(self) -> None:
        while True:
            if GameState.bot_is_running is False:
                time.sleep(0.5)
                continue

            last_time_fish = time.time()

            # Try to catch a fish
            GameUtils.press_key("space")

            # Try to find if a window opened
            fish_window = self.get_fish_window_pos()

            # Looking until a window is opened
            while fish_window == -1:
                if GameState.bot_is_running is False:
                    break

                fish_window = self.get_fish_window_pos()
                GameUtils.press_key("space")
                time.sleep(0.5)

                # There is an unknown bug in the game when sometimes the window bugs itself and needs restart
                if time.time() - last_time_fish > self.TIME_BEFORE_REFRESH:
                    GameUtils.press_key("enter")
                    # ? -> _ in CZ keyboard
                    # { -> / in CZ keyboard
                    GameUtils.write("{", auto_shift=True)
                    GameUtils.write("rewarp")
                    GameUtils.write("?", auto_shift=True)
                    GameUtils.write("user")
                    GameUtils.press_key("enter")
                    self.logger.info("Refreshing, bug appeared")
                    time.sleep(self.TIME_AFTER_REFRESH)
                    last_time_fish = time.time()
            else:
                # Try to catch a fish when I detect an opened window
                self.logger.info("fish window opened, trying to catch a fish")
                self.catch_fish(fish_window)

    def run(self) -> None:
        self.logger.info("STARTING and WAITING -> FISHING")

        self.main_loop()
