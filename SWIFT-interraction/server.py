import asyncio
import websockets
import json
from .StatusCodes import StatusCode
from .Communicator import Communicator


### TODO: rewrite
def is_valid_status_code(code: int):
    return code in [0, 1, 2, 3, 4, 7, 10, 11, 15, 16, 17, 18, 19]


async def echo(websocket, path):
    async for message in websocket:
        data = json.loads(message)
        print("Received: ", data)

        statusCode = int(data["statusCode"])
        assert is_valid_status_code(statusCode), "Wrong StatusCode... :/"

        if statusCode == StatusCode.SUBMIT_USER_RESPONSE:
            response = {**data,
                        **{
                            "statusCode": StatusCode.REQUEST_SENT_TO_API,
                        }
                        }
            await websocket.send(json.dumps(response))
            asyncio.create_task(process_user_input(data, websocket))


        # if statusCode == StatusCode.


async def process_user_input(data, websocket):
    uuid = data['UUID']
    user_input = data['userInput']

    # Call the communicator's method to send input to LLM and get a response
    response_uuid, llm_response, response_status_code = await Communicator.async_swift_input(data, websocket)

    # Send the LLM response back to the client asynchronously
    response = {**data,
                **{
                    "statusCode": response_status_code,
                    "llmResponse": llm_response,
                    "UUID": response_uuid
                }
                }
    print("Sending: ", response)
    await websocket.send(json.dumps(response))


async def main():
    async with websockets.serve(echo, "localhost", 8765):
        await asyncio.Future()  # Run forever


if __name__ == "__main__":
    asyncio.run(main())
