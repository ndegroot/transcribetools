# LocalWhisper

## Introduction
TranscribeTools is an Python application which transcribes all 
sound files in a configurable folder using a local Whisper model. 
TranscribeTools contains an Python application LocalWhisper
which transcribes all sound files in a configurable folder using a local Whisper model. 
You can choose which Whisper model is to be used 

## Details
 - using Python 3.12.7, openai-whisper https://pypi.org/project/openai-whisper/ (current version 20240930) 
does not support 3.13 yet.

## License
This project is licensed under the Apache 2.0 License - see the [LICENSE file](LICENSE) for details.

## Setup
We use uv for managing virtual environments and package installation. Follow these steps to set up the project:

### On macOS:
#### Install uv
- First install brew if needed from https://github.com/Homebrew/brew/releases/latese

### On Windows:
#### Download the setup script
We need to install `UV` a tool to install the Python environment and to 
install the tool. There are a few possibilities

1. Follow instructions at  [the UV website](https://docs.astral.sh/uv/getting-started/installation/#__tabbed_1_2)

2. Press {Windows button} then type or paste:. 
```powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"```

3. Use `winget`
- Open the Windows Powershell: press {Windows} button and type or paste
```Powershell
winget install --id=astral-sh.uv  -e
```

### These scripts will:

Installs the `uv` tool. Check if `uv {enter}` works. [At the moment](https://github.com/astral-sh/uv/issues/10014) a reboot is needed on Windows.
Now we can install the tools.

### Install tools

```uv tool install transcribetools```

Install the (commandline) tools in this project. For now 
it's only `transcribefolder`.

## Plans
- Make it a local service, running in the background
- Investigate options to let it run on a central computer, as a service
- Create Docker image
- Add speaker partitioning (see TranscribeWhisperX)
- Adjust models using PyTorch (more control)

## Documentation about Whisper on the cloud and local
- [Courtesy of and Credits to OpenAI: Whisper.ai](https://github.com/openai/whisper/blob/main/README.md)
- [doc](https://pypi.org/project/openai-whisper/)
- [alternatief model transcribe and translate](https://huggingface.co/facebook/seamless-m4t-v2-large)