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
from flask import Flask, json
from flask import request, Response
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from dbconn import db_conn, db_aggregation
from inference import Inference
from backend_helpers import helper, log
from backend_helpers.s3_storage import S3Storage

import time



CHUNK = 4096
PORT = 8888

inference = Inference()
inference.load_model()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'development key'
socketio = SocketIO(app, async_mode=async_mode)
cors = CORS(app, resources={r"/": {"origins": ""}})
#CORS(app)

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


#@app.route('/audioy', methods=['POST'])
@socketio.on('send_message')
def getdata(send_message):
    try:
        tmpVal = json.loads(send_message['body'])
        data = tmpVal['message']
        user = tmpVal['user']
    except Exception as e:
        logger.error("Wrong input - return null", e)
        return ""

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

        #emit
        json_data = json.dumps(data)
        emit('message', {'data': json_data}, broadcast=False, include_self=True)

    #start background thread - merge files - write to db - propagate changes to frontend
    db_aggregation.aggregate_job_results(agg_list, job_id, s3_client)

#@app.route('/audioy', methods=['POST'])
@socketio.on('get_table')
def gettable():
    db_results = []
    user = ""
    uid = ""
    record = None

    try:
        tmp_val = json.loads(get_table['body'])
        user = tmp_val['user']
        uid = tmp_val['uid']
    except Exception as e:
        logger.error("Wrong input - return null", e)
        return ""


    try:
        if uid == "":
            record = db_conn.perform_query(user)
            db_results = db_conn.perform_query_jobs(record['uid'])
    except Exception as e:
        logger.error("No result for table", e)
        return ""

    return db_results


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
    json_data = json.dumps(data)
    emit('echo', {'data': json_data}, broadcast=False, include_self=True)


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
    Response.headers.add('Access-Control-Allow-Origin', '*')
    global thread
    if thread is None:
        thread = Thread(target=background_thread)
        thread.daemon = True
        thread.start()
    return ""


if __name__ == "__main__":
    from gevent import monkey
    monkey.patch_all()
    socketio.run(app, debug=True, port=8888, host="0.0.0.0")
