import streamlit as st
import yt_dlp
import os
import glob

# WARNING: This script is for educational purposes only.
# Please ensure you have the right to download content.

def download_youtube(url, mode, file_format, output_folder):
    logs = []

    # Simple logger for Streamlit
    class StreamlitLogger:
        def debug(self, msg):
            logs.append(f"DEBUG: {msg}")
        def info(self, msg):
            logs.append(f"INFO: {msg}")
        def warning(self, msg):
            logs.append(f"WARNING: {msg}")
        def error(self, msg):
            logs.append(f"ERROR: {msg}")

    logger = StreamlitLogger()

    def progress_hook(d):
        if d["status"] == "finished":
            logger.info("Download finished, now post-processing...")
        elif d["status"] == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate")
            downloaded = d.get("downloaded_bytes", 0)
            if total:
                percent = downloaded / total * 100
                logger.info(f"Downloading... {percent:.1f}%")

    os.makedirs(output_folder, exist_ok=True)
    outtmpl = os.path.join(output_folder, "%(title)s.%(ext)s")

    if mode == "playlist":
        if file_format == "MP3":
            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": outtmpl,
                "ignoreerrors": True,
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }
                ],
                "logger": logger,
                "progress_hooks": [progress_hook],
            }
        else:  # MP4
            ydl_opts = {
                # Merge best audio + best video
                "format": "bestvideo+bestaudio/best",
                "outtmpl": outtmpl,
                "ignoreerrors": True,
                "logger": logger,
                "progress_hooks": [progress_hook],
                # Remux final output into MP4
                "postprocessors": [
                    {
                        "key": "FFmpegVideoRemuxer",
                        "preferredformat": "mp4"
                    }
                ],
            }
    else:  # single download
        if file_format == "Audio":
            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": outtmpl,
                "ignoreerrors": True,
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }
                ],
                "logger": logger,
                "progress_hooks": [progress_hook],
            }
        else:  # Video
            ydl_opts = {
                # Merge best audio + best video
                "format": "bestvideo+bestaudio/best",
                "outtmpl": outtmpl,
                "ignoreerrors": True,
                "logger": logger,
                "progress_hooks": [progress_hook],
                # Remux final output into MP4
                "postprocessors": [
                    {
                        "key": "FFmpegVideoRemuxer",
                        "preferredformat": "mp4"
                    }
                ],
            }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            logger.info("Starting download...")
            ydl.download([url])
            logger.info("Download completed.")
    except Exception as e:
        logger.error(f"Error: {str(e)}")

    return logs

def main():
    st.title("YouTube Downloader (Streamlit Version)")
    st.warning("This application is for educational purposes only. Only download if you have the rights to the content.")

    url = st.text_input("YouTube URL")
    mode = st.radio("Download Mode", ("playlist", "single"))
    if mode == "playlist":
        file_format = st.radio("Playlist Format", ("MP3", "MP4"))
    else:
        file_format = st.radio("Single File Format", ("Audio", "Video"))

    output_folder = st.text_input("Output Folder", "YouTubeDownloads")

    if st.button("Download"):
        if not url:
            st.error("Please enter a YouTube URL.")
        else:
            with st.spinner("Downloading..."):
                logs = download_youtube(url, mode, file_format, output_folder)
            st.write("\n".join(logs))

            # Provide download buttons for new files
            downloaded_files = glob.glob(os.path.join(output_folder, "*"))
            for file_path in downloaded_files:
                file_name = os.path.basename(file_path)
                with open(file_path, "rb") as f:
                    st.download_button(
                        f"Download {file_name}",
                        data=f,
                        file_name=file_name,
                        mime="application/octet-stream",
                    )

if __name__ == "__main__":
    main()
