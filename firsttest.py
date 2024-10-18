from openai import OpenAI
client = OpenAI(api_key='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',
                project='proj_9vUCFDiGw5IMcAQYjCsF92qP')

audio_file = open("data/fragment.mp3", "rb")

transcription = client.audio.transcriptions.create(
  model="whisper-1",
  file=audio_file,
  language="nl"
)
print(transcription.text)