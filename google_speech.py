# extra audio portions from a video script file and dump them into individual text files for speech synthesis

import sys
import os
import shutil
import subprocess
import re
import glob
from google.cloud import texttospeech

argc = len(sys.argv)

if argc < 2:
    error_message = "python input_video_script_file (tex)";
    print(error_message)
    raise Exception(error_message)

input_video_script_file = sys.argv[1]

fin = open(input_video_script_file, 'r')
lines = fin.read()

audios = re.findall('\\\\audio\s*\[(.*?)\]\s*{(.*?)}', lines, re.DOTALL)

client = texttospeech.TextToSpeechClient()
voice = texttospeech.VoiceSelectionParams(
    language_code='en-US',
    #ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE,
    name='en-US-Wavenet-F')

audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3)   

for audio in audios:
    file_tag = audio[0]
    audio_script = audio[1]
    
    output_script_file = file_tag + '.txt'
    fout = open(output_script_file, 'w')
    fout.write(audio_script)
    fout.close()

    synthesis_input = texttospeech.SynthesisInput(text=audio_script)
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

    with open(file_tag+'.mp3', 'wb') as out:
        out.write(response.audio_content)
    
    os.remove(output_script_file)
