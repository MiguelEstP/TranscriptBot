# Analisador de Vídeos do YT (vídeo -> script)
# imports gerais
import pytubefix
import ffmpeg
import openai

# OpenAIkey
openai.api_key = "Coloque sua API Key aq"

# Importar a URL dele (baixar o áudio)
import sys
url = sys.argv[1]
filename = "audio.wav"
yt = pytubefix.YouTube(url)
stream = yt.streams.filter(only_audio=True).first().url
ffmpeg.input(stream).output(filename,
                            format='wav',
                            loglevel="error")

# Transcrever o audio para texto
with open(filename, "rb") as audio_file:
    transcript = openai.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    ).text

# Gerar um script
completion = openai.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system",
         "content": """
         Você é um assistem que resume videos detalhando eles.
         Responda com formatação Markdown.
         """},

         {"role": "user",
          "content": f"Descreva o seguinde vídeo: {transcript}"}
    ])

# Salvar o resumo em um arquivo Markdown
with open("resumo.md", "w+") as md_file:
    md_file.write(completion.choices[0].message.content)
