#Bot que pela URL do YT consegue transcrever para um arquivo de testo markdown
import yt_dlp
import whisper

# Passo 1: Baixar o áudio do YouTube e converter para WAV
link = input("Link do vídeo: ")
ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': 'D:\bottranscript/%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
        'preferredquality': '192',
    }],
}

print("Baixando e convertendo o áudio para WAV...")
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(link, download=True)
    audio_path = ydl.prepare_filename(info).replace('.webm', '.wav').replace('.mp4', '.wav')
print("Áudio baixado com sucesso!")

# Passo 2: Transcrever o áudio com openai-whisper
modelo = whisper.load_model("base")
resposta = modelo.transcribe(audio_path)
texto = resposta['text']
with open('transcricao.txt', 'w', encoding='utf-8') as arquivo_texto:
    arquivo_texto.write(texto)
print("Transcrição salva em 'transcricao.txt' com sucesso.")
