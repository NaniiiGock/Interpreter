import asyncio
import websockets
import json
import communication_utils



async def echo(websocket, path):
    async for message in websocket:
        data = json.loads(message)
        print("Received: ")
        print(data)

        statusCode = int(data["statusCode"])
        assert communication_utils.is_valid_status_code(statusCode), "Wrong StatusCode... :/"

        response = {**data,
                    **{
                    "statusCode": 10,
                    "userInput": f"Echo: {data['userInput']}",
                    }
                }
        
        await websocket.send(json.dumps(response))

async def main():
    async with websockets.serve(echo, "localhost", 8765):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
