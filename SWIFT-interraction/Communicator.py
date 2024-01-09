from response_parser import ResponseParser
from StatusCodes import StatusCode
from llm_model.LiteLLMClient import LiteLLMClient
from execution_handler import ExecutionHandler
import asyncio


class Communicator:
    @staticmethod
    async def async_swift_input(data, websocket):
        """
        Function that will be called from swift to send user input to the LLM
        :param data:
        :param websocket:
        :return:
        """
        uuid = data['UUID']
        user_input = data['userInput']

        llm_client = LiteLLMClient("gpt-3.5-turbo")
        llm_message = llm_client.get_response(user_input)
        response, status_code = ResponseParser.parse_response_object(llm_message)

        # <<<Placeholder for writing response into DB>>> #

        if status_code == StatusCode.RAW_TEXT:
            return uuid, response.content, status_code

        elif status_code == StatusCode.SENT_FOR_EXECUTION:
            asyncio.create_task(
                ExecutionHandler.execute_code_asynchronously(
                    ResponseParser.get_func_class(response.func_name),
                    response.get_formatted_args(), data, websocket
                )
            )
            return uuid, ResponseParser.get_func_class(response.func_name).get_exec_description(), status_code
        elif status_code == StatusCode.ASK_CONFIRMATION:
            return uuid, \
                ResponseParser.get_func_class(response.func_name).get_confirmation_message(
                    **response.get_formatted_args()
                ), status_code


async def main():
    # Example usage of async_swift_input
    response = await Communicator.async_swift_input("123", "open Facetime app")
    print(response)

    # Sleep for a short period to allow background tasks to start
    await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())