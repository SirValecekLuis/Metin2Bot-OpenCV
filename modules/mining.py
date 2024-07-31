import logging
from typing import Sequence
import mss
import time
import cv2
import pydirectinput

from game_settings import VALUES
from modules.funcs import take_screenshot, min_max, click, gather_items, reset_camera_to_default, random_movement, \
    min_max_multiple, distance_from_center, measure_time


class MiningBot:
    def __init__(self):
        self.VEIN_PICTURE = cv2.imread('screenshots/vein.png')
        self.NEEDLES = [self.VEIN_PICTURE]

        self.MINING_SUCCESS = cv2.imread('screenshots/mining_success.png')
        self.MINING_FAILED = cv2.imread('screenshots/mining_failed.png')
        self.NOTHING_TO_MINE = cv2.imread('screenshots/nothing_to_mine.png')
        self.logger = logging.getLogger(__name__)
        self.failed_previously = False
        self.stopped_previously = False
        self.sct = None

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

    def check_mining_state(self) -> bool:
        time_start = time.time()

        while True:
            if time.time() - time_start > VALUES["VEIN_WAIT_TIME"]:
                self.logger.info("Mining stopped after waiting time")
                return True

            screenshot = take_screenshot(self.sct, 777, 970, 260, 75)

            if not self.failed_previously:
                mining_failed = min_max(screenshot, [self.MINING_FAILED], threshold=0.12)
                if mining_failed != -1:
                    self.logger.info("Mining failed, trying to mine again")
                    x, y = pydirectinput.position()
                    # Move a mouse a little to fix a click
                    pydirectinput.moveTo(x + 2, y + 2)
                    self.failed_previously = True

                    return False

            if not self.stopped_previously:
                mining_stopped = min_max(screenshot, [self.NOTHING_TO_MINE], threshold=0.12)
                if mining_stopped != -1:
                    self.logger.info("Mine deposit disappeared, trying to find a new vein")
                    self.stopped_previously = True
                    return False

            if time.time() - time_start > 4:
                mining_completed = min_max(screenshot, [self.MINING_SUCCESS], threshold=0.12)
                if mining_completed != -1:
                    self.logger.info("Mining completed successfully")
                    return True

            time.sleep(0.5)

    def find_vein(self) -> Sequence[int] | int:
        """
        Tries to find a vein from a screenshot
        :return: (x, y) if found, -1 if not
        """
        screenshot = take_screenshot(self.sct)
        matches = min_max_multiple(screenshot, self.NEEDLES, threshold=0.2)

        if matches == -1:
            return -1

        center_x = self.monitor_width // 2
        center_y = self.monitor_height // 2

        closest_match = min(matches, key=lambda match: distance_from_center(match, center_x, center_y))

        return closest_match[0], closest_match[1]

    def mine_vein(self):
        top_left = self.find_vein()
        if top_left == -1:
            random_movement(0.3, 1)
            return

        if click(top_left, 50, 20) is False:
            return

        if self.check_mining_state():
            gather_items()
            self.failed_previously = False
            self.stopped_previously = False

    def start_mining(self) -> None:
        self.logger.info("STARTING and WAITING -> MINING")
        time.sleep(5)
        self.logger.info("BOT STARTED")

        reset_camera_to_default()
        with mss.mss() as sct:
            self.sct = sct
            while True:
                self.mine_vein()
