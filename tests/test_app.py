import unittest
from unittest.mock import patch, MagicMock
from app import FileConverter
from tkinter import messagebox

class TestFileConverter(unittest.TestCase):
    def setUp(self):
        self.root = MagicMock()
        self.app = FileConverter(self.root)

    def test_choose_file_valid_image(self):
        with patch('tkinter.filedialog.askopenfilename', return_value='test_image.jpg'):
            self.app.choose_file()
            self.assertEqual(self.app.file_path, 'test_image.jpg')

    def test_choose_file_invalid_image_extension(self):
        with patch('tkinter.filedialog.askopenfilename', return_value='test_image.txt'):
            with patch.object(messagebox, 'showwarning') as mock_showwarning:
                self.app.choose_file()
                mock_showwarning.assert_called_once_with("Warning", "Please select a valid image file!")

    def test_choose_file_valid_audio(self):
        with patch('tkinter.filedialog.askopenfilename', return_value='test_audio.wav'):
            self.app.choose_file()
            self.assertEqual(self.app.file_path, 'test_audio.wav')

    def test_choose_file_invalid_audio_extension(self):
        with patch('tkinter.filedialog.askopenfilename', return_value='test_audio.mp4'):
            with patch.object(messagebox, 'showwarning') as mock_showwarning:
                self.app.choose_file()
                mock_showwarning.assert_called_once_with("Warning", "Please select a valid audio file!")

    def test_convert_file_image_to_audio(self):
        self.app.conversion_mode.set(0)  # Set conversion mode to Image to Sound
        self.app.file_path = 'test_image.jpg'

        with patch('tkinter.messagebox.showinfo') as mock_showinfo:
            self.app.image_to_audio_conversion()
            mock_showinfo.assert_called_once_with("Conversion Complete", "Audio file generated successfully!")

    def test_convert_file_sound_to_image(self):
        self.app.conversion_mode.set(1)  # Set conversion mode to Sound to Image
        self.app.file_path = 'test_audio.wav'

        with patch('tkinter.messagebox.showinfo') as mock_showinfo:
            self.app.audio_to_image_conversion()
            mock_showinfo.assert_called_once_with("Conversion Complete", "Image file generated successfully!")

    def test_update_scales_image_to_sound(self):
        # Test if scales are updated when conversion mode is changed to Image to Sound
        self.app.conversion_mode.set(0)
        self.app.update_scales()
        self.assertTrue(self.app.image_to_sound_frame.winfo_children())
        self.assertFalse(self.app.sound_to_image_frame.winfo_children())

    def test_update_scales_sound_to_image(self):
        # Test if scales are updated when conversion mode is changed to Sound to Image
        self.app.conversion_mode.set(1)
        self.app.update_scales()
        self.assertTrue(self.app.sound_to_image_frame.winfo_children())
        self.assertFalse(self.app.image_to_sound_frame.winfo_children())

    def test_map_brightness_to_volume(self):
        # Test mapping of brightness to volume
        self.assertEqual(self.app.map_brightness_to_volume(0.5), 0.5)

    def test_map_hue_to_frequency(self):
        # Test mapping of hue to frequency
        self.assertEqual(self.app.map_hue_to_frequency(0.5), 0.5)

    def test_map_color_distribution_to_panning(self):
        # Test mapping of color distribution to panning
        self.assertEqual(self.app.map_color_distribution_to_panning(0.5), 0.5)

    def test_extract_audio_properties(self):
        # Test extraction of audio properties
        audio = MagicMock()
        audio_properties = self.app.extract_audio_properties(audio)
        self.assertIsInstance(audio_properties, dict)

if __name__ == '__main__':
    unittest.main()
