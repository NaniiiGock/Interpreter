import asyncio
import websockets
import json



### TODO: rewrite
def is_valid_status_code(code: int):
    return code in [0, 1, 2, 3, 4, 7, 10, 11, 15, 16, 17, 18]


async def echo(websocket, path):
    async for message in websocket:
        data = json.loads(message)
        print("Received: ", data)

        statusCode = int(data["statusCode"])
        assert is_valid_status_code(statusCode), "Wrong StatusCode... :/"

        response = {**data,
                    **{
                    "statusCode": 2,
                    "llmResponse": "I sent this from Python!"
                    }
                }

        await websocket.send(json.dumps(response))

async def main():
    async with websockets.serve(echo, "localhost", 8765):
        await asyncio.Future()  # Run forever


if __name__ == "__main__":
    asyncio.run(main())
