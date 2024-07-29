import time
import cv2
import pyautogui
import pydirectinput

from game_settings import VALUES
#
IMAGE = cv2.imread('screenshots/test_screenshot4.png')
# NEEDLE = cv2.imread('screenshots/white_pixel.png')

# # Apply NEEDLE matching
# result = cv2.matchTemplate(IMAGE, NEEDLE, cv2.TM_SQDIFF_NORMED)
#
# # Min/Max values for locating the best match
# min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
#
# match_loc = min_loc
#
# # Draw a rectangle around the matched region
# bottom_right = (match_loc[0] + NEEDLE.shape[1], match_loc[1] + NEEDLE.shape[0])
# cv2.rectangle(IMAGE, match_loc, bottom_right, (0, 255, 0), 2)
#
# print(bottom_right)

# Aplikace Cannyho detektoru hran

edges = cv2.Canny(IMAGE, 550, 600)

# Display the IMAGE with the match rectangle
cv2.imshow('IMAGE', edges)
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

# import cv2
# import numpy as np
#
# img = cv2.imread('screenshots/test_screenshot.png')
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#
# edges = cv2.Canny(gray, 300, 350)
#
# contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#
#
# objects = []
#
#
# for i, contour in enumerate(contours):
#
#     area = cv2.contourArea(contour)
#
#
#     if area > 50:
#
#         x, y, w, h = cv2.boundingRect(contour)
#
#
#         objects.append({
#             'id': i,
#             'area': area,
#             'center': (x + w // 2, y + h // 2),
#             'bounding_box': (x, y, w, h)
#         })
#
#
#         cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
#
#
# for obj in objects:
#     print(
#         f"Objekt {obj['id']}: Plocha = {obj['area']}, Střed = {obj['center']}, Ohraničující obdélník = {obj['bounding_box']}")
#
#
# cv2.imshow('Nalezené objekty', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()