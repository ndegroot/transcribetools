"""uses cloud version of whisper model to transcribe
a key-like project name has tob be created in de OpenAi site,
you need an OpenAI account for that"""
from openai import OpenAI
from tiutools import OpenAICloudConfig

# 08-01-2025 laatste run: $0.02

config = OpenAICloudConfig(reset_keys=False)  # the keys are safe in the macOS keychain

api_key = config.api_key
project = config.prj_id

client = OpenAI(api_key=api_key,
                project=project)

audio_file = open("data/filename.mp3", "rb")

transcription = client.audio.transcriptions.create(
  model="whisper-1",
  file=audio_file,
  language="nl"
)
print(transcription.text)

