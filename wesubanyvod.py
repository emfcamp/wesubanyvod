# --- importing boring stuff ---
from datetime import timedelta
import os
import config
import logging
# --- importing AI related stuff --- #
import whisper
import torch

logging.basicConfig()

# --- start cuda engine, load the model into it ---
torch.cuda.init()
logging.warning(f"Loaded CUDA device {config.cuda_device}")
model = whisper.load_model(config.model).to(config.cuda_device) # Change this to your desired model
logging.warning(f"Loaded model {config.model}.")

# --- pick up directories from config ---
audio_directory = os.fsencode(config.audio_folder)
logging.warning(f"Audio folder: {config.audio_folder}")
srt_directory = os.fsencode(config.srt_folder)
logging.warning(f"SRT output folder: {config.srt_folder}")

def transcribe_audio(src_file):
    logging.warning(f"Transcribing {src_file}...")
    transcribe = model.transcribe(audio=src_file,verbose=True)
    with torch.cuda.device(config.cuda_device):
        segments = transcribe['segments']
        for segment in segments:
            startTime = str(0)+str(timedelta(seconds=int(segment['start'])))+',000'
            endTime = str(0)+str(timedelta(seconds=int(segment['end'])))+',000'
            text = segment['text']
            segmentId = segment['id']+1
            segment = f"{segmentId}\n{startTime} --> {endTime}\n{text[1:] if text[0] == ' ' else text}\n\n"
            srtFilename = os.path.join(f"{config.srt_folder}",f"{src_file.rsplit(".", 1)[0]}.srt")
            with open(srtFilename, 'a', encoding='utf-8') as srtFile:
                srtFile.write(segment)
                logging.warning(segment)
    return srtFilename

for file in os.listdir(audio_directory):
    src_file = os.fsdecode(file)
    if src_file.endswith(".mp3") or src_file.endswith(".wav") or src_file.endswith(".mp4") or src_file.endswith(".webm"): 
        transcribe_audio(f"{config.audio_folder}/{src_file}")
        continue
    else:
        continue