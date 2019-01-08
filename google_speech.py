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
voice = texttospeech.types.VoiceSelectionParams(
    language_code='en-US',
    ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)
audio_config = texttospeech.types.AudioConfig(
    audio_encoding=texttospeech.enums.AudioEncoding.MP3)   

for audio in audios:
    file_tag = audio[0]
    audio_script = audio[1]
    
    output_script_file = file_tag + '.txt'
    fout = open(output_script_file, 'w')
    fout.write(audio_script)
    fout.close()

    synthesis_input = texttospeech.types.SynthesisInput(text=audio_script)
    response = client.synthesize_speech(synthesis_input, voice, audio_config)

    # The response's audio_content is binary.
    with open(file_tag+'.mp3', 'wb') as out:
        # Write the response to the output file.
        out.write(response.audio_content)
    
    #output_audio_file = file_tag + '.wav'
    #command = 'cscript ' + speech_config_file + ' ' + output_script_file + ' ' + output_audio_file
    #os.system(command)

    os.remove(output_script_file)
