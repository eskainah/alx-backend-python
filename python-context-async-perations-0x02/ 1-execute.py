import sqlite3

class ExecuteQuery:
    def __init__(self, db_path='example.db', query="SELECT * FROM users WHERE age > ?", param=(25,)):
        self.db_path = db_path
        self.query = query
        self.param = param
        self.conn = None
        self.results = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        cursor = self.conn.cursor()
        cursor.execute(self.query, self.param)
        self.results = cursor.fetchall()
        return self.results

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            self.conn.close()

# Usage example:
with ExecuteQuery() as results:
    for row in results:
        print(row)
