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

### On macOS:
#### Install uv

- first install brew if needed from https://github.com/Homebrew/brew/releases/latese

### On Windows:
#### Download the setup script
```Invoke-WebRequest -Uri https://gitlab.uvt.nl/tst-research/transcribetools/-/blob/main/setup.ps1?ref_type=heads -OutFile setup.ps1```

#### Set execution policy to run the script
```Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass```

#### Run the setup script
.\setup.ps1

### These scripts will:

Install uv if it's not already installed

### Install localwhisper

```uv tool install transcribetool```

Install (commandline) tools in this project. For now only `localwhisper`.

## Plans
- add speaker partitioning
- use (same) models through directly from PyTorch (more control)

## Documentation about Whisper on the cloud and local
- [Courtesy of and Credits to OpenAI: Whisper.ai](https://github.com/openai/whisper/blob/main/README.md)
- [doc](https://pypi.org/project/openai-whisper/)
- [alternatief model transcribe and translate](https://huggingface.co/facebook/seamless-m4t-v2-large)