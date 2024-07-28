import logging

import cv2
import mss
import pydirectinput
import numpy as np

from PIL import Image, ImageDraw

from funcs import get_screenshot, measure_time
from log_config import setup_logger

logger = logging.getLogger(__name__)


@measure_time()
def get_circle_from_screenshot(screenshot, center_x, center_y, radius):
    """From given screenshot it will make the circular shape where to catch a fish"""

    # Make a mask
    mask = Image.new('L', (screenshot.shape[1], screenshot.shape[0]), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((center_x - radius, center_y - radius, center_x + radius, center_y + radius), fill=255)

    # Make it np array
    mask_array = np.array(mask)

    # Apply mask
    result = np.dstack((screenshot, mask_array))

    # Cut it
    left = max(0, center_x - radius)
    top = max(0, center_y - radius)
    right = min(screenshot.shape[1], center_x + radius)
    bottom = min(screenshot.shape[0], center_y + radius)

    result = result[top:bottom, left:right]

    return result


def catch_fish(sct) -> bool:
    """This function will try to get a screenshot and cath a fish."""
    screenshot = get_screenshot(sct)
    screenshot = get_circle_from_screenshot(screenshot, 300, 300, 50)
    cv2.imshow('IMAGE', screenshot)
    cv2.waitKey(0)
    return True


def start_fishing() -> None:
    with mss.mss() as sct:
        while True:
            pydirectinput.press("space")
            catch_fish(sct)


if __name__ == "__main__":
    setup_logger()
    start_fishing()
