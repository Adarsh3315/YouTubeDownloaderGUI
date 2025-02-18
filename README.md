# YouTube Downloader GUI

This is a simple Python-based graphical user interface (GUI) application that allows you to download videos and audio from YouTube. It uses the powerful `yt-dlp` library to handle the downloading process and `tkinter` for the user interface.

**Please note:** This program is intended for personal and educational use only. Downloading copyrighted material without permission may infringe copyright laws. Please use this tool responsibly and respect the terms of service of YouTube and copyright holders.

## Features

  * **Download YouTube Videos and Playlists**: You can download both single YouTube videos and entire playlists.
  * **Audio and Video Downloads**: Choose to download videos in MP4 format or just the audio in MP3 format.
  * **Four Download Options**:
      * **Playlist (Audio - MP3)**: Downloads an entire YouTube playlist as MP3 audio files.
      * **Playlist (Video - MP4)**: Downloads an entire YouTube playlist as MP4 video files.
      * **Single (Audio - MP3)**: Downloads a single YouTube video as an MP3 audio file.
      * **Single (Video - MP4)**: Downloads a single YouTube video as an MP4 video file.
  * **User-Friendly GUI**:  Easy to use interface with a text area to show the download status.
  * **Download Status Updates**:  Real-time status messages are displayed in the GUI to keep you informed about the download process.
  * **Safe and Threaded Download**: Downloads are performed in a separate thread, ensuring the GUI remains responsive even during downloads.
  * **Automatic Output Folder**: Downloads are automatically saved in a "Downloads" folder created in the same directory as the script.

## Prerequisites

Before running this program, you need to have the following installed on your system:

1.  **Python**: You need Python 3.x installed on your computer. If you don't have it, you can download it from the official Python website: [https://www.python.org/downloads/](https://www.google.com/url?sa=E&source=gmail&q=https://www.python.org/downloads/)

2.  **Required Python Libraries**: You need to install the following Python libraries. You can install them using `pip`, the Python package installer. Open your terminal or command prompt and run the following commands:

    ```bash
    pip install tkinter  # You might already have this as it's often included with Python
    pip install yt-dlp
    ```

      * **`tkinter`**: This library is used for creating the graphical user interface. It's often included in standard Python installations, but if you encounter issues, you can try to install it.
      * **`yt-dlp`**: This is the main library that handles the actual YouTube downloading. It's a powerful and actively maintained fork of `youtube-dl`.

3.  **FFmpeg**: FFmpeg is required for post-processing tasks, specifically for converting videos to MP4 and extracting audio to MP3. You need to have FFmpeg installed and properly configured on your system.

      * **Why is FFmpeg needed?**:

          * **MP3 Conversion**: To download audio as MP3, the program extracts audio from the video and converts it to MP3 format using FFmpeg.
          * **MP4 Conversion (Sometimes)**: While `yt-dlp` tries to download videos directly in MP4 format, sometimes it might download in other formats and then use FFmpeg to convert them to MP4 to ensure compatibility.

      * **How to install FFmpeg**:
        The installation process for FFmpeg varies depending on your operating system:

          * **For Windows**:

            1.  Go to the FFmpeg website or a reliable source like [https://www.ffmpeg.org/download.html](https://www.google.com/url?sa=E&source=gmail&q=https://www.ffmpeg.org/download.html) to download FFmpeg binaries for Windows.
            2.  Download the `ffmpeg` release for Windows (usually a `.zip` file).
            3.  Extract the contents of the `.zip` file to a directory (e.g., `C:\ffmpeg`).
            4.  **Add FFmpeg to your system's PATH environment variable**: This is crucial so that the program can find FFmpeg.
                  * Search for "Environment Variables" in the Windows Start Menu and open "Edit the system environment variables".
                  * Click on "Environment Variables...".
                  * Under "System variables", find "Path" and select it, then click "Edit...".
                  * Click "New" and add the path to the `bin` directory inside your FFmpeg extraction folder (e.g., `C:\ffmpeg\bin`).
                  * Click "OK" on all dialogs to save changes.
            5.  Restart your command prompt or terminal for the changes to take effect.

         
        **After installation, verify FFmpeg is installed correctly.** Open your terminal or command prompt and type:

        ```bash
        ffmpeg -version
        ```

        If FFmpeg is correctly installed and in your PATH, it will display version information. If you get an error like "ffmpeg is not recognized...", double-check your PATH settings and FFmpeg installation.

## How to Run the Program

1.  **Save the Python script**: Save the provided Python code as a `.py` file (e.g., `youtube_downloader.py`).

2.  **Open a terminal or command prompt**: Navigate to the directory where you saved the `.py` file.

3.  **Run the script**: Execute the script using Python by running the following command in your terminal/command prompt:

    ```bash
    python youtube_downloader.py
    ```

    (or `python3 youtube_downloader.py` if `python` refers to Python 2 on your system).

4.  **Using the GUI**:

      * A window titled "YouTube Downloader" will appear.
      * **Enter YouTube URL**: In the "YouTube URL / Playlist URL" field, paste the URL of the YouTube video or playlist you want to download.
      * **Select Download Option**: Choose your desired download option from the "Download Options" frame by clicking on one of the radio buttons:
          * Playlist (Audio - MP3)
          * Playlist (Video - MP4)
          * Single (Audio - MP3)
          * Single (Video - MP4)
      * **Click "Download"**: Press the "Download" button to start the download process.
      * **Status Updates**: The "Status" text area at the bottom will display messages indicating the download progress and any errors.
      * **Downloads Folder**: Once the download is complete (or if you downloaded successfully previously), you will find your downloaded files in a folder named "Downloads" which is created in the same directory as the script.

## Disclaimer

This program is provided for educational purposes only. Downloading copyrighted content without proper authorization may violate copyright laws and the terms of service of YouTube. Please use this tool responsibly and ensure you have the right to download the content you are accessing. The developers are not responsible for any misuse of this program.

**Use this software at your own risk.**

-----

Enjoy downloading your favorite YouTube content responsibly\!
