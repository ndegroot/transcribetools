from datetime import datetime
import pathlib
import whisper

MODEL = "large"
model = None


def process_file(path):
    output_path = path.with_suffix('.txt')
    try:
        print("Start processing...")
        result = model.transcribe(str(path), verbose=True)
        # false: only progressbar; true: all; no param: no feedback
    except Exception as e:
        print(f"Error while processing {path}: '{e}'. Please fix it")
    else:
        text_to_save = result["text"]
        print(text_to_save)

        # file_name = f"{data_file.split('.')[0]}_{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.txt"
        file_name = output_path
        # Open the file in write mode
        with open(output_path, 'w') as file:
            # Write the text to the file
            file.write(text_to_save)

        print(f'Text has been saved to {output_path}')


if __name__ == "__main__":

    model = whisper.load_model(MODEL)  # "large")

    internal_path = pathlib.Path('data')
    teams_path = pathlib.Path('/Users/ncdegroot/Library/CloudStorage/'
                              'OneDrive-Gedeeldebibliotheken-TilburgUniversity/'
                              'Project - Reflective cafe - data')
    path = teams_path

    txt_files = [file for file in path.glob('*') if file.suffix.lower() == '.txt']
    file_stems = [file.stem for file in txt_files]
    # file_stem indicates mp3 has been processed already
    mp3_files = [file for file in path.glob('*') if file.suffix.lower() == '.mp3' and file.stem not in file_stems]

    print(f"{len(mp3_files)} files to be processed")
    for file in mp3_files:
        print(f"Processing {file}")
        process_file(file)
