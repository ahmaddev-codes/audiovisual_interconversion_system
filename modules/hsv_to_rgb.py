"""hsv_to_rgb module

This module converts HSV values to RGB value
"""


import colorsys

def hsv_to_rgb(h, s, v):
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return int(r * 255), int(g * 255), int(b * 255)