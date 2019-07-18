from flask import Flask
from flask import request, render_template, Response
from flask import send_file
import queue
import helper
# import audio_processing as ap
import datetime
import pyaudio
import wave
import io
import time
import asyncio
import itertools

# from inference import Inference

CHUNK = 4096

# inference = Inference()
# inference.load_model()

app = Flask(__name__, template_folder='static')

class Sync():
    a = False


sync = Sync()

@app.route('/text', methods=['POST'])
def text():
    print("1")
    val = request.form['sentence']
    sentence_list = helper.split_sentences(val)

    #audio(sentence_list)

    def generate():
        while True:
            yield "data: %s\n\n" % sentence_list.get()
            sentence_list.task_done()
            time.sleep(1)

    return Response(generate(), content_type='text/event-stream')


@app.route('/audio')
def audio():
    print("2")
    p = pyaudio.PyAudio()
    wf = wave.open('sample1.wav', 'rb')

    def generate():
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        @asyncio.coroutine
        def stream_audio():
            data = wf.readframes(CHUNK)
            while True:
                stream.write(data)
                data=wf.readframes(CHUNK)

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        cors = asyncio.wait([stream_audio()])
        loop.run_until_complete(cors)

        loop.close()



    return Response(generate(), mimetype='application/json')

    p.terminate()


@app.route('/')
def index():
    return render_template('audio.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888, debug=True)
