import youtube_dl
import os.path

VIDEO_URL = 'https://www.youtube.com/watch?v=9Z1IGjr2cT0'

def download():
    if not os.path.isfile('soundAlert.mp3'):
        options = {
            'outtmpl': 'soundAlert.mp3',
            'format': 'bestaudio/best',
        }
        with youtube_dl.YoutubeDL(options) as youtubeDl:
            youtubeDl.download([VIDEO_URL])
