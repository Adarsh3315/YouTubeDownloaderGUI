import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import yt_dlp
import threading

class TkdLogger:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def debug(self, msg):
        self.log_message("DEBUG: " + msg)

    def info(self, msg):
        self.log_message("INFO: " + msg)

    def warning(self, msg):
        self.log_message("WARNING: " + msg)

    def error(self, msg):
        self.log_message("ERROR: " + msg)

    def log_message(self, msg):
        def append():
            self.text_widget.insert(tk.END, msg + "\n")
            self.text_widget.see(tk.END)
        self.text_widget.after(0, append)

def download_task(url, mode, file_format, output_folder, text_widget):
    logger = TkdLogger(text_widget)

    def progress_hook(d):
        if d['status'] == 'finished':
            logger.info('Download finished, now post-processing...')
        elif d['status'] == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate')
            downloaded = d.get('downloaded_bytes', 0)
            if total:
                percentage = downloaded / total * 100
                logger.info(f"Downloading... {percentage:.1f}%")
    
    os.makedirs(output_folder, exist_ok=True)
    outtmpl = os.path.join(output_folder, '%(title)s.%(ext)s')
    
    ydl_opts = {
        'ignoreerrors': True,
        'logger': logger,
        'progress_hooks': [progress_hook],
    }

    if mode == "playlist":
        if file_format == "MP3":
            ydl_opts.update({
                'format': 'bestaudio/best',
                'outtmpl': outtmpl,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            })
        elif file_format == "MP4":
            ydl_opts.update({
                'format': 'bestvideo[ext=mp4]+bestaudio/best',
                'outtmpl': outtmpl,
                'merge_output_format': 'mp4',
            })
        else:
            logger.error("Invalid playlist format selected.")
            return
    elif mode == "single":
        if file_format == "Audio":
            ydl_opts.update({
                'format': 'bestaudio/best',
                'outtmpl': outtmpl,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            })
        elif file_format == "Video":
            ydl_opts.update({
                'format': 'bestvideo[ext=mp4]+bestaudio/best',
                'outtmpl': outtmpl,
                'merge_output_format': 'mp4',
            })
        else:
            logger.error("Invalid single file format selected.")
            return
    else:
        logger.error("Invalid mode selected.")
        return
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            logger.info("Starting download...")
            ydl.download([url])
            logger.info("Download completed.")
    except Exception as e:
        logger.error(f"Error: {str(e)}")

def start_download(url_entry, mode_var, playlist_format_var, single_format_var, output_folder_entry, log_text):
    url = url_entry.get().strip()
    if not url:
        messagebox.showerror("Error", "Please enter a YouTube URL.")
        return
    
    mode = mode_var.get()  # "playlist" or "single"
    if mode == "playlist":
        file_format = playlist_format_var.get()  
    else:
        file_format = single_format_var.get()  
    
    output_folder = output_folder_entry.get().strip() or "YouTubeDownloads"
    
    log_text.delete("1.0", tk.END)
    
    thread = threading.Thread(target=download_task, args=(url, mode, file_format, output_folder, log_text))
    thread.start()

def choose_folder(output_folder_entry):
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        output_folder_entry.delete(0, tk.END)
        output_folder_entry.insert(0, folder_selected)

def update_format_options(mode_var, playlist_frame, single_frame):
    mode = mode_var.get()
    if mode == "playlist":
        playlist_frame.grid()      
        single_frame.grid_remove()
    else:
        single_frame.grid()        
        playlist_frame.grid_remove() 

def create_gui():
    root = tk.Tk()
    root.title("YouTube Downloader GUI")
    root.geometry("600x500")
    
    url_label = ttk.Label(root, text="YouTube URL :")
    url_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    
    url_entry = ttk.Entry(root, width=70)
    url_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")
    
    mode_var = tk.StringVar(value="playlist")
    mode_label = ttk.Label(root, text="Download Mode:")
    mode_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    
    mode_frame = ttk.Frame(root)
    mode_frame.grid(row=1, column=1, padx=10, pady=10, sticky="w")
    
    playlist_rb = ttk.Radiobutton(
        mode_frame, text="Playlist", variable=mode_var, value="playlist",
        command=lambda: update_format_options(mode_var, playlist_frame, single_frame))
    playlist_rb.grid(row=0, column=0, padx=5)
    
    single_rb = ttk.Radiobutton(
        mode_frame, text="Single", variable=mode_var, value="single",
        command=lambda: update_format_options(mode_var, playlist_frame, single_frame))
    single_rb.grid(row=0, column=1, padx=5)
    
    playlist_frame = ttk.LabelFrame(root, text="Playlist Format")
    playlist_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="w")
    
    playlist_format_var = tk.StringVar(value="MP3")
    mp3_rb = ttk.Radiobutton(playlist_frame, text="MP3", variable=playlist_format_var, value="MP3")
    mp3_rb.grid(row=0, column=0, padx=5, pady=5)
    mp4_rb = ttk.Radiobutton(playlist_frame, text="MP4", variable=playlist_format_var, value="MP4")
    mp4_rb.grid(row=0, column=1, padx=5, pady=5)
    
    single_frame = ttk.LabelFrame(root, text="Single File Format")
    single_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="w")
    
    single_format_var = tk.StringVar(value="Audio")
    audio_rb = ttk.Radiobutton(single_frame, text="Audio", variable=single_format_var, value="Audio")
    audio_rb.grid(row=0, column=0, padx=5, pady=5)
    video_rb = ttk.Radiobutton(single_frame, text="Video", variable=single_format_var, value="Video")
    video_rb.grid(row=0, column=1, padx=5, pady=5)
    
    if mode_var.get() == "playlist":
        single_frame.grid_remove()
    else:
        playlist_frame.grid_remove()
    
    output_folder_label = ttk.Label(root, text="Output Folder:")
    output_folder_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")
    
    output_folder_entry = ttk.Entry(root, width=50)
    output_folder_entry.grid(row=4, column=1, padx=10, pady=10, sticky="w")
    output_folder_entry.insert(0, os.path.join(os.getcwd(), "YouTubeDownloads"))
    
    browse_button = ttk.Button(root, text="Browse", command=lambda: choose_folder(output_folder_entry))
    browse_button.grid(row=4, column=2, padx=10, pady=10)
    
    download_button = ttk.Button(
        root, text="Download",
        command=lambda: start_download(url_entry, mode_var, playlist_format_var, single_format_var, output_folder_entry, log_text))
    download_button.grid(row=5, column=0, columnspan=3, padx=10, pady=10)
    
    log_text = tk.Text(root, wrap="word", height=15)
    log_text.grid(row=6, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
    
    root.grid_rowconfigure(6, weight=1)
    root.grid_columnconfigure(1, weight=1)
    
    root.mainloop()

if __name__ == "__main__":
    create_gui()