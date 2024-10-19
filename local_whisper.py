from datetime import datetime

import whisper

MODEL = "large"

model = whisper.load_model(MODEL)  # "large")

data_file = "240221_0098GroepChristel.MP3"
result = model.transcribe(f"data/{data_file}")
text_to_save = result["text"]
print(text_to_save)

file_name = f"data/{data_file.split('.')[0]}_{datetime.now().strftime('%Y-%m-%d')}.txt"
# Open the file in write mode
with open(file_name, 'w') as file:
    # Write the text to the file
    file.write(text_to_save)

print(f'Text has been saved to {file_name}')
