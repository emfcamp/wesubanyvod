# wecaptionanyvod

A tool for taking VODs from media.ccc.de, and generating SRT caption files using OpenAI's Whisper local speech-to-text-module

## Requirements
- A modern computer, ideally with a CUDA enabled GPU.
- A relatively recent Python version installed
- Install CUDA and PyTorch using [this guide](https://github.com/imxzone/Step-by-Step-Setup-CUDA-cuDNN-and-PyTorch-Installation-on-Windows-with-GPU-Compatibility)
- Install ffmpeg
- Install Whisper using `pip install openai-whisper`

## Usage
- Satisfy requirements as above
- Edit `config.py` to your liking
- Fill your input folder with media (audio is most compact, but it uses ffmpeg so will read basically anything. The script only looks for `mp3`, `mp4`, `wav`, `webm`.)
- Run the script

## Notes

tbd