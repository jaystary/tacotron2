import psycopg2
from psycopg2 import extras
from psycopg2.pool import SimpleConnectionPool
from contextlib import contextmanager
from dbconn import settings
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
        sql = cursor.mogrify(sql, (user_name))
        cursor.execute(sql, data)
        records = cursor.fetchone()
    return records

def perform_query_jobs(user_name, data=None):
    records = None
    sql = "select uid from tschema.users where user_name = %s"
    with get_cursor("read") as cursor:
        sql = cursor.mogrify(sql, (user_name))
        cursor.execute(sql, data)
        records = cursor.fetchone()
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
def perform_insert_jobs(user_id, link, order_id, delivery_type, chunk_size, headline):
    job_id = str(uuid.uuid1())
    dt = datetime.now()
    with get_cursor("write") as cursor:
        try:
            dt = datetime.now()
            cursor.execute(
                'INSERT INTO tschema.jobs (uid, users_id, link, created, delivery_type, chunk_size, headline) VALUES (%s, %s, %s, %s, %s, %s, %s);',
                (job_id, user_id, link, dt, delivery_type, chunk_size, headline))
        except Exception as e:
            logger.error("Insert failed", e)
    return job_id


def perform_insert_job_text(job_id, job_text, duration, order_id):
    dt = datetime.now()
    with get_cursor("write") as cursor:
        try:
            dt = datetime.now()
            cursor.execute(
                'INSERT INTO tschema.job_text (job_text_uid, job_text, duration, order_id) VALUES (%s, %s, %s, %s);',
                (job_id, job_text, duration, order_id))
        except Exception as e:
            logger.error("Insert failed", e)
    return text_id
#####################################


