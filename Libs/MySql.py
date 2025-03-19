import mysql.connector

class Mysql:

    def __init__(self, database, user, password, host, port="3306"):
        self.mysql = None
        self.database = database
        self.conn = self._connect(user, password, host, port)

        self.execute_actions_progress = 0.0

    def _connect(self, user, password, host, port):
        return mysql.connector.connect(user=user, password=password,
                                       host=host, port=port,
                                       database=self.database)

    def close(self):
        self.conn.close()

    def execute_actions(self, queries):
        cur = self.conn.cursor()

        for query in queries:
            cur.execute(query)

        self.conn.commit()
        cur.close()

    def execute_query(self, query):
        cur = self.conn.cursor()
        cur.execute(query)
        res = cur.fetchall()
        cur.close()
        return res


