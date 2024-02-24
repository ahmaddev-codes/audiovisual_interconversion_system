import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from pydub import AudioSegment
from PIL import Image
from app import FileConverter

class TestFileConverter(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = FileConverter(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_choose_file(self):
        # Mock the filedialog.askopenfilename method
        with patch("tkinter.filedialog.askopenfilename", return_value="/path/to/file.txt"):
            self.app.choose_file()
            self.assertEqual(self.app.file_path, "/path/to/file.txt")

    def test_extract_audio_texture(self):
        samples = [0, 10, 20, 30, 40]
        result = self.app.extract_audio_texture(samples)
        self.assertEqual(result, 10.0)

    def test_extract_panning(self):
        samples = [1, 2, 3, 4, 5, 6]
        result = self.app.extract_panning(samples)
        self.assertEqual(result, 1.0)

    def test_extract_audio_properties(self):
        audio = MagicMock(spec=AudioSegment, frame_rate=44100)
        audio.get_array_of_samples.return_value = [1, 2, 3, 4, 5]
        result = self.app.extract_audio_properties(audio)
        self.assertEqual(result, {'volume': 6.666666666666667e-06, 'frequency': 2.0, 'audio_texture': 1.0, 'panning': 3.0})

    def test_map_brightness_to_volume(self):
        result = self.app.map_brightness_to_volume(0.5)
        self.assertEqual(result, 5.0)

    def test_map_hue_to_frequency(self):
        result = self.app.map_hue_to_frequency(0.5)
        self.assertEqual(result, 30)

    def test_map_saturation_to_audio_property(self):
        result = self.app.map_saturation_to_audio_property(0.5)
        self.assertEqual(result, 25)

    def test_map_volume_to_brightness(self):
        result = self.app.map_volume_to_brightness(5.0)
        self.assertEqual(result, 0.25)

    def test_map_frequency_to_hue(self):
        result = self.app.map_frequency_to_hue(40)
        self.assertEqual(result, 0.1)

    def test_map_panning_to_color_distribution(self):
        result = self.app.map_panning_to_color_distribution(0.5)
        self.assertEqual(result, 0.75)

    def test_map_audio_property_to_saturation(self):
        result = self.app.map_audio_property_to_saturation(25)
        self.assertEqual(result, 0.5)

    def test_map_color_distribution_to_panning(self):
        result = self.app.map_color_distribution_to_panning(0.75)
        self.assertEqual(result, 0.5)

    def test_image_to_audio_conversion(self):
        # Mock the necessary methods and attributes
        self.app.file_path = "./test_image.jpg"
        self.app.brightness_var.set(0.5)
        self.app.hue_var.set(0.5)
        self.app.saturation_var.set(0.5)
        self.app.panning_var.set(0.5)

        with patch("tkinter.messagebox.showinfo") as mock_showinfo, \
            patch("pydub.generators.Sine") as mock_sine, \
            patch("pydub.AudioSegment") as mock_audio_segment, \
            patch("pydub.AudioSegment.export") as mock_export:
            mock_export.return_value = mock_audio_segment
            self.app.image_to_audio_conversion()

        mock_showinfo.assert_called_once_with("Audio Generated", f"Audio file generated: {'output_audio.mp3'}")
        mock_sine.assert_called_once()
        mock_audio_segment.assert_called_once_with.silent(duration=500)
        mock_audio_segment.return_value.overlay.assert_called_once_with(mock_sine.return_value - 5.0)
        mock_audio_segment.return_value.pan.assert_called_once_with(0.5)
        mock_audio_segment.return_value.fade_in.assert_called_once_with(100)
        mock_audio_segment.return_value.fade_out.assert_called_once_with(100)
        mock_export.assert_called_once_with('output_audio.mp3', format='mp3')


    def test_audio_to_image_conversion(self):
        # Mock the necessary methods and attributes
        self.app.file_path = "./test_audio.mp3"
        self.app.volume_var.set(0.5)
        self.app.frequency_var.set(0.5)
        self.app.audio_texture_var.set(0.5)
        self.app.panning_var.set(0.5)

        with patch("tkinter.messagebox.showinfo") as mock_showinfo, \
            patch("PIL.Image.open") as mock_open:
            # Create a mock image instance and mock the save method
            mock_image_instance = mock_open.return_value
            mock_image_instance.save.return_value = None

            self.app.audio_to_image_conversion()

        mock_showinfo.assert_called_once_with("Image Generated", f"Image file generated: {'output_image.png'}")
        mock_open.assert_called_once_with('./test_audio.mp3')
        mock_image_instance.save.assert_called_once_with('output_image.png')

if __name__ == "__main__":
    unittest.main()
