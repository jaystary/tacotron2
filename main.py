#from gevent import monkey
#monkey.patch_all()

from flask import Flask, jsonify, json
from flask import request, render_template, Response
from flask import send_file
from flask_cors import CORS
from flask_socketio import SocketIO, emit

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
PORT = 8888

# inference = Inference()
# inference.load_model()

app = Flask(__name__, template_folder='static')
app.config['SECRET_KEY'] = 'development key'
socketio = SocketIO(app)
socketio.start_background_task(app)
CORS(app)

@socketio.on('connect')
def connected():
    print("connecting")
    print(request.sid)
    data = {'request_id': request.sid,
            'timestamp': int(time.time())}
    json_data = json.dumps(data)
    emit('echo', {'data': json_data}, broadcast=False, include_self=True)


@socketio.on('disconnect')
def disconnect():
    print("disconnecting")
    data = {'request_id': request.sid,
            'timestamp': int(time.time())}


@socketio.on('getdata', namespace='/audiostream')
def getdata(data):

    #Chop up sentences and send back clustered data
    count = 0
    sentence_list = helper.split_sentences(data)
    for sentence in sentence_list:

        data = {'request_id': request.sid,
                'timestamp': int(time.time()),
                'sentence': sentence,
                'audio_id': count,
                'job_id': }
        json_data = json.dumps(data)
        emit('getdata', {'data': json_data}, broadcast=False, include_self=True)
        count += 1
        socketio.sleep(0)

    #Merge all files into 1 and then send this file when its required again
    #Write first sentence to DB and store properties of file





#@socketio.on('send_message')
#    def handle_source(json_data):
#        text = json_data['message'].encode('ascii', 'ignore')
#        emit('echo', {'echo': 'Server Says: '+text}, broadcast=True, include_self=False)


#def process_text(message):



@app.route('/infer_tts', methods=['GET', 'POST'])
def text():
    #val = request.json
    #val = val['sentence']

    #sentence_list = helper.split_sentences(val)
    #print(sentence_list)



    def generate():

        yield jsonify({'some': 'data'})
        #while True:
        #    yield "data: %s\n\n" % sentence_list.get()
        #    sentence_list.task_done()
        #    time.sleep(1)


    return Response(generate(), content_type='text/event-stream')


@app.route('/audiox')
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
    response.headers.add('Access-Control-Allow-Origin', '*')
    #return render_template('audio.html')


if __name__ == "__main__":
    #app.run(host="localhost", port=PORT, debug=True)
    socketio.run(app, debug=True, port=8888)
