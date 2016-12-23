import pymysql
import config as CONFIG


class SqlHelper:
    conn = None

    def __init__(self):
        self.conn = pymysql.connect(CONFIG.MYSQL_HOST,
                                    CONFIG.MYSQL_USER,
                                    CONFIG.MYSQL_PASS,
                                    CONFIG.MYSQL_DB)

    def read(self, query):
        if CONFIG.SETTINGS['SQL_DEBUG']:
            print(query)
        results = []
        c = self.conn.cursor()
        c.execute(query)
        for row in c:
            results.append(row)
        return results

    def execute(self, query):
        if CONFIG.SETTINGS['SQL_DEBUG']:
            print(query)
        c = self.conn.cursor()
        c.execute(query)
        self.conn.commit()
        return True

    def close(self):
        self.conn.close()


if __name__ == '__main__':
    sqlConn = SqlHelper()
    sid = 1
    sqlStr = ''' SELECT * FROM stations '''
    data = sqlConn.read(sqlStr)
    print(data)
