#Bot que pela URL do YT consegue transcrever para um arquivo de testo markdown
#Baixar o audio do vídeo do YT
import yt_dlp

link = input("Link do vídeo: ")
ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': 'D:\Miguel\Downloads\Vídeos/%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([link])
print("O áudio foi baixado com sucesso.")
