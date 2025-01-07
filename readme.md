# LocalWhisper

## Introduction
TranscribeTools is an Python application which transcribes all 
sound files in a configurable folder using a local Whisper model. 
You can choose which Whisper model is to be used 

## Details
 - using Python 3.12.7, openai-whisper https://pypi.org/project/openai-whisper/ (current version 20240930) 
does not support 3.13 yet.

## Plans
- add speaker partitioning
- use (same) models through directly from PyTorch (more control)

## Documentation about Whisper on the cloud and local
- [doc](https://pypi.org/project/openai-whisper/)
- [alternatief model transcribe and translate](https://huggingface.co/facebook/seamless-m4t-v2-large)