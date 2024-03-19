import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageFilter
from pydub import AudioSegment
from pydub.generators import Sine
from modules.map import *
from modules.hsv_to_rgb import *
from modules.rgb_to_hsv import *
from modules.map import *
from modules.extract import *
import hashlib


class FileConverter:
    def __init__(self, master):
        self.master = master
        self.master.title("AV-Interconversion System")
        self.master.geometry("400x600")
        self.master.minsize(400, 400)

        self.create_variables()
        self.create_gui()

    def create_variables(self):
        self.brightness_var = tk.DoubleVar()
        self.hue_var = tk.DoubleVar()
        self.saturation_var = tk.DoubleVar()
        self.volume_var = tk.DoubleVar()
        self.frequency_var = tk.DoubleVar()
        self.panning_var = tk.DoubleVar()
        self.audio_texture_var = tk.DoubleVar()

        self.file_path = None
        self.conversion_mode = tk.IntVar(value=0)

    def create_gui(self):
        self.create_labels()
        self.create_buttons()
        self.create_radio_buttons()
        self.create_frames()
        self.create_scales()
        self.create_convert_button()
        self.create_file_path_label()

    def create_labels(self):
        tk.Label(self.master, text="Audio-Visual Interconversion System", font=("Helvetica", 16)).pack(pady=10)

    def create_buttons(self):
        tk.Button(self.master, text="Select File", command=self.choose_file, width=30).pack(pady=5)

    def create_radio_buttons(self):
        tk.Radiobutton(self.master, text="Image to Sound", variable=self.conversion_mode, value=0, command=self.show_image_to_sound).pack(pady=2)
        tk.Radiobutton(self.master, text="Sound to Image", variable=self.conversion_mode, value=1, command=self.show_sound_to_image).pack(pady=2)

    def create_frames(self):
        self.image_to_sound_frame = tk.Frame(self.master)
        self.image_to_sound_frame.pack(pady=5)

        self.sound_to_image_frame = tk.Frame(self.master)
        self.sound_to_image_frame.pack(pady=5)

    def create_scales(self):
        scales_config_image_to_sound = [
            ("Brightness", self.brightness_var, 0, 1, 0.01),
            ("Hue", self.hue_var, 0, 1, 0.01),
            ("Saturation", self.saturation_var, 0, 1, 0.01),
            ("Audio Texture", self.audio_texture_var, 0, 1, 0.01),
        ]

        scales_config_sound_to_image = [
            ("Volume", self.volume_var, 0, 1, 0.01),
            ("Frequency", self.frequency_var, 0, 1, 0.01),
            ("Panning", self.panning_var, -1, 1, 0.01),
        ]

        for label, var, from_, to, resolution in scales_config_image_to_sound:
            tk.Scale(self.image_to_sound_frame, label=label, variable=var, from_=from_, to=to, resolution=resolution,
                    orient="horizontal", length=300).pack(pady=2)

        for label, var, from_, to, resolution in scales_config_sound_to_image:
            scale = tk.Scale(self.sound_to_image_frame, label=label, variable=var, from_=from_, to=to, resolution=resolution,
                            orient="horizontal", length=300)
            scale.pack(pady=2)

        self.show_image_to_sound()


    def show_image_to_sound(self):
        self.image_to_sound_frame.pack(pady=5)
        self.sound_to_image_frame.pack_forget()

    def show_sound_to_image(self):
        self.sound_to_image_frame.pack(pady=5)
        self.image_to_sound_frame.pack_forget()

    def create_convert_button(self):
        tk.Button(self.master, text="Convert", command=self.convert_file, width=30).pack(pady=40, side="bottom")

    def create_file_path_label(self):
        max_label_width = self.master.winfo_reqwidth() + 40
        self.file_path_label = tk.Label(self.master, text="Selected File: None", wraplength=max_label_width)
        self.file_path_label.pack(pady=5)

    def update_file_path_label(self):
        self.file_path_label.config(text=f"Selected File: {self.file_path}")

    def update_scales(self):
        for scale in self.image_to_sound_frame.winfo_children():
            scale.pack_forget()

        if self.conversion_mode.get() == 0:
            for scale in self.image_to_sound_frame.winfo_children():
                scale.pack(pady=2)

    def choose_file(self):
        self.file_path = filedialog.askopenfilename(title="Select File")
        if self.file_path:
            tk.messagebox.showinfo("File Selected", "File selected successfully!")
            self.update_file_path_label()

    def convert_file(self):
        # Check the mode of conversion
        mode = self.conversion_mode.get()

        # Update the scales based on the mode
        self.update_scales()

        # Check if a file is selected
        if not self.file_path:
            messagebox.showwarning("Warning", "Please select a file first!")
            return

        # Check the conversion mode and call the appropriate conversion method
        if mode == 0:  # Image to Sound
            if not self.file_path.endswith((".jpg", ".jpeg", ".png")):
                messagebox.showwarning("Warning", "Please select a valid image file!")
                return
            self.image_to_audio_conversion()
        elif mode == 1:  # Sound to Image
            if not self.file_path.endswith((".mp3", ".wav")):
                messagebox.showwarning("Warning", "Please select a valid audio file!")
                return
            self.audio_to_image_conversion()
        else:
            messagebox.showwarning("Warning", "Invalid conversion mode!")

    # ========================================================================================================

    def image_to_audio_conversion(self):
        if not self.file_path:
            messagebox.showwarning("Warning", "Please select an image file first!")
            return

        img = Image.open(self.file_path)

        # Convert image to RGB mode if it's not already in RGB mode
        if img.mode != "RGB":
            img = img.convert("RGB")

        width, height = img.size

        duration = min(5000, width * height)  # Duration of the audio (5 seconds or as long as the extracted pixels)

        audio = AudioSegment.silent(duration=duration)

        # Map slider values to audio properties
        volume = map_brightness_to_volume(self.brightness_var.get())
        frequency = map_hue_to_frequency(self.hue_var.get())
        saturation = self.saturation_var.get()

        for y in range(height):
            for x in range(width):
                pixel = img.getpixel((x, y))

                # Extract RGB components from the pixel
                r, g, b = pixel[:3]  # Take the first three components

                # Map color information to audio properties
                # Normalize to [0, 1]
                brightness = (r + g + b) / (255 * 3)
                hue = r / 255
                panning = (b / 255) * 2 - 1

                # Apply slider-adjusted values
                volume_adjusted = volume * brightness
                frequency_adjusted = frequency * hue
                panning_adjusted = panning * saturation

                sine_wave = Sine(freq=frequency_adjusted * 10000)
                sine_wave = sine_wave.to_audio_segment(duration=2000)  # Adjust duration

                # Overlay sine wave with adjusted volume and apply panning
                audio = audio.overlay(sine_wave - volume_adjusted).pan(panning_adjusted)

        audio.export("output.wav", format="wav")
        messagebox.showinfo("Conversion Complete", "Audio file generated successfully!")

    # ========================================================================================================

    def audio_to_image_conversion(self):
        audio = AudioSegment.from_file(self.file_path)

        audio_properties = extract_audio_properties(audio)

        # Use the current slider values for brightness, hue, saturation, and panning
        brightness = self.brightness_var.get()
        hue = self.hue_var.get()
        saturation = self.saturation_var.get()
        panning = self.panning_var.get()

        # Map brightness, hue, and panning to appropriate ranges
        brightness = map_volume_to_brightness(brightness)
        hue = map_frequency_to_hue(hue)
        panning = map_color_distribution_to_panning(panning)

        # Generate a unique color scheme based on the audio file's content
        hash_value = hashlib.md5(audio.raw_data).hexdigest()
        hash_as_int = int(hash_value, 16)
        hue = (hash_as_int % 360) / 360.0  # Map hash value to hue in [0, 1] range

        # Convert HSV to RGB
        rgb = hsv_to_rgb(hue, panning, brightness)

        # Create and save the image
        image = Image.new("RGB", (100, 100), rgb)
        image = image.filter(ImageFilter.BLUR)
        image.save("output.jpg")

        messagebox.showinfo("Conversion Complete", "Image file generated successfully!")

    def update_generated_output(self, mode):
        if mode == 0:  # Image to Sound
            self.image_to_audio_conversion()
        elif mode == 1:  # Sound to Image
            self.audio_to_image_conversion()

    # ========================================================================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = FileConverter(root)
    root.mainloop()
