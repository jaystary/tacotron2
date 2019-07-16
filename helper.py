#from pydub import AudioSegment
import re
import random
import datetime
import time
import queue
import asyncio

def split_sentences(sentence):
    que_list = queue.Queue()
    sentence.replace('....', '.').replace('...', '.').replace('..', '.')
    ends = ['.', '!', '?']
    split_sentence = re.split(r'[\.\!\?]', sentence)
    for s in split_sentence:
        if len(s) > 3:
            val = s.strip()
            contains_delimiter = checkEnds(val, ends)
            if not contains_delimiter:
                val += '.'
            que_list.put(val)

    return que_list


def do_something_with_sentences(que):

    que.get()

    return True


def example(seconds):
    print('Starting task')
    for i in range(seconds):
        print(i)
        time.sleep(1)
    print('Task completed')

'''
def merge_wav(filename_list):

    now = datetime.now()
    timestamp = datetime.timestamp(now)

    wav_list = []
    combined_wav = AudioSegment.empty()

    for f in filename_list:
        wav_list.append(AudioSegment.from_wav(f))

    for w in wav_list:
        combined_wav += w

    filename = "static/generatedAudio/" + str(timestamp) + str(random.randint(1, 20)) + '.wav'
    combined_wav.export(filename, format="wav")
    return filename
'''


def checkEnds(line, ends):
    return any(line.endswith(end) for end in ends)


def calculate_position_percent(cur, total):
    return (cur / total)*100





