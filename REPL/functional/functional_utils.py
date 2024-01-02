from .music import turn_music
import json

available_functions = {
    "turn_music": turn_music,
}


def get_funcs_responses(tool_calls):
    responses = []
    for tool_call in tool_calls:
        function_name = tool_call.function.name
        function_to_call = available_functions[function_name]
        function_args = json.loads(tool_call.function.arguments)
        function_response = function_to_call(**function_args)
        responses.append(function_response)
    return responses
