import sqlite3

class DatabaseConnection:
    def __init__(self, db_path='example.db'):
        self.db_path = db_path
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        return self.conn

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            if exc_type is not None:
                # An exception occurred, rollback any changes
                self.conn.rollback()
            else:
                # Commit if no exception
                self.conn.commit()
            self.conn.close()

# Usage example:
with DatabaseConnection('example.db') as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    for row in results:
        print(row)
