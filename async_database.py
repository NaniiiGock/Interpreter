import asyncpg
import asyncio
import uuid
import pickle
import base64
import datetime


def json_to_bin(json_message):
    return pickle.dumps(json_message)


class AsyncDatabase:

    def __init__(self, dbname, user, password, host='localhost', port=5433):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.lock = asyncio.Lock()

    async def connect(self):
        async with self.lock:
            self.conn = await asyncpg.connect(user=self.user, password=self.password,
                                              database=self.dbname, host=self.host, port=self.port)

    async def create_table(self):
        await self.conn.execute('''
            CREATE TABLE IF NOT EXISTS data (
                UUID UUID PRIMARY KEY,
                "User Input" TEXT,
                StdOut TEXT,
                StdErr TEXT,
                StatusCode INTEGER,
                is_saved BOOLEAN,
                "LLM Response" BYTEA
            )
        ''')

    async def get_rows(self):
        async with self.lock:
            return await self.conn.fetch('SELECT * FROM data')

    async def get_saved_rows(self):
        async with self.lock:
            return await self.conn.fetch('SELECT * FROM data WHERE is_saved = TRUE')

    async def get_row_by_uuid(self, uuid):
        async with self.lock:
            return await self.conn.fetchrow('SELECT * FROM data WHERE UUID = $1', uuid)

    async def remove_row_by_uuid(self, uuid):
        async with self.lock:
            return await self.conn.execute('DELETE FROM data WHERE UUID = $1', uuid)

    async def update_status_code(self, uuid, status_code):
        async with self.lock:
            await self.conn.execute('UPDATE data SET StatusCode = $1 WHERE UUID = $2', status_code, uuid)

    async def update_stdout_stderr(self, uuid, stdout, stderr):
        async with self.lock:
            await self.conn.execute('UPDATE data SET StdOut = $1, StdErr = $2 WHERE UUID = $3', stdout, stderr, uuid)

    async def add_row(self, user_input, status_code, new_uuid, is_saved=False, llm_response=None, date=None):
        current_date = datetime.datetime.now() if date is None else datetime.datetime.strptime(date, '%d.%m.%Y, %H:%M')
        if llm_response:
            llm_response = json_to_bin(llm_response)
        async with self.lock:
            await self.conn.execute('''
                INSERT INTO data (UUID, "User Input", StatusCode, is_saved, "LLM Response", date)
                VALUES ($1, $2, $3, $4, $5, $6)
            ''', str(new_uuid), user_input, status_code, is_saved, llm_response, current_date)

    async def update_is_saved(self, uuid, is_saved):
        async with self.lock:
            await self.conn.execute('UPDATE data SET is_saved = $1 WHERE UUID = $2', is_saved, uuid)

    async def delete_unsaved_rows(self):
        async with self.lock:
            await self.conn.execute('DELETE FROM data WHERE is_saved = FALSE')

    async def delete_all_rows(self):
        async with self.lock:
            await self.conn.execute('DELETE FROM data')

    async def close(self):
        async with self.lock:
            await self.conn.close()

    async def update_llm_response_and_status_code(self, uuid, llm_response, status_code):
        llm_response = json_to_bin(llm_response)
        async with self.lock:
            await self.conn.execute('UPDATE data SET StatusCode = $1, "LLM Response" = $2 WHERE UUID = $3', status_code,
                                    llm_response, uuid)


async def test_database_operations():
    db = AsyncDatabase(dbname='postgres', user='postgres', password='postgres', host='localhost', port=5432)

    await db.connect()
    print("Connected")

    await db.create_table()
    print("Table created.")
    #
    # await db.add_row("Test input 1", 200, is_saved=True, llm_response="Response 1")
    # await db.add_row("Test input 2", 404, is_saved=False, llm_response="Response 2")
    # print("Rows added.")
    #
    #
    # rows = await db.get_rows()
    # print("All rows:")
    # for row in rows:
    #     print(row)
    #
    #
    # new_llm_response = json_to_bin("llm response")
    #
    # await db.update_llm_response_and_status_code("23760804-d81c-4459-bdcb-65588b993109", new_llm_response, 300)
    #
    #
    # saved_rows = await db.get_saved_rows()
    # print("\nsaved rows:")
    # for row in saved_rows:
    #     print(row)
    #
    #
    # await db.delete_unsaved_rows()
    # # await db.delete_all_rows()
    #
    # saved_rows = await db.get_saved_rows()
    # print("\nSaved rows:")
    # for row in saved_rows:
    #     print(row)
    #
    # rows = await db.get_rows()
    # print("All rows:")
    # for row in rows:
    #     print(row)

    await db.delete_all_rows()

    saved_rows = await db.get_saved_rows()
    print("\nSaved rows:")
    for row in saved_rows:
        print(row)

    # await db.close()
    # print("Unsaved rows deleted and database connection closed.")


if __name__ == "__main__":
    asyncio.run(test_database_operations())
    pass