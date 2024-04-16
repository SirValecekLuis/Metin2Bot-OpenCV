import cv2

from game_settings import VALUES

IMAGE = cv2.imread('screen.png')
CURSOR = cv2.imread('cursor.png')

# Apply CURSOR matching
result = cv2.matchTemplate(IMAGE, CURSOR, cv2.TM_SQDIFF_NORMED)

# Min/Max values for locating the best match
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

match_loc = min_loc

# Draw a rectangle around the matched region
bottom_right = (match_loc[0] + CURSOR.shape[1], match_loc[1] + CURSOR.shape[0])
cv2.rectangle(IMAGE, match_loc, bottom_right, (0, 255, 0), 2)

# Display the IMAGE with the match rectangle
cv2.imshow('IMAGE', IMAGE)
cv2.waitKey(0)
cv2.destroyWindow('IMAGE')
