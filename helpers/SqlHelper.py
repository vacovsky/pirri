import sqlite3


class SqlHelper:
    conn = None

    def __init__(self, dbpath='data/pirri.db'):
        self.conn = sqlite3.connect(dbpath)

    def setup(self):
        pass

    def read(self, query):
        c = self.conn.cursor()
        c.execute(query)

    def execute(self, query):
        c = self.conn.cursor()
        c.execute(query)
        self.conn.commit()

    def close(self):
        self.conn.close()
