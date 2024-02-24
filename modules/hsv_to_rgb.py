"""hsv_to_rgb module

This module converts HSV values to RGB value
"""

def hsv_to_rgb(h, s, v):
    hi = (h * 6) % 6
    hi = int(hi)
    f = (h * 6) - hi
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)

    if hi == 0:
        return int(v * 255), int(t * 255), int(p * 255)
    elif hi == 1:
        return int(q * 255), int(v * 255), int(p * 255)
    elif hi == 2:
        return int(p * 255), int(v * 255), int(t * 255)
    elif hi == 3:
        return int(p * 255), int(q * 255), int(v * 255)
    elif hi == 4:
        return int(t * 255), int(p * 255), int(v * 255)
    else:
        return int(v * 255), int(p * 255), int(q * 255)