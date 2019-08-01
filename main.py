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

if async_mode == 'eventlet':
    import eventlet
    eventlet.monkey_patch()
elif async_mode == 'gevent':
    from gevent import monkey
    monkey.patch_all()

from threading import Thread
from flask import Flask, jsonify, json
from flask import request, render_template, Response
from flask import send_file
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from dbconn import db_conn, db_aggregation
from inference import Inference
from backend_helpers import helper, log
from backend_helpers.s3_storage import S3Storage
import datetime
import pyaudio
import wave
import io
import time



CHUNK = 4096
PORT = 8888

inference = Inference()
inference.load_model()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'development key'
socketio = SocketIO(app, async_mode=async_mode)
CORS(app)

thread = None
conn = None
cursor = None

logger = log.setup_custom_logger('root')


class AggData(object):
    def __init__(self, filename, audio_length, job_text_id):
        self.filename = filename
        self.audio_length = audio_length
        self.job_text_id = job_text_id
        self.audio_length_percent = 0


@app.route('/audioy', methods=['POST'])
def getdata():
    json_val = request.json
    data = json_val['message']
    user = json_val['user']

    record = db_conn.perform_query(user)

    if record == None:
        return None

    s3_client = S3Storage()

    headline = (data[:70] + '..') if len(data) > 70 else data
    job_id = db_conn.perform_insert_jobs(record['uid'], 0, 1, headline)

    count = 0
    sentence_list = helper.split_sentences(data)
    agg_list = []

    for sentence in sentence_list:
        job_text_id = job_id + '_' + str(count)
        audio_length = inference.infer(sentence, job_text_id)
        filename = "tmp/" + job_text_id + ".mp3"
        agg_list.append(AggData(filename, audio_length, job_text_id))

        s3_filename = job_text_id + ".mp3"
        db_conn.perform_insert_job_text(job_id, sentence, audio_length, count)
        count += 1

        #upload file and verify success otherwise ignore and continue - check that file exists

        response = s3_client.store_data("audiomodelstts", filename, s3_filename)

        data = {'request_id': "asdf",
                'timestamp': int(time.time()),
                'sentence': sentence,
                'audio_id': count,
                'job_id': s3_filename}

        json_data = json.dumps(data)
    #start background thread - merge files - write to db - propagate changes to frontend
    db_aggregation.aggregate_job_results(agg_list, job_id, s3_client)

    return json_data

        #emit('getdata', {'data': json_data}, broadcast=False, include_self=True)

    #Once all data is done merge the file and record in jobs (Link)


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
    from gevent import monkey
    monkey.patch_all()
    socketio.run(app, debug=True, port=8888)
