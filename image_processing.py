# STEP 2 (PART1) : CONVERTING RGB IMAGES TO BLACK AND WHITE IMAGES

import numpy as np
import cv2

minValue = 70


def func(path):
    frame = cv2.imread(path)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 2)

    _, res = cv2.threshold(blur, minValue, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    return res
