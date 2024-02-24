"""Map module

    This module contains all the mapping methods to convert
    image properties to sound properties and also convert
    sound properties to image properties
"""

# Maps brightness to volume
def map_brightness_to_volume(brightness):
    return brightness * 10

# Maps hue to frequency
def map_hue_to_frequency(hue):
    return int(hue * 20) + 20

# Maps saturation to audio property
def map_saturation_to_audio_property(saturation):
    return int(saturation * 50)

# Maps volume to brightness
def map_volume_to_brightness(volume):
    return volume / 20

# Maps frequency to hue
def map_frequency_to_hue(frequency):
    return (frequency - 20) / 200

# Maps panning to color distribution
def map_panning_to_color_distribution(panning):
    return (panning / 2) + 0.5

# Maps audio property to saturation
def map_audio_property_to_saturation(audio_texture):
    return audio_texture / 50

# Maps color distribution to panning
def map_color_distribution_to_panning(color_distribution):
    return (color_distribution - 0.5) * 2
