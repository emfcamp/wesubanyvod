# --- importing boring stuff ---
import os
import config
import logging
# --- importing AI related stuff --- #
import whisper
import torch

logging.root.setLevel(logging.INFO)

# --- start cuda engine, load the model into it ---
torch.cuda.init()
logging.info(f"Loaded CUDA device {config.cuda_device}")
model = whisper.load_model(config.model).to(config.cuda_device) # Change this to your desired model
logging.info(f"Loaded model {config.model}.")
writer = whisper.utils.WriteSRT("static")

# --- pick up directories from config ---
input_directory = os.fsencode(config.input_folder)
logging.info(f"Input folder: {config.input_folder}")
srt_directory = os.fsencode(config.srt_folder)
logging.info(f"SRT output folder: {config.srt_folder}")

def transcribe_audio(src_file):
    logging.warning(f"Transcribing {src_file}...")
    transcription = model.transcribe(audio=src_file,verbose=True)
    with torch.cuda.device(config.cuda_device):  
        if config.c3voc_mode:
            srtfilename = config.srt_folder + '/' + f"{"-".join(src_file[src_file.find('/')+1:].split("-", 2)[:2])}.srt"
        else:
            srtfilename = config.srt_folder + '/' + src_file[src_file.find('/')+1:]
        with open(srtfilename, 'a', encoding='utf-8') as srtFile:
            writer.write_result(transcription, srtFile)
    logging.info(f'Finished writing {srtfilename}')
for file in os.listdir(input_directory):
    src_file = os.fsdecode(file)
    if src_file.endswith(".mp3") or src_file.endswith(".wav") or src_file.endswith(".mp4") or src_file.endswith(".webm"): 
        transcribe_audio(f"{config.input_folder}/{src_file}")
        continue
    else:
        continue