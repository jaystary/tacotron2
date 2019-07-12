from pydub import AudioSegment
import re
import random


def split_sentences(sentence):
    new_list = []
    sentence.replace('....', '.').replace('...', '.').replace('..', '.')
    ends = ['.', '!', '?']
    split_sentence = re.split('\.+|\!+|\?+|', sentence)
    for s in split_sentence:
        if len(s)>3:
            val = s.strip()
            contains_delimiter = checkEnds(val, ends)
            if not contains_delimiter:
                val += '.'
            new_list.append(val)

    return new_list


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


def checkEnds(line, ends):
    return any(line.endswith(end) for end in ends)


