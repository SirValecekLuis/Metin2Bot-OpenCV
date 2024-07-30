import logging
from typing import Sequence
import mss
import time
import cv2
from game_settings import VALUES
from modules.funcs import take_screenshot, min_max, click, gather_items, reset_camera_to_default, random_movement


class MiningBot:
    def __init__(self):
        self.VEIN_PICTURE = cv2.imread('screenshots/vein_picture.png')
        self.VEIN_PICTURE2 = cv2.imread('screenshots/vein_picture2.png')
        self.MINING_SUCCESS = cv2.imread("screenshots/mining_success.png")
        self.MINING_FAILED = cv2.imread("screenshots/mining_failed.png")
        self.NOTHING_TO_MINE = cv2.imread('screenshots/nothing_to_mine.png')
        self.logger = logging.getLogger(__name__)
        self.failed_previously = False
        self.stopped_previously = False

    def check_mining_state(self, sct) -> bool:
        time_start = time.time()

        while True:
            if time.time() - time_start > VALUES["VEIN_WAIT_TIME"]:
                self.logger.info("Mining stopped after waiting time")
                return True

            screenshot = take_screenshot(sct, 777, 970, 260, 75)

            if not self.failed_previously:
                mining_failed = min_max(screenshot, [self.MINING_FAILED], threshold=0.12)
                if mining_failed != -1:
                    self.logger.info("Mining failed, trying to mine again")
                    self.failed_previously = True
                    return False

            if not self.stopped_previously:
                mining_stopped = min_max(screenshot, [self.NOTHING_TO_MINE], threshold=0.12)
                if mining_stopped != -1:
                    self.logger.info("Mine deposit disappeared, trying to find a new vein")
                    return False

            if time.time() - time_start > 4:
                mining_completed = min_max(screenshot, [self.MINING_SUCCESS], threshold=0.12)
                if mining_completed != -1:
                    self.logger.info("Mining completed successfully")
                    return True

            time.sleep(0.5)

    def find_vein(self, sct) -> Sequence[int] | int:
        screenshot = take_screenshot(sct)
        return min_max(screenshot, [self.VEIN_PICTURE, self.VEIN_PICTURE2], threshold=0.15)

    def mine_vein(self, sct) -> bool:
        top_left = self.find_vein(sct)
        if top_left == -1:
            return False

        if click(top_left, 50, 20) is False:
            return False

        if self.check_mining_state(sct):
            time.sleep(0.2)
            gather_items()
            self.failed_previously = False
            self.stopped_previously = False
            return True

        return False

    def start_mining(self) -> None:
        self.logger.info("STARTING and WAITING -> MINING")
        time.sleep(5)
        self.logger.info("BOT STARTED")

        reset_camera_to_default()
        with mss.mss() as sct:
            while True:
                while self.mine_vein(sct) is False:
                    random_movement(0.3, 1)
