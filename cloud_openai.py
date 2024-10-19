from openai import OpenAI
client = OpenAI(api_key='',
                project='proj_9vUCFDiGw5IMcAQYjCsF92qP')

audio_file = open("data/fragment.mp3", "rb")

transcription = client.audio.transcriptions.create(
  model="whisper-1",
  file=audio_file,
  language="nl"
)
print(transcription.text)