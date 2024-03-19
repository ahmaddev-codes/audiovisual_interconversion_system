"""Map module

    This module contains all the mapping methods to convert
    image properties to sound properties and also convert
    sound properties to image properties
"""


def map_brightness_to_volume(brightness):
    # Map brightness to volume
    return brightness * 100

def map_hue_to_frequency(hue):
    # Map hue to frequency
    return hue * 10000

def map_saturation_to_audioproperty(saturation):
    # Map saturation to audio property
    return saturation

def map_volume_to_brightness(volume):
    # Map volume to brightness
    # Normalize volume to the range [0, 1]
    return (volume + 50) / 100

def map_frequency_to_hue(frequency):
    # Map frequency to hue
    # Normalize frequency to the range [0, 1]
    return frequency / 10000  # Adjust as needed

def map_audio_property_to_saturation(audio_texture):
    # Map audio texture to saturation
    # Normalize audio texture to the range [0, 1]
    return audio_texture

def map_color_distribution_to_panning(panning):
    # Map panning to color distribution
    # Normalize panning to the range [-1, 1]
    return (panning + 1) / 2
