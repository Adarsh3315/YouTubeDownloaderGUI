import streamlit as st
import yt_dlp
import os
import glob
import concurrent.futures
import time
import shutil
from datetime import datetime, timedelta

MAX_FILE_AGE_MINUTES = 30
TEMP_FOLDER_PREFIX = "yt_dl_"

class STATE:
    PROGRESS = "download_progress"
    LOGS = "download_logs"
    ACTIVE = "download_active"
    FOLDER = "download_folder"
    COUNT = "item_count"
    CURRENT = "current_item"

def setup_session_state():
    defaults = {
        STATE.PROGRESS: 0,
        STATE.LOGS: [],
        STATE.ACTIVE: False,
        STATE.FOLDER: None,
        STATE.COUNT: 1,
        STATE.CURRENT: 0
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def cleanup_old_downloads():
    now = time.time()
    for folder in glob.glob(TEMP_FOLDER_PREFIX + "*"):
        if os.path.isdir(folder) and (now - os.path.getmtime(folder)) > (MAX_FILE_AGE_MINUTES * 60):
            try:
                shutil.rmtree(folder)
            except Exception as e:
                st.error(f"Cleanup error: {str(e)}")

def create_temp_folder():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{TEMP_FOLDER_PREFIX}{timestamp}"

def get_base_options(file_format):
    file_format = file_format or "Video"
    folder = st.session_state.get(STATE.FOLDER)
    if not folder:
        folder = create_temp_folder()
        st.session_state[STATE.FOLDER] = folder
        os.makedirs(folder, exist_ok=True)
    base_opts = {
        "outtmpl": os.path.join(folder, "%(title)s.%(ext)s"),
        "ignoreerrors": True,
        "verbose": False,
        "concurrent_fragment_downloads": 4,
        "noprogress": False,
        "retries": 3
    }
    if file_format == "Audio":
        base_opts.update({
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }]
        })
    else:
        base_opts.update({
            "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "merge_output_format": "mp4",
            "postprocessors": [{
                "key": "FFmpegVideoRemuxer",
                "when": "post_process"
            }]
        })
    return base_opts

def progress_hook(d):
    if d["status"] == "downloading":
        if d.get("total_bytes"):
            percent = d["downloaded_bytes"] / d["total_bytes"] * 100
            st.session_state[STATE.PROGRESS] = percent
            st.session_state[STATE.LOGS].append(f"Progress: {percent:.1f}%")
    elif d["status"] == "finished":
        st.session_state[STATE.CURRENT] += 1
        st.session_state[STATE.LOGS].append("Post-processing file...")

def download_item(url):
    try:
        file_format = st.session_state.get("file_format") or "Video"
        ydl_opts = get_base_options(file_format)
        ydl_opts["progress_hooks"] = [progress_hook]
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        st.session_state[STATE.LOGS].append(f"ERROR: {str(e)}")
        st.session_state[STATE.ACTIVE] = False

def start_download():
    st.session_state[STATE.ACTIVE] = True
    if st.session_state[STATE.FOLDER] and os.path.exists(st.session_state[STATE.FOLDER]):
        try:
            shutil.rmtree(st.session_state[STATE.FOLDER])
        except Exception:
            pass
    st.session_state[STATE.FOLDER] = create_temp_folder()
    os.makedirs(st.session_state[STATE.FOLDER], exist_ok=True)
    
    if st.session_state.mode == "Single":
        download_item(st.session_state.url)
    else:
        try:
            with yt_dlp.YoutubeDL({"simulate": True}) as ydl:
                info = ydl.extract_info(st.session_state.url, download=False)
            entries = info.get("entries", [])
            urls = [e["webpage_url"] for e in entries if e]
            st.session_state[STATE.COUNT] = len(urls)
            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                futures = [executor.submit(download_item, url) for url in urls]
                for future in concurrent.futures.as_completed(futures):
                    future.result()
        except Exception as e:
            st.session_state[STATE.LOGS].append(f"Playlist error: {str(e)}")
    st.session_state[STATE.ACTIVE] = False

def ui_download_controls():
    col1, col2 = st.columns([1, 2])
    with col1:
        st.session_state.url = st.text_input("YouTube URL", key="url_input")
    with col2:
        st.session_state.mode = st.radio("Mode", ("Single", "Playlist"), horizontal=True, key="mode_radio")
    st.session_state.file_format = st.radio("Format", ("Video", "Audio"), horizontal=True, key="format_radio")
    if st.button("Start Download", disabled=st.session_state[STATE.ACTIVE]):
        if not st.session_state.url:
            st.error("Please enter a URL :")
        else:
            start_download()

def ui_live_status():
    with st.sidebar:
        st.header("Download Status")
        st.code("\n".join(st.session_state[STATE.LOGS][-10:]))

def ui_progress_display():
    if st.session_state[STATE.ACTIVE]:
        progress = st.session_state[STATE.PROGRESS]
        current = st.session_state[STATE.CURRENT]
        total = st.session_state[STATE.COUNT]
        st.progress(progress / 100, text=f"Downloading item {current+1}/{total}")
        time.sleep(0.1)
        st.rerun()

def ui_download_results():
    if not st.session_state[STATE.ACTIVE] and st.session_state[STATE.FOLDER]:
        files = glob.glob(os.path.join(st.session_state[STATE.FOLDER], "*"))
        if files:
            st.success(f"Downloaded {len(files)} files")
            for path in files:
                with open(path, "rb") as f:
                    st.download_button(
                        label=f"Download {os.path.basename(path)}",
                        data=f,
                        file_name=os.path.basename(path),
                        mime="video/mp4" if st.session_state.file_format == "Video" else "audio/mpeg"
                    )
            try:
                shutil.rmtree(st.session_state[STATE.FOLDER])
            except Exception as e:
                st.error(f"Cleanup error: {str(e)}")

def main():
    st.set_page_config(page_title="YouTube Downloader GUI", layout="centered")
    setup_session_state()
    cleanup_old_downloads()
    st.title("YouTube Downloader GUI")
    st.caption("For educational purposes only - Respect copyright laws")
    ui_download_controls()
    ui_live_status() 
    ui_progress_display()
    ui_download_results()

if __name__ == "__main__":
    main()
