"""rgb_to_hsv module

    Converts rgb color scale to hsv

    Returns:
        hsv: tuple (converted values from rgb to hsv)
"""
import colorsys

def rgb_to_hsv(rgb):
        r, g, b = rgb[0] / 255.0, rgb[1] / 255.0, rgb[2] / 255.0
        hsv = colorsys.rgb_to_hsv(r, g, b)
        return hsv
