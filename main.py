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
S3BUCKET = "https://audiomodelstts.s3.eu-central-1.amazonaws.com/"

inference = Inference()
inference.load_model()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'development key'
socketio = SocketIO(app, async_mode=async_mode)
cors = CORS(app, resources={r"/": {"origins": ""}})
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


@socketio.on('send_message')
def getdata(send_message):
    start = time.time()
    try:
        tmp_val = json.loads(send_message['body'])
        data = tmp_val['message']
        user = tmp_val['user']
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

        response = s3_client.store_data("audiomodelstts", filename, s3_filename)
        print(sentence)
        data = {
                'id': str(time.time()),
                'downloadURL': S3BUCKET+s3_filename,
                'sentence': sentence,
                'duration': str(audio_length),
                'audio_id': count,
                'job_id': S3BUCKET+s3_filename
                }

        emit('player', {'data': data}, broadcast=False, include_self=True)


    #start background thread - merge files - write to db - propagate changes to frontend
    audio_length_total = db_aggregation.aggregate_job_results(agg_list, job_id, s3_client)
    data = {
            'user': user,
            'uid': record['uid']
            }

    status = gettable(data)
    end = time.time()
    print("Produced audio length: " + str(audio_length_total) + " Processing time: " + str(end - start))


@socketio.on('get_table')
def gettable(get_table=None):
    db_results = []
    user = ""
    uid = ""
    record = None
    tmp_val = None
    try:
        user = get_table['user']
        uid = get_table['uid']
    except Exception as e:
        logger.error("Wrong input - return null", e)
        return False

    try:
        if uid == "":
            record = db_conn.perform_query(user)
            db_results = db_conn.perform_query_jobs(record['uid'])
        else:
            db_results = db_conn.perform_query_jobs(uid)
    except Exception as e:
        logger.error("No result for table", e)
        return False

    emit('table', {'data': db_results}, broadcast=False, include_self=True)
    return True


@socketio.on('delete_table')
def delete_entry(delete_table=None):

    uid = ""

    try:
        uid = delete_table['uid']
    except Exception as e:
        logger.error("Wrong input - return null", e)
        return ""

    try:
        record = db_conn.perform_delete_jobs(uid)
    except Exception as e:
        logger.error("No result for table", e)
        return ""

    #emit('table', {'data': db_results}, broadcast=False, include_self=True)


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
