from pydub import AudioSegment
import re
import random


def split_sentences(sentence):
    new_list = []
    sentence.replace('....', '.').replace('...', '.').replace('..', '.')
    re.split(r'[.;!?]+', sentence)
    for s in sentence:
        new_list.append(s.strip())

    

    return new_list()



#takes list of wav files and merges them to one
def merge_wav(filename_list):

    wav_list = []
    combined_wav = AudioSegment.empty()

    for f in filename_list:
        wav_list.append(AudioSegment.from_wav(f))

    for w in wav_list:
        combined_wav += w


    filename = "static/generatedAudio/" + str(random.randint(1, 101)) + 'generated.wav'
    combined_wav.export(filename, format="wav")
    return filename


