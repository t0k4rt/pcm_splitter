import os
import sys
import logging
import wave
import csv
from pydub import silence
from pydub import AudioSegment
from slugify import slugify

filename = sys.argv[1] or "./rip.output.pcm"
tracklist = sys.argv[2] or "./tracklist_final.csv"
debug = sys.argv[3] or "false"

l = logging.getLogger("pydub.converter")
l.setLevel(logging.INFO)



if debug == 'true':
    l.setLevel(logging.DEBUG)
l.addHandler(logging.StreamHandler())

l.info("Launching splitter with parameters:")
l.info("filename: "+filename)
l.info("tracklist: "+tracklist)
l.info("debug: "+debug)

l.debug("convert raw pcm to wav")
with open(filename, 'rb') as pcmfile:
    pcmdata = pcmfile.read()
with wave.open(filename+'.wav', 'wb') as wavfile:
    wavfile.setparams((2, 2, 44100, 0, 'NONE', 'NONE'))
    wavfile.writeframes(pcmdata)

l.debug("analyzing audio")
wav_audio = AudioSegment.from_file(filename+'.wav')
# chunks = silence.split_on_silence(
#     wav_audio,

#     # split on silences longer than 1000ms (1 sec)
#     min_silence_len=1500,

#     # anything under -16 dBFS is considered silence
#     silence_thresh=-40, 

#     # keep 200 ms of leading/trailing silence
#     keep_silence=300
# )

# l.debug("chunks length", len(chunks))
# # for i, chunk in enumerate(chunks):
# #   with open("sound-%s.ogg" % i, "wb") as f:
# #     chunk.export(f, format="ogg")
start = 0
add_silence = 0
with open(tracklist, newline='') as csvfile:
    csv_file = csv.reader(csvfile, delimiter=';')
    for i,line in enumerate(csv_file):
        print(line)
        with open("./export/track-%s.ogg" % slugify(line[0]), "wb") as f:
            end = start + int(line[3])
            print(start, end)
            current_track = wav_audio[start:end]
            start = end
            if add_silence > 100:
                current_track = AudioSegment.silent(duration=add_silence).append(current_track)
            current_track.export(f, format="ogg", tags={"TITLE":line[0] ,"ARTIST": line[1],"ALBUM": line[2]}, parameters=["-q:a", "9"])
        
 
os.remove(filename+".wav")

# https://stackoverflow.com/questions/16111038/how-to-convert-pcm-files-to-wav-files-scripting
# https://github.com/jiaaro/pydub/blob/master/API.markdown
# http://pydub.com/ -> split_on_silence
# https://github.com/amsehili/auditok
# https://github.com/jiaaro/pydub/blob/master/API.markdown