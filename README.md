# audiovisual_interconversion_system
A system that allows the interconversion of audio and visual files using a UI, with adjustment parameters for image and audio properties.

## How to use the program
1. Clone the repository
```bash
git clone <project-url>
```
2. Install the required libraries using the following command:
```bash
pip install -r requirements.txt
```
<br>

The program is now ready to use. Run the following command to start the UI:
```bash
python app.py
```

The UI will open, allowing you to choose the conversion direction, input file, and adjust parameters. After selecting the desired options, click the "Convert" button to start the conversion process.

## System Design and Architecture
### System Blueprint:
The system is designed to interconvert visual and audio files through a user interface. It supports two main tasks:
- Image to Audio Conversion
- Audio to Image Conversion

The architecture consists of three main components:
- Image Processing Module
- Audio Processing Module, and
- A User Interface to initiate the process.

### Image Processing Module:
- Utilizes the Pillow library for scanning images pixel by pixel.
- Extracts properties such as brightness, hue, and saturation from the image.
- Translates these properties into corresponding audio parameters, including volume, frequency, and overtones.

### Audio Processing Module:
- Employs Pydub to generate audio files based on translated parameters.
- Supports reverse processing, extracting properties from audio files.
- Translates audio parameters back into visual properties for image creation.

### User Interface:
- Developed using Tkinter for a user-friendly experience.
- Offers sliders and input fields for parameter adjustment in both tasks.
- Allows users to select the conversion direction (visual to audio or audio to visual).
- Provides options to choose input files and adjust conversion parameters.

## Data Flow Diagram:
```sql
              +-------------------+
              |   User Interface  |
              +---------+---------+
                        |
                        v
              +---------+---------+
              | Image Processing  |  <--(Task 1)
              |     Module        |  --- Extracts properties from images
              +---------+---------+
                        |
                        v
              +---------+---------+
              | Audio Processing  |  <--(Task 2)
              |     Module        |  --- Extracts properties from audio
              +---------+---------+
                        |
                        v
              +-------------------+
              |   File Conversion  |
              +-------------------+
```

## User Interface Design:
### Main Interface:
- Dropdown or radio buttons to select conversion direction (visual to audio or audio to visual).
- Input field/button for selecting the input file (image for Task 1, audio for Task 2).

### Parameter Adjustment:
- Sliders for adjusting brightness, hue, saturation, volume, frequency, and overtones.
- Input fields for precise parameter input.

### Conversion Action:
- Button to initiate the conversion process.
- Display area for status updates and notifications.
