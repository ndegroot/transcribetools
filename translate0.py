import whisper

model = whisper.load_model("large")
# turbo detects 'en', wrongly

# load audio and pad/trim it to fit 30 seconds
audio = whisper.load_audio("data/fragment.mp3")
audio = whisper.pad_or_trim(audio)

# make log-Mel spectrogram and move to the same device as the model
mel = whisper.log_mel_spectrogram(audio, n_mels=model.dims.n_mels).to(model.device)

# detect the spoken language
_, probs = model.detect_language(mel)
detected_language = max(probs, key=probs.get)
print(f"Detected language: {detected_language}")
print("translate to English")

# decode the audio
# options = whisper.DecodingOptions()
# result = whisper.decode(model, mel, options)
model = whisper.load_model("large")
args = dict()
args["language"] = "English"
result = model.transcribe(audio=audio, **args)

# print the recognized text
print(result.text)
