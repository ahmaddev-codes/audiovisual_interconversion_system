import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
from pydub import AudioSegment
from pydub.generators import Sine
from modules.map import *
from modules.hsv_to_rgb import *

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
            tk.Scale(self.sound_to_image_frame, label=label, variable=var, from_=from_, to=to, resolution=resolution,
                    orient="horizontal", length=300).pack(pady=2)

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

    def extract_audio_texture(self, samples):
        diff = sum(abs(samples[i] - samples[i-1]) for i in range(1, len(samples)))
        return diff / (len(samples) - 1) if len(samples) > 1 else 0

    def extract_panning(self, samples):
        left_channel = samples[::2]
        right_channel = samples[1::2]
        panning = sum(right_channel) / sum(left_channel) if sum(left_channel) != 0 else 0
        return max(-1.0, min(panning, 1.0))

    def extract_audio_properties(self, audio):
        samples = audio.get_array_of_samples()

        rms_amplitude = sum(x ** 2 for x in samples) / len(samples)
        volume = rms_amplitude / (2**15)

        frequencies = [i * audio.frame_rate / len(samples) for i in range(len(samples))]
        spectral_centroid = sum(frequencies[i] * samples[i] for i in range(len(samples))) / sum(samples)
        frequency = spectral_centroid / (audio.frame_rate / 2)

        audio_texture = self.extract_audio_texture(samples)
        panning = self.extract_panning(samples)

        return {'volume': volume, 'frequency': frequency, 'audio_texture': audio_texture, 'panning': panning}

    def convert_file(self):
        if not self.file_path:
            messagebox.showwarning("Warning", "Please select a file first!")
            return

        if self.conversion_mode.get() == 0:
            self.image_to_audio_conversion()
        elif self.conversion_mode.get() == 1:
            self.audio_to_image_conversion()
        else:
            messagebox.showwarning("Warning", "Invalid conversion mode!")

    def image_to_audio_conversion(self):
        if not self.file_path:
            messagebox.showwarning("Warning", "Please select a file first!")
            return

        # Map slider values directly to audio properties
        volume = map_brightness_to_volume(self.brightness_var.get())
        frequency = map_hue_to_frequency(self.hue_var.get())
        saturation = self.saturation_var.get()

        audio_texture = map_saturation_to_audio_property(saturation)
        panning = map_panning_to_color_distribution(self.panning_var.get())
        panning = max(-1.0, min(panning, 1.0))

        sine_wave = Sine(freq=frequency)
        sine_wave = sine_wave.to_audio_segment(duration=2000)

        audio = (
            AudioSegment.silent(duration=500)
            .overlay(sine_wave - volume)
            .pan(panning)
            .fade_in(100)
            .fade_out(100)
        )

        audio = audio.set_sample_width(2)
        audio = audio.set_frame_rate(44100)
        audio = audio + 10

        output_path = 'output_audio.mp3'
        audio.export(output_path, format='mp3')
        messagebox.showinfo("Audio Generated", f"Audio file generated: {output_path}")

    def audio_to_image_conversion(self):
        if not self.file_path:
            messagebox.showwarning("Warning", "Please select a file first!")
            return

        # Map slider values directly to image properties
        brightness = map_volume_to_brightness(self.volume_var.get())
        hue = map_frequency_to_hue(self.frequency_var.get())
        saturation = map_audio_property_to_saturation(self.audio_texture_var.get())
        panning = map_color_distribution_to_panning(self.panning_var.get())

        print(f"Brightness: {brightness}, Hue: {hue}, Saturation: {saturation}, Panning: {panning}")

        brightness = max(0, min(brightness, 1.0))
        hue = max(0, min(hue, 1.0))
        saturation = max(0, min(saturation, 1.0))

        brightness = min(brightness + 0.2, 1.0)
        hue = min(hue + 0.2, 1.0)
        saturation = min(saturation + 0.2, 1.0)

        rgb_color = hsv_to_rgb(hue, saturation, brightness)

        print(f"RGB Color: {rgb_color}")

        image_size = 200
        image = Image.new('RGB', (image_size, image_size), rgb_color)

        output_path = 'output_image.png'
        image.save(output_path)
        messagebox.showinfo("Image Generated", f"Image file generated: {output_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileConverter(root)
    root.mainloop()
