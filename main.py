import yt_dlp
import whisper
from transformers import pipeline

# Passo 1: Baixar o áudio do YouTube e converter para WAV
link = input("Link do vídeo: ")
ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': 'Users/migui/Downloads/videos/%(title)s.%(ext)s',
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

# Passo 2: Transcrever o áudio com OpenAI Whisper
modelo = whisper.load_model("base")
resposta = modelo.transcribe(audio_path)
texto = resposta['text']
with open('transcricao.txt', 'w', encoding='utf-8') as arquivo_texto:
    arquivo_texto.write(texto)
print("Transcrição salva em 'transcricao.txt' com sucesso.")

# Passo 3: Criar um markdown resumido usando T5
resumo_pipeline = pipeline("summarization", model="t5-base")

# Dividir texto em partes para evitar problemas de comprimento
tamanho_maximo = 1024
texto_parts = [texto[i:i+tamanho_maximo] for i in range(0, len(texto), tamanho_maximo)]

resumos = []
for parte in texto_parts:
    resumo = resumo_pipeline(parte, max_length=150, min_length=30, do_sample=False, truncation=True)[0]['summary_text']
    resumos.append(resumo)

resumo_final = ' '.join(resumos)

with open('resumo.md', 'w', encoding='utf-8') as arquivo_markdown:
    arquivo_markdown.write(f"# Resumo do Vídeo\n\n{resumo_final}")
print("Resumo em markdown salvo em 'resumo.md' com sucesso.")
