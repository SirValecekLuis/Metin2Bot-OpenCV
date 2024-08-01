import time
import cv2
import pyautogui
import pydirectinput

from game_settings import VALUES

#
IMAGE = cv2.imread('screenshots/test_screenshot6.png')
NEEDLE = cv2.imread('screenshots/mining_failed.png')

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
# cv2.imshow('IMAGE', IMAGE)
# cv2.waitKey(0)
#
# print(min_val)
#
# print(bottom_right)


# Aplikace Cannyho detektoru hran

# edges = cv2.Canny(IMAGE, 550, 600)
#
# # Display the IMAGE with the match rectangle
# cv2.imshow('IMAGE', edges)
# cv2.waitKey(0)

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

import numpy as np
import cv2
from modules.funcs import min_max_multiple, visualize_matches

# Usage of functions
hay = cv2.imread('screenshots/test_screenshot9.png')  # Load the screenshot
needles = [cv2.imread('screenshots/metin_hp_bar.png')]  # Load templates
threshold = 0.12
max_results = 20

matches = min_max_multiple(hay, needles, threshold, max_results)
print(f"Found {len(matches)} matches:")
for match in matches:
    print(f"Position: ({match[0]}, {match[1]}), Score: {match[2]:.4f}")

# Visualize results
template_size = needles[0].shape[:2][::-1]  # Assume all templates have the same size
result_image = visualize_matches(hay, matches, template_size)



# def calculate_vector_to_metin(screenshot) -> tuple[int, int] | int:
#     min_loc = min_max(screenshot, [METIN_POINT_ON_MAP])
#
#     if min_loc == -1:
#         return -1
#
#     vector = (min_loc[0] - VALUES["MINIMAP_CURSOR_X"], min_loc[1] - VALUES["MINIMAP_CURSOR_Y"])
#     return vector


# def move_to_metin_based_on_vector(vector) -> None:
#     x, y = vector
#     distance = abs(x) + abs(y)
#     travel_time_secs = distance / VALUES["MOVEMENT_SPEED"]
#
#     if y == 0:
#         x_fraction = 1
#     elif abs(x) >= abs(y):
#         x_fraction = abs(y / x)
#     else:
#         x_fraction = abs(x / y)
#
#     y_fraction = 1 - x_fraction if x_fraction != 1 else 1
#
#     # If the vector is 45 °, then it is 1/2 time going x and 1/2 time going y
#     # else get a fraction of how much time travel x and y
#     if x_fraction == 1 and y_fraction == 1:
#         x_travel_time = travel_time_secs / 0.5
#         y_travel_time = x_travel_time
#     else:
#         x_travel_time = travel_time_secs * x_fraction
#         y_travel_time = travel_time_secs * y_fraction
#
#     logger.info(distance, travel_time_secs, x_fraction, y_fraction, x_travel_time, y_travel_time)
#
#     movement_x = "right" if x <= 0 else "left"
#     movement_y = "up" if y <= 0 else "down"
#
#     # Move x axis for x_travel_time
#     pydirectinput.keyDown(movement_x)
#     time.sleep(x_travel_time)
#     pydirectinput.keyUp(movement_x)
#
#     # Move y axis for y_travel_time
#     pydirectinput.keyDown(movement_y)
#     time.sleep(y_travel_time)
#     pydirectinput.keyUp(movement_y)
