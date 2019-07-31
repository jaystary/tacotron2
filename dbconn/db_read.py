import logging

logger = logging.getLogger('root')
'''
def read(conn, cursor, sql):
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()

        for row in rows:
            print("ADMISSION =", row[0])
            print("NAME =", row[1])
            print("AGE =", row[2])
            print("COURSE =", row[3])
            print("DEPARTMENT =", row[4], "\n")

        logger.debug("Operation done successfully")
        return true
    except:
        logger.error("Read failed")
        return false
'''