import time
import cv2
import pyautogui
import pydirectinput

from game_settings import VALUES

IMAGE = cv2.imread('screenshots/test_screenshot.png')
NEEDLE = cv2.imread('screenshots/white_pixel.png')

# Apply NEEDLE matching
result = cv2.matchTemplate(IMAGE, NEEDLE, cv2.TM_SQDIFF_NORMED)

# Min/Max values for locating the best match
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

match_loc = min_loc

# Draw a rectangle around the matched region
bottom_right = (match_loc[0] + NEEDLE.shape[1], match_loc[1] + NEEDLE.shape[0])
cv2.rectangle(IMAGE, match_loc, bottom_right, (0, 255, 0), 2)

print(bottom_right)

# Display the IMAGE with the match rectangle
cv2.imshow('IMAGE', IMAGE)
cv2.waitKey(0)

# from modules.farm_metins import get_screenshot
# import mss
#
# i = 10
# with mss.mss() as sct:
#     while True:
#         get_screenshot(sct, f"hp_bar{i}.png", VALUES["HEALTH_BAR_X"], VALUES["HEALTH_BAR_Y"],
#                        VALUES["HEALTH_BAR_WIDTH"], VALUES["HEALTH_BAR_HEIGHT"], save=True)
#         i += 1
#         time.sleep(3)