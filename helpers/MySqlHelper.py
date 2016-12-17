import sqlite3
from data import config as CONFIG


class SqlHelper:
    conn = None

    def __init__(self, dbpath=CONFIG.DBPATH):
        self.conn = sqlite3.connect(dbpath)

    def setup(self):
        pass

    def read(self, query):
        results = []
        c = self.conn.cursor()
        c.execute(query)
        for row in c:
            results.append(row)
        return results

    def execute(self, query):
        c = self.conn.cursor()
        c.execute(query)
        self.conn.commit()
        return True

    def close(self):
        self.conn.close()


if __name__ == '__main__':
    sqlConn = SqlHelper(dbpath='/home/joe/Projects/pirri/data/pirri.sql')
    sid = 1
    sqlStr = ''' SELECT * FROM stations '''
    data = sqlConn.read(sqlStr)
    print(data)
