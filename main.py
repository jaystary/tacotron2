#from gevent import monkey
#monkey.patch_all()

async_mode = None

if async_mode is None:
    try:
        import eventlet
        async_mode = 'eventlet'
    except ImportError:
        pass

    if async_mode is None:
        try:
            from gevent import monkey
            async_mode = 'gevent'
        except ImportError:
            pass

    if async_mode is None:
        async_mode = 'threading'

    print('async_mode is ' + async_mode)

# monkey patching is necessary because this application uses a background
# thread
if async_mode == 'eventlet':
    import eventlet
    eventlet.monkey_patch()
elif async_mode == 'gevent':
    from gevent import monkey
    monkey.patch_all()

import time
from threading import Thread
from flask import Flask, jsonify, json
from flask import request, render_template, Response
from flask import send_file
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import psycopg2
from dbconn import db_conn

import queue
from backend_helpers import helper
# import audio_processing as ap
import datetime
import pyaudio
import wave
import io
import time
import asyncio
import itertools
from backend_helpers import log



# from inference import Inference

CHUNK = 4096
PORT = 8888

# inference = Inference()
# inference.load_model()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'development key'
socketio = SocketIO(app, async_mode=async_mode)
CORS(app)

thread = None
conn = None
cursor = None
#results = db_conn.perform_query("select * from tschema.users")
#db_conn.perform_insert_register_users("Jay1", "Juergen1")
#for r in results:
#    print(r['registered'])
getdata("Hello World. How are you", "jay")

def getdata(data, user):

    #lookup uid
    record = db_conn.perform_query(user)


    #Chop up sentences and send back clustered data
    count = 0
    sentence_list = helper.split_sentences(data)
    for sentence in sentence_list:
        # write to database
        job_id = db_conn.perform_insert_jobs()

        data = {'request_id': request.sid,
                'timestamp': int(time.time()),
                'sentence': sentence,
                'audio_id': count,
                'job_id': 1 }
        json_data = json.dumps(data)
        emit('getdata', {'data': json_data}, broadcast=False, include_self=True)

logger = log.setup_custom_logger('root')

def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        time.sleep(10)
        count += 1
        socketio.emit('my response',
                      {'data': 'Server generated event', 'count': count},
                      namespace='/test')


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
def getdata(data, user):

    #lookup uid

    #write to database

    #Chop up sentences and send back clustered data
    count = 0
    sentence_list = helper.split_sentences(data)
    for sentence in sentence_list:

        data = {'request_id': request.sid,
                'timestamp': int(time.time()),
                'sentence': sentence,
                'audio_id': count,
                'job_id': 1 }
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
    '''
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
    '''
    d = make_summary()
    return jsonify(d)


@app.route('/')
def index():
    print("test")
    response.headers.add('Access-Control-Allow-Origin', '*')
    global thread
    if thread is None:
        thread = Thread(target=background_thread)
        thread.daemon = True
        thread.start()
    #return render_template('audio.html')


if __name__ == "__main__":
    #app.run(host="localhost", port=PORT, debug=True)
    socketio.run(app, debug=True, port=8888)
