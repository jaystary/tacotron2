from dbconn import db_conn
from backend_helpers import helper
import logging
import os

self.filename = filename
self.audio_length = audio_length
self.job_text_id = job_text_id
self.audio_length_percent = 0


def aggregate_job_results(agg_list, job_id, s3_client):

    audio_length = sum(res.audio_length for res in agg_list)
    filename = helper.merge_wav(agg_list, job_id)
    for obj in agg_list:
        obj.audio_length_percent = obj.audio_length / audio_length

        # remove temp files from system - they are still in S3
        if os.path.exists(obj.filename):
            os.remove(obj.filename)

    #aggregate files
    s3_filename = job_id + ".mp3"
    s3_client.store_data("audiomodelstts", filename, s3_filename)

    #update database
    #write agg duration
    #write per duration
    #prepare json for client:
    #total duration
    #full file

    return True


