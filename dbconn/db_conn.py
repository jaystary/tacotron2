import psycopg2
from psycopg2 import extras
from psycopg2.pool import SimpleConnectionPool
from contextlib import contextmanager
from settings import settings
from flask import json
import uuid
from datetime import datetime
import logging

logger = logging.getLogger('root')

DB = SimpleConnectionPool(1,
                          1,
                          host=settings.DB_HOST,
                          database=settings.DB_NAME,
                          user=settings.DB_USER,
                          password=settings.DB_PASSWORD,
                          port="5432"
                          )


@contextmanager
def get_cursor(type=None):
    if type == None:
        return False

    conn = DB.getconn()
    try:
        if type == "read":
            yield conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        if type == "write":
            yield conn.cursor()
        conn.commit()
    except Exception as e:
        conn.rollback()
        logger.error("Connection failed", e)
    finally:
        DB.putconn(conn)

#####################################
def perform_query(user_name, data=None):
    records = None
    sql = "select uid from tschema.users where user_name = %s"
    with get_cursor("read") as cursor:
        try:
            sql = cursor.mogrify(sql, (user_name,))
            cursor.execute(sql, data)
            records = cursor.fetchone()
        except Exception as e:
            logger.error("Registration failed", e)

    return records


def perform_query_jobs(user_uid, data=None):
    records = None
    sql = "select uid, created, headline, agg_duration  from tschema.jobs where users_uid = %s order by created desc"
    with get_cursor("read") as cursor:
        try:
            sql = cursor.mogrify(sql, (user_uid,))
            cursor.execute(sql)
            records = json.dumps(cursor.fetchall())
        except Exception as e:
            logger.error("Registration failed", e)
    return records
#####################################

def perform_insert_register_users(user_name, first_name):
    with get_cursor("write") as cursor:
        try:
            dt = datetime.now()
            cursor.execute(
                'INSERT INTO tschema.users (uid, user_name, last_login, registered, first_name) VALUES (%s, %s, %s, %s, %s);',
                (str(uuid.uuid1()), user_name, dt, dt, first_name))
        except Exception as e:
            logger.error("Registration failed", e)
            return False


#####################################
def perform_insert_jobs(users_uid, delivery_type, chunk_size, headline):
    job_id = str(uuid.uuid1())
    dt = datetime.now()
    with get_cursor("write") as cursor:
        try:
            dt = datetime.now()
            cursor.execute(
                'INSERT INTO tschema.jobs (uid, users_uid, created, delivery_type, chunk_size, headline) VALUES (%s, %s, %s, %s, %s, %s);',
                (job_id, users_uid, dt, delivery_type, chunk_size, headline))
        except Exception as e:
            logger.error("Insert failed", e)
    return job_id


def perform_insert_job_text(job_id, job_text, duration, order_id):
    job_text_id = str(uuid.uuid1())
    dt = datetime.now()
    with get_cursor("write") as cursor:
        try:
            dt = datetime.now()
            cursor.execute(
                'INSERT INTO tschema.job_text (job_text_uid, jobs_uid, job_text, duration, order_id) VALUES (%s, %s, %s, %s, %s);',
                (job_text_id, job_id, job_text, duration, order_id))
        except Exception as e:
            logger.error("Insert failed", e)
    return job_text_id
#####################################

def perform_update_jobs(job_id, agg_duration):
    with get_cursor("write") as cursor:
        try:
            cursor.execute(
                'UPDATE tschema.jobs SET agg_duration = %s WHERE uid = %s;',
                (agg_duration, job_id))
        except Exception as e:
            logger.error("Update failed", e)


def perform_update_jobs_text(job_id, order_id, duration_per):
    with get_cursor("write") as cursor:
        try:
            cursor.execute(
                'UPDATE tschema.job_text SET duration_per = %s WHERE jobs_uid = %s AND order_id = %s;',
                (duration_per, job_id, order_id))
        except Exception as e:
            logger.error("Update failed", e)

##################




