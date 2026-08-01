# --- importing boring stuff ---
import os
import config
import logging
import requests
# --- importing AI related stuff --- #
import whisper
import torch

logging.root.setLevel(logging.INFO)

while True: 

    menu = input("""welcome to wesubanyvod!
please choose an option:
1) bulk transcribe input folder and generate subtitles
2) bulk upload subtitles to publishing.media.ccc.de (WIP - please use with care)
select option: """)

    if menu == '1':
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
        logging.info('transcription of folder {config.input_folder} done!')

    if menu == '2':
        def upload_to_c3voc(srt_file):
            c3voc_publishing_headers = {
            'accept': 'application/json',
            'Authorization': config.c3voc_publishing_api_key
            }

            c3voc_publishing_file = {
                'file': open(f"{config.upload_folder}/{srt_file}", 'rb'),
                'meta': (None, 'subtitles'),
                'groups': (None, ''),
            }

            event = srt_file[:srt_file.index("-")]
            occurrence = srt_file[srt_file.index("-")+1:srt_file.index(".srt")]
            logging.info(f"Processing {srt_file}: Event {event}, occurrence {occurrence}")
            if len(event) < 2 or len(occurrence) < 2:
                logging.info("Event or occurrence length less than 2. Are your files named event-occurrence.srt? (e.g. emf2026-120.srt)")
                return None
            else:
                logging.info(f"Uploading {srt_file}")
                response = requests.put('https://publishing.c3voc.de/api/{event}/events/{occurrence}/file', headers=c3voc_publishing_headers, files=c3voc_publishing_file)
                logging.info(f"Response from server: {response.content}")
                return None
        try:
            os.mkdir(f"{config.upload_folder}/done")
        except:
            pass
        for file in os.listdir(config.upload_folder):
            if file.endswith('.srt'):
                upload_to_c3voc(file)
                os.replace(f"{config.upload_folder}/{file}",f"{config.upload_folder}/done/{file}")
        logging.info('uploader done! uploaded all srt files in {config.upload_folder}')
        
    else:
        print('invalid option, try again!')