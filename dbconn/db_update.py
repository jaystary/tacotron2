import logging

logger = logging.getLogger('root')
'''
def update(conn, cursor, sql):
    try:
        cursor.execute(sql)
        conn.commit()
        logger.debug("Total updated rows:", cur.rowcount)
        return true
    except:
        logger.error("Update failed")
        return false
'''