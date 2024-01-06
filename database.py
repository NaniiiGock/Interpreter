import psycopg2
import uuid

class Database:
    def __init__(self, dbname, user, password, host='localhost', port=5432):
        self.conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        self.cur = self.conn.cursor()

        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS data (
                UUID UUID PRIMARY KEY,
                "User Input" TEXT,
                StdOut TEXT,
                StdErr TEXT,
                StatusCode INTEGER,
                is_saved BOOLEAN,
                "LLM Response" TEXT
            )
        ''')
        self.conn.commit()

    def get_saved_rows(self):
        self.cur.execute('SELECT * FROM data WHERE is_saved = TRUE')
        return self.cur.fetchall()

    def get_row_by_uuid(self, uuid):
        self.cur.execute('SELECT * FROM data WHERE UUID = %s', (uuid,))
        return self.cur.fetchone()

    def update_status_code(self, uuid, status_code):
        self.cur.execute('UPDATE data SET StatusCode = %s WHERE UUID = %s', (status_code, uuid))
        self.conn.commit()

    def update_stdout_stderr(self, uuid, stdout, stderr):
        self.cur.execute('UPDATE data SET StdOut = %s, StdErr = %s WHERE UUID = %s', (stdout, stderr, uuid))
        self.conn.commit()

    def add_row(self, user_input, status_code, is_saved=False, llm_response=None):
        new_uuid = uuid.uuid4()
        self.cur.execute('''
            INSERT INTO data (UUID, "User Input", StatusCode, is_saved, "LLM Response")
            VALUES (%s, %s, %s, %s, %s)
        ''', (new_uuid, user_input, status_code, is_saved, llm_response))
        self.conn.commit()

    def update_is_saved(self, uuid, is_saved):
        self.cur.execute('UPDATE data SET is_saved = %s WHERE UUID = %s', (is_saved, uuid))
        self.conn.commit()

    def delete_unsaved_rows(self):
        self.cur.execute('DELETE FROM data WHERE is_saved = FALSE')
        self.conn.commit()

    def __del__(self):
        self.cur.close()
        self.conn.close()


db = Database(dbname='your_dbname', user='your_username', password='your_password')
db.add_row("Example input", 200)
db.add_row("Another input", 404, is_saved=True)
print(db.get_saved_rows())

row_uuid = db.get_saved_rows()[0][0]
print(db.get_row_by_uuid(row_uuid))

db.update_status_code(row_uuid, 500)
db.update_stdout_stderr(row_uuid, "New stdout", "New stderr")
db.update_is_saved(row_uuid, False)

db.delete_unsaved_rows()
