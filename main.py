from flask import Flask, jsonify
from flask import request, render_template, Response
from flask import send_file
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room
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
socket = SocketIO(app)
CORS(app)


@socket.on('connect')
def on_connect():
    print('user connected')
    activate_socket()

@socket.on('send_message')
def on_sent(data):
    emit('message_sent', data)

def activate_socket():
    emit('activate_socket', 'Hello')

#@socketio.on('send_message')
#    def handle_source(json_data):
#        text = json_data['message'].encode('ascii', 'ignore')
#        emit('echo', {'echo': 'Server Says: '+text}, broadcast=True, include_self=False)


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
    response.headers.add('Access-Control-Allow-Origin', '*')
    #return render_template('audio.html')


if __name__ == "__main__":
    app.run(host="localhost", port=PORT, debug=True)
