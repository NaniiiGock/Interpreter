import asyncio
import websockets
import json
import communication_utils

async def echo(websocket, path):
    async for message in websocket:
        data = json.loads(message)

        
        interaction_type: InteractioTynpe = int(data["statusCode"])
        assert is_valid_type(interaction_type), "Wrong intertype"

        print("Received: ")
        print(data)

        response = {**message,
                    **{
                    "userInput": f"Echo: {data['userInput']}"
                    }
                }
        
        await websocket.send(json.dumps(response))

async def main():
    async with websockets.serve(echo, "localhost", 8765):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
