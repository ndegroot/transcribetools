# TranscribeTools

## Introduction
TranscribeTools is a collection of commandline tools for transcription and translation, which currently only includes TranscribeFolder. Transcribefolder is a Python application that transcribes all sound files in a configurable folder using a local version of the Whisper model. Whisper is an automatic speech recognition system created by OpenAI, which can transcribe audio files in multiple languages and translate those languages into English.

The model must be run locally to comply with the General Data Protection Regulation (GDPR). This is because, when using OpenAI’s transcription service (based on the Whisper model), OpenAI collects user data from prompts and files uploaded by the user. These audio files may contain personal data from which people can be identified. Therefore, using OpenAI’s service without a processing agreement is not allowed within organisations.

On the other hand, using TranscribeTools to run the Whisper model on your own device means that files containing personal data will not be collected. The program essentially downloads the model—released as open-source software in 2022—and uses the command line to select a folder, which it then transcribes, all locally.

It works with audio files under 25 MB in the following formats: mp3, wav, mp4, mpeg, mpga, m4a, and webm. It also allows the user to choose the model size. The larger models are more accurate but slower, and vice versa.

Furthermore, the application utilizes the terminal—a text-based interface to interact with the computer—to install and use Whisper. This might sound intimidating but is hopefully manageable when following the instructions given below. The terminal is already installed in most cases.

## Details
 - using Python 3.12.7, openai-whisper https://pypi.org/project/openai-whisper/ (current version 20240930) 
does not support 3.13 yet.

## License
This project is licensed under the Apache 2.0 License - see the [LICENSE file](LICENSE) for details.

## Setup
Before installing TranscribeTools, you need to download a package manager to install dependencies—pieces of code that the application relies on. On macOS, we will use Homebrew and uv; on Windows, we will only use uv. Then, we will install TranscribeTools.

To run the following prompts, one must copy and paste the commands in the command line and press enter. During the setup, it might be necessary to restart powershell after installing homebrew, uv, or transcribetools in order to be able to proceed. 

### Package manager
#### On Windows
Open Windows Powershell or the Command shell

Run prompt to install uv:

```powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"```

#### On macOS:
Open Terminal

Run prompt to install brew:

```/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"```

Run prompt to install uv:

```brew install uv```

### Install tools
Install the (commandline) tools in this project. For now it's only `transcribefolder`:

```uv tool install transcribetools```

## Command-line usage
Run prompt to see the possible commands and options:

```transcribefolder --help```

Run prompt to create a configuration file with the right folder to transcribe and the right whisper model to use:

```transcribefolder config create```

Run prompt to transcribe all sound files in the selected folder using the configuration file transcribefolder.toml:

```transcribefolder transcribe```

Run prompt to transcribe all sound files in the selected folder using a specific configuration file:

```transcribefolder -c name of the config file.toml transcribe```

## Known issues 
- The deepl_translate command is not yet working. 
- The duration and realtime factor are not available for processed files in the formats: mp4, mpeg, mpga, m4a, and webm.

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
