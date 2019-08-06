from dbconn import db_conn
from backend_helpers import helper
import logging
import os

def aggregate_job_results(agg_list, job_id, s3_client):

    filename = ""
    audio_length = sum(res.audio_length for res in agg_list)

    if len(agg_list) > 1:
        filename = helper.merge_wav(agg_list, job_id)

    db_conn.perform_update_jobs(job_id, audio_length)

    for obj in agg_list:
        order_id = obj.filename.split('_')[-1].split('.')[0]

        if order_id is None:
            logging.error("Oops something went wrong here:" + obj.filename)
            continue

        obj.audio_length_percent = obj.audio_length / audio_length
        db_conn.perform_update_jobs_text(job_id, order_id, obj.audio_length_percent)

        if os.path.exists(obj.filename):
            os.remove(obj.filename)

    s3_filename = job_id + ".mp3"
    s3_client.store_data("audiomodelstts", filename, s3_filename)

    return True


