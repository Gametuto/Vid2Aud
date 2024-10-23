import subprocess
import os
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
from rich.panel import Panel
import inquirer

console = Console()

def get_ffmpeg_path():
    ffmpeg_path = os.path.join(os.path.dirname(__file__), 'ffmpeg.exe')
    if os.path.exists(ffmpeg_path):
        return ffmpeg_path
    return 'ffmpeg'  # Assume ffmpeg is in the system PATH

def video_to_audio(video_path, audio_path, codec, format_choice):
    ffmpeg_path = get_ffmpeg_path()
    command = [
        ffmpeg_path,
        '-i', video_path,
        '-vn',  # No video
        '-acodec', codec,  # Use the selected codec
    ]
    # Add '-strict -2' for experimental codecs
    if codec in ['libfdk_aac', 'libshine', 'libtwolame']:
        command.extend(['-strict', '-2'])
    command.append(audio_path)
    result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
    if result.returncode != 0:
        raise subprocess.CalledProcessError(result.returncode, command, output=result.stdout, stderr=result.stderr)

def process_file(filename, input_folder, output_folder, codec, extension, progress, task):
    video_path = os.path.join(input_folder, filename)
    audio_filename = os.path.splitext(filename)[0] + f".{extension}"
    audio_path = os.path.join(output_folder, audio_filename)
    try:
        video_to_audio(video_path, audio_path, codec, extension)
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Error processing file {filename}: {e.stderr}[/red]")
    progress.update(task, advance=1)

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

def print_success_message():
    success_message = r"""
   _____                               
  / ___/__  _______________  __________
  \__ \/ / / / ___/ ___/ _ \/ ___/ ___/
 ___/ / /_/ / /__/ /__/  __(__  |__  ) 
/____/\__,_/\___/\___/____/____/____/  
    """
    console.print(Panel(success_message, style="bold green"))

def print_no_files_message():
    no_files_message = r"""
There are no video files in the "videoInput" folder.
Stopping the script.
    """
    console.print(Panel(no_files_message, style="bold red"))

def print_ffmpeg_not_found_message():
    ffmpeg_not_found_message = r"""
FFmpeg executable not found in the project directory or system PATH.
Please ensure ffmpeg is available.
Stopping the script.
    """
    console.print(Panel(ffmpeg_not_found_message, style="bold red"))

if __name__ == "__main__":
    input_folder = "videoInput"
    output_folder = "audioOutput"

    # Create input and output folders if they don't exist
    os.makedirs(input_folder, exist_ok=True)
    os.makedirs(output_folder, exist_ok=True)

    # Check if ffmpeg is in the project directory or system PATH
    ffmpeg_path = get_ffmpeg_path()
    if ffmpeg_path == 'ffmpeg' and not shutil.which('ffmpeg'):
        print_ffmpeg_not_found_message()
        exit(1)

    # Define the list of video file extensions to process
    video_extensions = [
        ".webm", ".mp4", ".avi", ".mkv", ".mov", ".flv", ".wmv", ".mpeg", ".mpg", ".m4v", ".3gp", ".3g2",
        ".mxf", ".ogv", ".ts", ".vob", ".mts", ".m2ts", ".divx", ".f4v", ".rm", ".rmvb", ".asf", ".amv",
        ".svi", ".m2v", ".mpe", ".mpv", ".m1v", ".m2p", ".m2t", ".tod", ".vro", ".mvi", ".qt", ".yuv",
        ".bik", ".drc", ".fli", ".flc", ".f4p", ".f4a", ".f4b"
    ]

    # List all video files in the input folder with the specified extensions
    files = [f for f in os.listdir(input_folder) if any(f.endswith(ext) for ext in video_extensions)]

    # Check if there are no video files
    if not files:
        print_no_files_message()
        exit(1)

    # Print starter message
    print_starter_message()

    # Define the list of audio file extensions to choose from
    audio_extensions = [
        'mp3', 'ogg', 'wav', 'flac', 'aac', 'm4a', 'wma', 'opus', 'aiff', 'ac3', 'eac3', 'mp2'
    ]

    # Ask the user for the desired audio format
    questions = [
        inquirer.List('format',
                      message="Choose the audio format",
                      choices=audio_extensions,
                      ),
    ]
    answers = inquirer.prompt(questions)
    format_choice = answers['format']

    # Map the chosen format to the appropriate codec
    codec_map = {
        'mp3': 'libmp3lame',
        'ogg': 'libvorbis',
        'wav': 'pcm_s16le',
        'flac': 'flac',
        'aac': 'aac',
        'm4a': 'aac',
        'wma': 'wmav2',
        'opus': 'libopus',
        'aiff': 'pcm_s16be',
        'ac3': 'ac3',
        'eac3': 'eac3',
        'mp2': 'mp2'
    }
    codec = codec_map[format_choice]

    # Create a rich progress bar
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeRemainingColumn(),
    ) as progress:
        task = progress.add_task("[cyan]Converting files...", total=len(files))
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(process_file, filename, input_folder, output_folder, codec, format_choice, progress, task) for filename in files]
            for future in as_completed(futures):
                pass

    # Print success message
    print_success_message()