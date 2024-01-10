import asyncio
import websockets
import json
import pickle
from StatusCodes import StatusCode
from Communicator import Communicator
from execution_handler import ExecutionHandler

from response_container import LLMResponse
from response_parser import ResponseParser


### TODO: rewrite
def is_valid_status_code(code: int):
    return code in [0, 1, 2, 3, 4, 7, 8, 10, 11, 15, 16, 17, 18, 19]


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

        if statusCode == StatusCode.EXECUTION_CONFIRMED:
            # await llm_response = DBHandler.get_llm_response(data["UUID"])
            llm_message = b'\x80\x04\x95\xc9\x01\x00\x00\x00\x00\x00\x00\x8c\rlitellm.utils\x94\x8c\x07Message\x94\x93\x94)\x81\x94}\x94(\x8c\x08__dict__\x94}\x94\x8c\x12__pydantic_extra__\x94}\x94(\x8c\x07content\x94N\x8c\x04role\x94\x8c\tassistant\x94\x8c\ntool_calls\x94]\x94h\x00\x8c\x1dChatCompletionMessageToolCall\x94\x93\x94)\x81\x94}\x94(h\x05}\x94(\x8c\x02id\x94\x8c\x1dcall_oIABKi3ICZCzUXuMhCMYD2pP\x94\x8c\x08function\x94h\x00\x8c\x08Function\x94\x93\x94)\x81\x94}\x94(h\x05}\x94(\x8c\targuments\x94\x8c7{\n  "name": "Anastasiia \xf0\x9f\x8c\xb8",\n  "body": "I love you"\n}\x94\x8c\x04name\x94\x8c\x17message_by_contact_name\x94uh\x07}\x94\x8c\x17__pydantic_fields_set__\x94\x8f\x94(h\x1dh\x1b\x90\x8c\x14__pydantic_private__\x94Nub\x8c\x04type\x94\x8c\x08function\x94uh\x07}\x94h \x8f\x94(h#h\x13h\x15\x90h"Nubauh \x8f\x94h"Nub.'
            llm_message = pickle.loads(llm_message)
            statusCode = StatusCode.SENT_FOR_EXECUTION
            response = {**data,
                        **{
                            "statusCode": StatusCode.REQUEST_SENT_TO_API,
                        }
                        }
            await websocket.send(json.dumps(response))
            asyncio.create_task(process_user_input(data, websocket, llm_message, statusCode))

            # response_container = LLMResponse()
            # response_container.set_func_name("message_by_contact_name")
            # response_container.set_func_args(json.dumps({"name": "Anastasiia 🌸",
            #                                              "body": "I love you to the moon and back!"}))
            #
            # data = {**data,
            #         **{
            #             "llmResponse": f"{response_container}",
            #             "statusCode": StatusCode.SENT_FOR_EXECUTION,
            #         }
            #         }
            # print("Sending: ", data)
            # await websocket.send(json.dumps(data))
            # print("SENT")
            # asyncio.create_task(
            #     ExecutionHandler.execute_code_asynchronously(
            #         ResponseParser.get_func_class(response_container.func_name),
            #         response_container.get_formatted_args(), data, websocket
            #     )
            # )


async def process_user_input(data, websocket, llm_message=None, specified_status=None):
    # Call the communicator's method to send input to LLM and get a response
    response_uuid, llm_response, response_status_code = await Communicator.async_swift_input(
        data, websocket, llm_message, specified_status)

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
