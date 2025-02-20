# 🎬 YouTube Downloader GUI 🎶

## 📌 About This Project

This is a simple and user-friendly YouTube Downloader with a graphical interface built using `tkinter`. It utilizes `yt-dlp` to download videos or audio from YouTube and automatically converts them using `ffmpeg` when necessary.

> **⚠ Disclaimer:** This tool is intended for personal and educational purposes only. Downloading copyrighted content without permission may violate YouTube's Terms of Service and local copyright laws. Please use this tool responsibly.

> **🌐 Online Demo:** If you just want to see a demo, please check out this link: [YouTube Downloader GUI Demo](https://youtubedownloadergui.streamlit.app/). However, due to YouTube policies, we have implemented a system to disable audio downloads within videos. But if you run the same Streamlit file on your local system, everything will work perfectly.

## ✨ Features

✅ **Download Videos & Audio** - Choose between downloading videos in MP4 format or extracting audio as MP3.

✅ **Download Playlists** - Download entire YouTube playlists either as audio (MP3) or video (MP4).

✅ **Easy-to-Use Interface** - A graphical user interface (GUI) built with `tkinter` for seamless navigation.

✅ **Multi-threaded Processing** - Downloads happen in a separate thread to keep the GUI responsive.

✅ **Automatic File Management** - Downloads are saved to a chosen folder with appropriate file names.

✅ **Progress Updates & Logs** - The status area keeps you updated with download progress and potential issues.

## 🛠 Requirements

Before running this program, ensure you have the following installed:

### 1️⃣ Install Python
This program requires Python 3.x. If you don't have it installed, download it from:
[https://www.python.org/downloads/](https://www.python.org/downloads/)

### 2️⃣ Install Dependencies
To install the required Python packages, open a terminal or command prompt in the same directory as the `requirements.txt` file and run:

```bash
pip install -r requirements.txt
```

The dependencies include:
- `yt-dlp` - Handles the downloading of YouTube videos and audio.
- `streamlit` - Required for the alternate web-based version of the downloader.
- `ffmpeg` - Used for processing audio and video formats.

### 3️⃣ FFmpeg Installation (If Needed)
FFmpeg is required for converting videos and extracting audio. It is included with `yt-dlp`, but if you need to install it separately, follow these steps:

#### 📌 Windows
1. Download FFmpeg from: [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
2. Extract the contents and place it in a directory (e.g., `C:\ffmpeg\bin`).
3. Add `C:\ffmpeg\bin` to your system `PATH`.

#### 🍎 macOS
If you use Homebrew, install FFmpeg by running:
```bash
brew install ffmpeg
```

#### 🐧 Linux
For Ubuntu/Debian-based distributions:
```bash
sudo apt update && sudo apt install ffmpeg
```

For Fedora-based distributions:
```bash
sudo dnf install ffmpeg
```

To check if FFmpeg is installed, run:
```bash
ffmpeg -version
```

## 🚀 How to Run the Program

1. **Download the Script** - Ensure you have `youtube_downloader.py`.
2. **Open a Terminal/Command Prompt** in the script’s directory.
3. **Run the Script**:

```bash
python youtube_downloader.py
```
(or use `python3 youtube_downloader.py` if necessary)

4. **Use the GUI**:
   - Paste the YouTube video or playlist URL.
   - Select `Single` or `Playlist` mode.
   - Choose the format: `MP3` (Audio) or `MP4` (Video).
   - Click **Download** and monitor progress in the status area.

## 🗂 Where Are My Downloads Saved?
By default, all downloaded files are saved in a folder named **YouTubeDownloads** inside the program directory. You can select a different output folder from the GUI.

## ⚠ Troubleshooting

1. **FFmpeg not found?** Ensure it is installed and added to the system `PATH`.
2. **Slow Downloads?** YouTube may limit speeds. Try restarting your internet or use a VPN if needed.
3. **Error Messages?** Check the logs in the status area and ensure `yt-dlp` is updated:
   ```bash
   pip install -U yt-dlp
   ```

## 📜 License
This project is open-source and provided under the MIT License. Use it responsibly!

Enjoy downloading your favorite YouTube content responsibly! 🎥🎵

