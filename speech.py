# extra audio portions from a video script file and dump them into individual text files for speech synthesis

import sys
import os
import shutil
import subprocess
import re
import glob

argc = len(sys.argv)

if argc < 3:
    error_message = "python speech_config_file (vbs) input_video_script_file (tex)";
    print(error_message)
    raise Exception(error_message)

speech_config_file = sys.argv[1]
input_video_script_file = sys.argv[2]

fin = open(input_video_script_file, 'r')
lines = fin.read()

audios = re.findall('\\\\audio\s*\[(.*?)\]\s*{(.*?)}', lines, re.DOTALL)
for audio in audios:
    file_tag = audio[0]
    audio_script = audio[1]
    
    output_script_file = file_tag + '.txt'
    fout = open(output_script_file, 'w')
    fout.write(audio_script)
    fout.close()
    
    output_audio_file = file_tag + '.wav'
    command = 'cscript ' + speech_config_file + ' ' + output_script_file + ' ' + output_audio_file
    os.system(command)

