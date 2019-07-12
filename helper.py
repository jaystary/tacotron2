import audiolab, scipy
import re


def split_sentences(sentence):
    sentence.replace('....', '.').replace('...', '.').replace('..', '.')
    return re.split(r'[.;!?]+', sentence)


#takes list of wav files and merges them to one
def merge_wav():
    a, fs, enc = audiolab.wavread('file1.wav')
    b, fs, enc = audiolab.wavread('file2.wav')
    c = scipy.vstack((a, b))
    audiolab.wavwrite(c, 'file3.wav', fs, enc)
    return rt


