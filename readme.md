# LocalWhisper

## Introduction
TranscribeTools is an Python application which transcribes all 
sound files in a configurable folder using a local Whisper model. 
You can choose which Whisper model is to be used 

## Details
 - using Python 3.12.7, openai-whisper https://pypi.org/project/openai-whisper/ (current version 20240930) 
does not support 3.13 yet.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Setup
We use uv for managing virtual environments and package installation. Follow these steps to set up the project:

On macOS and Linux:
## Download the setup script
curl -O https://raw.githubusercontent.com/ncdegroot/audio_transcriber/main/setup.sh

# Make the script executable
chmod +x setup.sh

# Run the setup script
./setup.sh
On Windows:
# Download the setup script
Invoke-WebRequest -Uri https://raw.githubusercontent.com/yourusername/audio_transcriber/main/setup.ps1 -OutFile setup.ps1

# Set execution policy to run the script
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# Run the setup script
.\setup.ps1
These scripts will:

Install uv if it's not already installed
Create a virtual environment
Activate the virtual environment
Install all required packages


## Plans
- add speaker partitioning
- use (same) models through directly from PyTorch (more control)

## Documentation about Whisper on the cloud and local
- [Courtesy of and Credits to OpenAI: Whisper.ai](https://github.com/openai/whisper/blob/main/README.md)
- [doc](https://pypi.org/project/openai-whisper/)
- [alternatief model transcribe and translate](https://huggingface.co/facebook/seamless-m4t-v2-large)