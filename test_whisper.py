import whisper

model = whisper.load_model("large")

result = model.transcribe("data/fragment.mp3")
print(result["text"])