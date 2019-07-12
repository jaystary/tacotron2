from pydub import AudioSegment
import re


def split_sentences(sentence):
    sentence.replace('....', '.').replace('...', '.').replace('..', '.')
    return re.split(r'[.;!?]+', sentence)


#takes list of wav files and merges them to one
def merge_wav(filename_list):

    wav_list = []
    combined_wav = None

    for f in filename_list:
        wav_list.append(AudioSegment.from_wav(f))

    for w in wav_list:
        combined_wav = combined_wav + w


    filename = "static/generatedAudio/" + str(random.randint(1, 101)) + 'generated.wav'
    combined_sounds.export(filename, format="wav")
    return filename


