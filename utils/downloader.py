import yt_dlp

def download_audio(yt_url, output_file="audio.m4a"):
    ydl_opts = {
        'format': 'bestaudio[ext=m4a]/bestaudio/best',
        'outtmpl': output_file,
        'postprocessors': [],  # <- Skip ffmpeg
        'quiet': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([yt_url])
        return output_file
    except Exception as e:
        print("Download error:", e)
        return None
