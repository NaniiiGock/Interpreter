from REPL.functional.functional_utils import parse_markdown_code_blocks, check_language, available_functions
from REPL.functional.BaseClassFunction import RedFunction
from .StatusCodes import StatusCode
from .response_container import LLMResponse
import json


class ResponseParser:
    @staticmethod
    def parse_response_object(message):
        """
        parse the message object from llm_response['choices'][0]['message']
        :param message:
        :return: LLMResponse object and StatusCode
        """
        response = LLMResponse()

        # if LLM knows which function to call
        if hasattr(message, 'tool_calls'):
            tool_call = message.tool_calls[0]
            response.set_func_name(tool_call.function.name)
            response.set_func_args(tool_call.function.arguments)
            status_code = ResponseParser.determine_safety(tool_call.function.name)
            return response, status_code

        # if there's executable code in the message
        code_blocks = parse_markdown_code_blocks(message.content)
        if code_blocks and check_language(code_blocks[0][0]):
            response.set_func_name("execute_script")
            response.set_func_args(json.dumps({"language": code_blocks[0][0],
                                               "code": code_blocks[0][1]}))
            return response, StatusCode.ASK_CONFIRMATION

        # if there's no executable code in the message, just raw text
        response.set_content(message.content)
        return response, StatusCode.RAW_TEXT

    @staticmethod
    def determine_safety(function_name: str):
        """
        determine whether the function needs confirmation
        :return:
        """
        function_class = ResponseParser.get_func_class(function_name)
        if issubclass(function_class, RedFunction):
            return StatusCode.ASK_CONFIRMATION
        return StatusCode.SENT_FOR_EXECUTION

    @staticmethod
    def get_func_class(func_name: str):
        """
        get the class of the function
        :param func_name:
        :return:
        """
        return available_functions.get(func_name)


