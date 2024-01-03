from .music import turn_music
from .scheduler import schedule_command, remove_scheduled_command
from .run_generated_scripts import run_applescript, run_shell_script, run_python_script, run_scripts
import json


available_functions = {
    "turn_music": turn_music,
    "schedule_command": schedule_command,
    "remove_scheduled_command": remove_scheduled_command,
    "run_scripts": run_scripts
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
