import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
from pathlib import Path
import yt_dlp
import re

class YouTubeDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hello youtube ")
        self.root.geometry("700x600")
        self.root.configure(bg='#2c3e50')
        
        # Set window icon (you can replace this with your own icon file)
        try:
            self.root.iconbitmap('icon.ico')  # Add your icon file here
        except:
            pass
        
        self.download_path = Path("./Downloads")
        self.download_path.mkdir(exist_ok=True)
        
        self.available_formats = []
        self.setup_ui()
        
    def create_logo(self, parent):
        """Create a custom logo using text and styling"""
        logo_frame = tk.Frame(parent, bg='#2c3e50')
        logo_frame.pack(pady=10)
        
        # Main title
        title_label = tk.Label(logo_frame, text="Hello Youtube ", 
                              font=('Arial', 20, 'bold'), 
                              fg='#e74c3c', bg='#2c3e50')
        title_label.pack()
        
        # Subtitle
        subtitle_label = tk.Label(logo_frame, text="Fast • Organized • High Quality", 
                                 font=('Arial', 10), 
                                 fg='#95a5a6', bg='#2c3e50')
        subtitle_label.pack()
        
        # Separator line
        separator = tk.Frame(parent, height=2, bg='#34495e')
        separator.pack(fill='x', padx=20, pady=10)
        
    def setup_ui(self):
        # Create main container
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Logo
        self.create_logo(main_frame)
        
        # URL input section
        url_frame = tk.Frame(main_frame, bg='#2c3e50')
        url_frame.pack(fill='x', pady=10)
        
        tk.Label(url_frame, text="YouTube URL:", 
                font=('Arial', 12, 'bold'), 
                fg='white', bg='#2c3e50').pack(anchor='w')
        
        url_input_frame = tk.Frame(url_frame, bg='#2c3e50')
        url_input_frame.pack(fill='x', pady=5)
        
        self.url_entry = tk.Entry(url_input_frame, font=('Arial', 11), 
                                 bg='#34495e', fg='white', 
                                 insertbackground='white', relief='flat')
        self.url_entry.pack(side='left', fill='x', expand=True, ipady=5)
        
        # Get formats button
        get_formats_btn = tk.Button(url_input_frame, text="Get Quality Options", 
                                   command=self.get_available_formats,
                                   bg='#3498db', fg='white', 
                                   font=('Arial', 10, 'bold'),
                                   relief='flat', padx=10)
        get_formats_btn.pack(side='right', padx=(10, 0))
        
        # Download type section
        type_frame = tk.Frame(main_frame, bg='#2c3e50')
        type_frame.pack(fill='x', pady=10)
        
        tk.Label(type_frame, text="Download Type:", 
                font=('Arial', 12, 'bold'), 
                fg='white', bg='#2c3e50').pack(anchor='w')
        
        radio_frame = tk.Frame(type_frame, bg='#2c3e50')
        radio_frame.pack(fill='x', pady=5)
        
        self.download_type = tk.StringVar(value="video")
        
        radio_style = {'font': ('Arial', 10), 'fg': 'white', 'bg': '#2c3e50', 
                      'selectcolor': '#34495e', 'activebackground': '#2c3e50'}
        
        tk.Radiobutton(radio_frame, text=" Video", variable=self.download_type, 
                      value="video", **radio_style).pack(side='left', padx=(0, 20))
        tk.Radiobutton(radio_frame, text=" Playlist", variable=self.download_type, 
                      value="playlist", **radio_style).pack(side='left', padx=(0, 20))
        tk.Radiobutton(radio_frame, text="🎵 Audio Only", variable=self.download_type, 
                      value="audio", **radio_style).pack(side='left')
        
        # Quality selection section
        quality_frame = tk.Frame(main_frame, bg='#2c3e50')
        quality_frame.pack(fill='x', pady=10)
        
        tk.Label(quality_frame, text="Quality Selection:", 
                font=('Arial', 12, 'bold'), 
                fg='white', bg='#2c3e50').pack(anchor='w')
        
        # Quality dropdown
        self.quality_var = tk.StringVar()
        self.quality_combo = ttk.Combobox(quality_frame, textvariable=self.quality_var, 
                                         font=('Arial', 10), state='readonly')
        self.quality_combo.pack(fill='x', pady=5)
        
        # Set default quality options
        self.set_default_qualities()
        
        # Download button
        download_btn = tk.Button(main_frame, text=" Start Download", 
                               command=self.start_download,
                               bg='#27ae60', fg='white', 
                               font=('Arial', 14, 'bold'),
                               relief='flat', pady=10)
        download_btn.pack(fill='x', pady=15)
        
        # Progress section
        progress_frame = tk.Frame(main_frame, bg='#2c3e50')
        progress_frame.pack(fill='x', pady=5)
        
        tk.Label(progress_frame, text="Progress:", 
                font=('Arial', 10, 'bold'), 
                fg='white', bg='#2c3e50').pack(anchor='w')
        
        self.progress = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.progress.pack(fill='x', pady=5)
        
        # Status section
        status_frame = tk.Frame(main_frame, bg='#2c3e50')
        status_frame.pack(fill='both', expand=True, pady=10)
        
        tk.Label(status_frame, text="Status Log:", 
                font=('Arial', 10, 'bold'), 
                fg='white', bg='#2c3e50').pack(anchor='w')
        
        # Status text with scrollbar
        text_frame = tk.Frame(status_frame)
        text_frame.pack(fill='both', expand=True, pady=5)
        
        self.status_text = tk.Text(text_frame, height=10, font=('Consolas', 9),
                                  bg='#34495e', fg='#ecf0f1', 
                                  insertbackground='white', relief='flat')
        
        scrollbar = tk.Scrollbar(text_frame, orient='vertical', command=self.status_text.yview)
        self.status_text.configure(yscrollcommand=scrollbar.set)
        
        self.status_text.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Bottom buttons
        button_frame = tk.Frame(main_frame, bg='#2c3e50')
        button_frame.pack(fill='x', pady=10)
        
        change_dir_btn = tk.Button(button_frame, text=" Change Directory", 
                                  command=self.change_directory,
                                  bg='#9b59b6', fg='white', 
                                  font=('Arial', 10, 'bold'),
                                  relief='flat', padx=15)
        change_dir_btn.pack(side='left')
        
        clear_log_btn = tk.Button(button_frame, text=" Clear Log", 
                                 command=self.clear_log,
                                 bg='#e67e22', fg='white', 
                                 font=('Arial', 10, 'bold'),
                                 relief='flat', padx=15)
        clear_log_btn.pack(side='right')
        
        # Initial log message
        self.log_message(" Hi , Iam tahir and iam here to help you to download any playlist or video from youtube ! ")
        self.log_message(f" Default download directory: {self.download_path.absolute()}")
        
    def set_default_qualities(self):
        """Set default quality options"""
        default_qualities = [
            "best - Best available quality",
            "4K (2160p)",
            "2K (1440p)", 
            "Full HD (1080p)",
            "HD (720p)",
            "SD (480p)",
            "(360p)",
            "Worst available quality"
        ]
        
        self.quality_combo['values'] = default_qualities
        self.quality_combo.set("HD (720p)")  # Default selection
        
    def get_available_formats(self):
        """Get available formats for the given URL"""
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a URL first")
            return
            
        self.log_message("🔍 Fetching available quality options...")
        
        def fetch_formats():
            try:
                ydl_opts = {
                    'quiet': True,
                    'no_warnings': True,
                    'listformats': True,
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    
                formats = info.get('formats', [])
                
                # Filter and organize formats
                video_formats = []
                audio_formats = []
                
                for f in formats:
                    if f.get('vcodec') != 'none' and f.get('acodec') != 'none':  # Video with audio
                        height = f.get('height', 0)
                        fps = f.get('fps', 30)
                        ext = f.get('ext', 'mp4')
                        filesize = f.get('filesize')
                        
                        size_str = ""
                        if filesize:
                            size_mb = filesize / (1024 * 1024)
                            size_str = f" (~{size_mb:.1f}MB)"
                        
                        if height:
                            format_desc = f"best[height<={height}] - {height}p {fps}fps ({ext}){size_str}"
                            if format_desc not in video_formats:
                                video_formats.append(format_desc)
                
                # Sort by quality (highest first)
                video_formats.sort(key=lambda x: int(re.search(r'(\d+)p', x).group(1)) if re.search(r'(\d+)p', x) else 0, reverse=True)
                
                # Add audio-only options
                audio_formats = [
                    "bestaudio - Best audio quality",
                    "bestaudio[ext=m4a] - Best M4A audio",
                    "bestaudio[ext=mp3] - Best MP3 audio"
                ]
                
                # Combine all options
                all_formats = ["best - Best available quality"] + video_formats + ["--- Audio Only ---"] + audio_formats
                
                # Update combobox
                self.root.after(0, lambda: self.update_quality_options(all_formats))
                self.root.after(0, lambda: self.log_message(" Quality options updated!"))
                
            except Exception as e:
                self.root.after(0, lambda: self.log_message(f" Error fetching formats: {str(e)}"))
        
        thread = threading.Thread(target=fetch_formats)
        thread.daemon = True
        thread.start()
        
    def update_quality_options(self, formats):
        """Update the quality combobox with fetched formats"""
        self.quality_combo['values'] = formats
        if formats:
            self.quality_combo.set(formats[0])
            
    def get_format_code(self, quality_selection):
        """Extract format code from quality selection"""
        if "best[height<=" in quality_selection:
            return quality_selection.split(" - ")[0]
        elif "bestaudio" in quality_selection:
            return quality_selection.split(" - ")[0]
        elif quality_selection.startswith("best"):
            return "best"
        elif quality_selection.startswith("worst"):
            return "worst"
        else:
            return "best[height<=720]"  # fallback
        
    def log_message(self, message):
        """Add message to status log"""
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)
        self.root.update()
        
    def clear_log(self):
        """Clear the status log"""
        self.status_text.delete(1.0, tk.END)
        self.log_message(" Log cleared")
        
    def start_download(self):
        """Start the download process"""
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a URL")
            return
            
        quality = self.quality_var.get()
        if not quality:
            messagebox.showerror("Error", "Please select a quality option")
            return
            
        self.progress.start()
        thread = threading.Thread(target=self.download_worker, args=(url, quality))
        thread.daemon = True
        thread.start()
        
    def download_worker(self, url, quality):
        """Worker thread for downloading"""
        try:
            download_type = self.download_type.get()
            format_code = self.get_format_code(quality)
            
            self.log_message(f" Starting download with quality: {quality}")
            
            if download_type == "playlist":
                self.download_playlist(url, format_code)
            elif download_type == "audio":
                self.download_audio(url, format_code)
            else:
                self.download_video(url, format_code)
                
        except Exception as e:
            self.log_message(f" Error: {str(e)}")
        finally:
            self.root.after(0, self.progress.stop)
            
    def sanitize_filename(self, filename):
        """Remove invalid characters from filename"""
        return re.sub(r'[<>:"/\\|?*]', '', filename)
            
    def download_video(self, url, format_code):
        """Download a single video"""
        ydl_opts = {
            'format': format_code,
            'outtmpl': str(self.download_path / '%(title)s.%(ext)s'),
            'ignoreerrors': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        self.log_message(" Video download completed!")
        
    def download_playlist(self, url, format_code):
        """Download entire playlist"""
        # Get playlist info first
        with yt_dlp.YoutubeDL({'quiet': True, 'extract_flat': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            
        playlist_title = self.sanitize_filename(info.get('title', 'Unknown_Playlist'))
        playlist_folder = self.download_path / playlist_title
        playlist_folder.mkdir(exist_ok=True)
        
        self.log_message(f" Created folder: {playlist_title}")
        self.log_message(f" Total videos: {len(info.get('entries', []))}")
        
        ydl_opts = {
            'format': format_code,
            'outtmpl': str(playlist_folder / '%(playlist_index)02d - %(title)s.%(ext)s'),
            'ignoreerrors': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        self.log_message(" Playlist download completed!")
        
    def download_audio(self, url, format_code):
        """Download audio only"""
        audio_folder = self.download_path / "Audio"
        audio_folder.mkdir(exist_ok=True)
        
        # Check if it's a playlist for audio
        try:
            with yt_dlp.YoutubeDL({'quiet': True, 'extract_flat': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                
            is_playlist = 'entries' in info and len(info.get('entries', [])) > 1
            
            if is_playlist:
                playlist_title = self.sanitize_filename(info.get('title', 'Unknown_Playlist'))
                audio_folder = audio_folder / playlist_title
                audio_folder.mkdir(exist_ok=True)
                outtmpl = str(audio_folder / '%(playlist_index)02d - %(title)s.%(ext)s')
                self.log_message(f" Created audio playlist folder: {playlist_title}")
            else:
                outtmpl = str(audio_folder / '%(title)s.%(ext)s')
        except:
            outtmpl = str(audio_folder / '%(title)s.%(ext)s')
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': outtmpl,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'ignoreerrors': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        self.log_message("🎵 Audio download completed!")
        
    def change_directory(self):
        """Change download directory"""
        directory = filedialog.askdirectory()
        if directory:
            self.download_path = Path(directory)
            self.log_message(f" Download directory changed to: {directory}")

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloaderGUI(root)
    root.mainloop()
