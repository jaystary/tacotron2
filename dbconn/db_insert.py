import logging

logger = logging.getLogger('root')


def insert(conn, cursor, sql):
    try:
        cursor.execute(sql);
        conn.commit()
        logger.debug("Record inserted successfully")
        return true
    except:
        logger.warning("error insert")
        return false
