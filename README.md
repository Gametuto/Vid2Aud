# Vid2Aud

This project is a Python-based tool that converts video files to audio files using the FFmpeg library. It supports multiple audio codecs and formats, and provides a user-friendly command-line interface with progress tracking.

## Features

- [x] Convert video files to audio files
- [x] Support for multiple audio codecs (e.g., `libfdk_aac`, `libshine`, `libtwolame`)
- [x] Progress tracking with rich console output
- [x] Error handling and informative messages
- [x] Multi-threaded processing for faster conversion
- [ ] Choose a specific audio codec

## Requirements

- Python 3.6+
- FFmpeg executable (`ffmpeg.exe`)
- Required Python packages: `rich`, `inquirer`

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/Video-To-Audio-Converter.git
    cd Vid2Aud
    ```

2. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

3. Download and install FFmpeg:
    - Go to the [FFmpeg download page](https://ffmpeg.org/download.html).
    - Download the appropriate version for your operating system.
    - Extract the downloaded archive.
    - Copy the `ffmpeg.exe` executable to the project directory or add its location to your system's PATH.

## Usage

1. Place your video files in the `videoInput` folder.

2. Run the script:
    ```sh
    python Vid2Aud.py
    ```

3. Follow the prompts to select the audio ~~codec and~~ format.

4. The converted audio files will be saved in the `audioOutput` folder.

## Code Overview

### Main Functions

- `video_to_audio(video_path, audio_path, codec, format_choice)`: Converts a video file to an audio file using the specified codec and format.
- `process_file(filename, input_folder, output_folder, codec, extension, progress, task)`: Processes a single video file and converts it to audio.
- `print_starter_message()`: Prints an ASCII starter message when the script begins.
- `print_success_message()`: Prints an ASCII success message when the script completes.
- `print_no_files_message()`: Prints an ASCII message if no video files are found in the input folder.

### Example Code Excerpts

#### `video_to_audio` Function
```py
def video_to_audio(video_path, audio_path, codec, format_choice):
    ffmpeg_path = os.path.join(os.path.dirname(__file__), 'ffmpeg.exe')
    command = [
        ffmpeg_path,
        '-i', video_path,
        '-vn',  # No video
        '-acodec', codec,  # Use the selected codec
    ]
    if codec in ['libfdk_aac', 'libshine', 'libtwolame']:
        command.extend(['-strict', '-2'])
    command.append(audio_path)
    result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
    if result.returncode != 0:
        raise subprocess.CalledProcessError(result.returncode, command, output=result.stdout, stderr=result.stderr)
```

#### `print_starter_message` Function
```py
def print_starter_message():
    starter_message = r"""
   ________                                         __              __     ____                           __ 
  / ____/ /_  ____  ____  ________     ____  __  __/ /_____  __  __/ /_   / __/___  _________ ___  ____ _/ /_
 / /   / __ \/ __ \/ __ \/ ___/ _ \   / __ \/ / / / __/ __ \/ / / / __/  / /_/ __ \/ ___/ __ `__ \/ __ `/ __/
/ /___/ / / / /_/ / /_/ (__  )  __/  / /_/ / /_/ / /_/ /_/ / /_/ / /_   / __/ /_/ / /  / / / / / / /_/ / /_  
\____/_/ /_/\____/\____/____/\___/   \____/\__,_/\__/ .___/\__,_/\__/  /_/  \____/_/  /_/ /_/ /_/\__,_/\__/  
                                                   /_/                                                       
    """
    console.print(Panel(starter_message, style="bold green"))
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Contact

For any questions or suggestions, please contact [gametutoytb@gmail.com](mailto:gametutoytb@gmail.com).
