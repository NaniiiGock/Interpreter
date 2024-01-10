import asyncio
import websockets
import json
import pickle
from StatusCodes import StatusCode
from Communicator import Communicator
from async_database import AsyncDatabase
import base64



### TODO: rewrite
def is_valid_status_code(code: int):
    return code in [0, 1, 2, 3, 4, 7, 8, 10, 11, 15, 16, 17, 18, 19]


class StatusCodesMapper:
    @staticmethod
    async def submit_user_response(data, db, websocket):
        response = {
            **data,
            **{
                "statusCode": StatusCode.REQUEST_SENT_TO_API,
            }
        }
        await websocket.send(json.dumps(response))
        await db.add_row(response["userInput"], StatusCode.REQUEST_SENT_TO_API, new_uuid=response["UUID"])
        asyncio.create_task(process_user_input(response, websocket, db))

    @staticmethod
    async def send_for_execution(data, db, websocket):
        row = await db.get_row_by_uuid(data["UUID"])

        llm_message = pickle.loads(row["LLM Response"])
        statusCode = StatusCode.SENT_FOR_EXECUTION
        response = {
            **data,
            "statusCode": statusCode,
        }
        print(llm_message)
        await websocket.send(json.dumps(response))
        asyncio.create_task(process_user_input(data, websocket, db, llm_message, statusCode))

    @staticmethod
    async def saved_to_bookmarks(data, db, websocket):
        await db.update_is_saved(data["UUID"], is_saved=True)

    @staticmethod
    async def remove_from_bookmarks(data, db, websocket):
        await db.update_is_saved(data["UUID"], is_saved=False)

    @staticmethod
    async def asked_all_saved(data, db, websocket):
        await db.delete_unsaved_rows()
        rows = await db.get_saved_rows()
        new_rows = []
        for row in rows:
            llm_response = base64.b64encode(row["LLM Response"]).decode('utf-8')
            new_row = {
                **data,
                "UUID": str(row["uuid"]),
                "statusCode": row["statuscode"],
                "userInput": row["User Input"],
                "StdErr": row["stderr"] if row["stderr"] else "",
                "StdOut": row["stdout"] if row["stdout"] else "",
                # "llmResponse": llm_response
                "llmResponse": "llmResponse"
            }
            new_rows.append(new_row)
        print(new_rows)
        await websocket.send(json.dumps(new_rows))


async def echo(websocket, path):
    db = AsyncDatabase("postgres", "postgres", "postgres", port=5432)
    await db.connect()
    await db.create_table()
    func_mapping = {
        StatusCode.SUBMIT_USER_RESPONSE: StatusCodesMapper.submit_user_response,
        StatusCode.EXECUTION_CONFIRMED: StatusCodesMapper.send_for_execution,
        StatusCode.ASK_RERUN: StatusCodesMapper.send_for_execution,
        StatusCode.SAVE_TO_BOOKMARKS: StatusCodesMapper.saved_to_bookmarks,
        StatusCode.REMOVE_FROM_BOOKMARKS: StatusCodesMapper.remove_from_bookmarks,
        StatusCode.ASK_ALL_SAVED: StatusCodesMapper.asked_all_saved,
    }

    async for message in websocket:
        data = json.loads(message)
        print("Received: ", data)

        statusCode = int(data["statusCode"])
        assert is_valid_status_code(statusCode), "Wrong StatusCode... :/"

        submit_func = func_mapping[statusCode]
        await submit_func(data, db, websocket)


async def process_user_input(data, websocket, db, llm_message=None, specified_status=None):
    # Call the communicator's method to send input to LLM and get a response
    response_uuid, llm_response, llm_description, response_status_code = await Communicator.async_swift_input(
        data, websocket, db, llm_message, specified_status)

    # Send the LLM response back to the client asynchronously
    response = {**data,
                **{
                    "statusCode": response_status_code,
                    "llmResponse": llm_description,
                }
                }
    print("Sending: ", response)
    await websocket.send(json.dumps(response))

    await db.update_llm_response_and_status_code(response_uuid, llm_response, response_status_code)


async def main():
    async with websockets.serve(echo, "localhost", 8765):
        await asyncio.Future()  # Run forever


if __name__ == "__main__":
    asyncio.run(main())
