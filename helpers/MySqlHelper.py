import pymysql
from data import config as CONFIG
import newrelic.agent


class SqlHelper:
    conn = None

    def __init__(self):
        self.conn = pymysql.connect(CONFIG.MYSQL_HOST,
                                    CONFIG.MYSQL_USER,
                                    CONFIG.MYSQL_PASS,
                                    CONFIG.MYSQL_DB)

    def setup(self):
        pass

    @newrelic.agent.background_task()
    def read(self, query):
        print(query)
        results = []
        c = self.conn.cursor()
        c.execute(query)
        for row in c:
            results.append(row)
        return results

    @newrelic.agent.background_task()
    def execute(self, query):
        print(query)
        c = self.conn.cursor()
        c.execute(query)
        self.conn.commit()
        return True

    @newrelic.agent.background_task()
    def close(self):
        self.conn.close()


if __name__ == '__main__':
    sqlConn = SqlHelper()
    sid = 1
    sqlStr = ''' SELECT * FROM stations '''
    data = sqlConn.read(sqlStr)
    print(data)
