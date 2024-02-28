import sys
import os
import re
from openai import OpenAI
from pathlib import Path


argc = len(sys.argv)

if argc < 2:
    error_message = "python input_video_script_file (tex)"
    print(error_message)
    raise Exception(error_message)

input_video_script_file = sys.argv[1]

fin = open(input_video_script_file, 'r')
lines = fin.read()

audios = re.findall('\\\\audio\s*\[(.*?)\]\s*{(.*?)}', lines, re.DOTALL)

client = OpenAI()
# Iterate over each text portion
for i, text in enumerate(audios, start=1):
    # Call the OpenAI Text-to-Speech API
    file_tag = text[0]
    audio_script = text[1]
    output_script_file = file_tag + '.txt'
    fout = open(output_script_file, 'w')
    fout.write(audio_script)
    fout.close()
    response = client.audio.speech.create(
        #adjust model and voice here
        model="tts-1",
        voice="alloy",
        input=audio_script
    )

    # Define the path for the output audio file
    speech_file_path = Path(f"{file_tag}.mp3")

    # Save the audio content to a file, the function says to have a bug but works well on my side
    response.stream_to_file(str(speech_file_path))

    print(f"Saved speech to {speech_file_path}")
