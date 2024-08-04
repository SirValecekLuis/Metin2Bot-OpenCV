import logging
import time
import cv2

from game_settings import VALUES
from game_utils import GameUtils
from game_classes import Monitor, Keyboard


class MetinFarmer(Monitor, Keyboard):
    def __init__(self):
        Monitor.__init__(self)
        Keyboard.__init__(self)

        self.logger = logging.getLogger(__name__)
        self.METIN_PICTURE = cv2.imread('screenshots/metin_picture3.png')
        self.METIN_HP_BAR = cv2.imread('screenshots/metin_hp_bar.png')
        self.metin_wait = self._calculate_metin_wait()

    def _calculate_metin_wait(self) -> int:
        wait_time = round(VALUES["HP_METIN"] / (VALUES["DAMAGE_METIN"] * 2) + 2)
        return max(wait_time, 1)

    def main_loop(self) -> None:
        """Tries to click on the metin based on coordinates from the screenshot."""

        while True:
            if self.bot_is_running is False:
                time.sleep(0.5)
                continue

            screenshot = GameUtils.take_screenshot(self.sct)
            matches = GameUtils.min_max_multiple(screenshot, [self.METIN_PICTURE], threshold=0.12)

            if matches == -1:
                self.logger.info("Metin not found")
                GameUtils.random_movement()
                continue

            center_x = self.monitor_width // 2
            center_y = self.monitor_height // 2

            closest_match = min(matches, key=lambda match: GameUtils.distance_from_center(match, center_x, center_y))

            # When the metin is found, we will click on it, but check if we didn't click in the forbidden area
            if GameUtils.mouse_left_click(closest_match, 30, 50):
                # Wait a little, so we can click in the game on the metin and correctly check if the HP bar is there or not
                time.sleep(0.5)
                # If metin is alive, we know we clicked on one
                if self.is_metin_alive():
                    # We will be waiting till the metin is alive, and once it is not we will gather dropped items and go on
                    click_time = time.time()
                    while self.is_metin_alive():
                        if self.bot_is_running is False:
                            break

                        time.sleep(0.2)
                        if time.time() - click_time > self.metin_wait * 1.5:
                            self.logger.info("Stucked? Random moving")
                            # If metin is not destroyed in long time prob stuck the character
                            GameUtils.random_movement(0.3, 1)
                            break
                    else:
                        self.logger.info("Metin destroyed")
                        GameUtils.gather_items()
                        time.sleep(0.5)
                        continue

            self.logger.info("Metin miss clicked")
            # We will wait a bit if we failed to click a metin because a character is probably moving towards the
            #   miss clicked metin
            time.sleep(0.3)
            GameUtils.gather_items()

    def is_metin_alive(self) -> bool:
        """Determines if metin is being clicked/destroyed or not."""
        screenshot = GameUtils.take_screenshot(self.sct, 670, 0, 300, 120)
        top_left = GameUtils.min_max(screenshot, [self.METIN_HP_BAR], threshold=0.16)

        if top_left == -1:
            return False

        return True

    def farm_metins(self) -> None:
        self.logger.info("STARTING and WAITING -> FARMING")

        while True:
            if self.bot_is_running:
                GameUtils.reset_camera_to_default()
                break
            time.sleep(0.5)

        self.main_loop()
