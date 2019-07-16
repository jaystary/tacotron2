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


@app.route('/text')
def text():
    val = "Hello. How are you today.Last Sentence. Next Sentence. Overnext Sentence. 3rd Overnext Sentence. 4th Sentence. last Sentence."
    sentence_list = helper.split_sentences(val)
    helper.do_something_with_sentences(sentence_list)

    def generate():
        while True:
            yield "data: %s\n\n" % sentence_list.get()
            sentence_list.task_done()
            time.sleep(1)

    return Response(generate(), content_type='text/event-stream')


@app.route('/audio')
def audio():
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

'''




@app.route('/')
def index():
    return render_template('audio.html')



@app.route('/', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        val = request.form['sentence']
        sentence_list = helper.split_sentences(val)
        result_list = []
        result = None
        start = datetime.datetime.now()
        count = 0
        for s in sentence_list:
            if s:
                result_list.append(inference.infer(s))
                count += 1

        if len(sentence_list) > 1:
            result = helper.merge_wav(result_list)
        else:
            if len(result_list) == 1:
                result = result_list[0]

        stop = datetime.datetime.now()
        time = (stop - start) /1000

        template_data = {
            'sentence': result,
            'time': str(time.microseconds),
            'sentence_value': val
        }
        return render_template('index.html', **template_data)

    return render_template('index.html')


@app.route('/api',methods = ['POST'])
def result_api():
    if request.method == 'POST':
        val = request.jsonify
        val = val['sentence']
        sentence_list = helper.split_sentences(val)
        result_list = []
        result = None

        count = 0
        for s in sentence_list:
            if s:
                result_list.append(inference.infer(s))
                count += 1

        if len(sentence_list) > 1:
            result = helper.merge_wav(result_list)
        else:
            if len(result_list) == 1:
                result = result_list[0]


        return send_file(
            result,
            mimetype="audio/wav",
            as_attachment=True)
'''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888, debug=True)
