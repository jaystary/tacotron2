import logging

logger = logging.getLogger('root')

def delete(conn, cursor, sql):
    try:
        cursor.execute(sql)
        conn.commit()
        logger.debug("Total deleted rows:", cur.rowcount)
        return true
    except:
        logger.error("Error delete")
        return false
