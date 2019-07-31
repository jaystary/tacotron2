from pydub import AudioSegment
import re
import random
import datetime
import time
import logging

def split_sentences(sentence):
    que_list = []
    sentence.replace('....', '.').replace('...', '.').replace('..', '.')
    ends = ['.', '!', '?']
    split_sentence = re.split(r'[\.\!\?]', sentence)
    for s in split_sentence:
        if len(s) > 3:
            val = s.strip()
            contains_delimiter = checkEnds(val, ends)
            if not contains_delimiter:
                val += '.'
            que_list.append(val)

    return que_list

def merge_wav(agg_list, new_file_name):

    audio_list = []
    combined = AudioSegment.empty()

    for f in agg_list:
        audio_list.append(AudioSegment.from_mp3(f.filename))

    for w in audio_list:
        combined += w

    filename = "tmp/" + new_file_name + '.mp3'
    combined.export(filename, format="mp3")

    return filename


def checkEnds(line, ends):
    return any(line.endswith(end) for end in ends)


def calculate_position_percent(cur, total):
    return (cur / total)*100







