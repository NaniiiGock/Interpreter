import asyncio
import websockets
import json
from StatusCodes import StatusCode


async def echo(websocket, path):
    async for message in websocket:
        data = json.loads(message)
        print("Received: ", data)

        statusCode = int(data["statusCode"])

        response = {**data,
                    **{
                        "UUID": "e7143435-a493-4d2d-be1f-ffbc7a696940",
                        "statusCode": 0,
                        "llmResponse": "A response! Integral result: 12 + 42i\nTime taken: -0.04ms\nAccuracy: -0.01%",
                        "StdOut": "",
                        "StdErr": "Something went wrong.",
                    }
                    }

        if statusCode == 19:
            response = [response]

        await websocket.send(json.dumps(response))


async def main():
    async with websockets.serve(echo, "localhost", 8765):
        await asyncio.Future()  # Run forever


if __name__ == "__main__":
    asyncio.run(main())
