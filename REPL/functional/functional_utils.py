from .green_functions.music import TurnMusic
from .green_functions.datetime_mac import TellCurrentDatetime
from .green_functions.apps_mac import OpenApp
from .green_functions.email_writer import ComposeEmail
from .green_functions.voice_over import TellNumberUnreadMessages
from .green_functions.safari_surfer import SearchGoogle
from .green_functions.noter import MakeNote

from .red_functions.make_call import CallByPhoneNumber, CallByName
from .red_functions.scheduler import ScheduleCommand, RemoveScheduledCommand
from .red_functions.write_message import MessageByPhoneNumber, MessageByContactName
from .red_functions.run_generated_scripts import ScriptExecution

from .red_functions.run_generated_scripts import check_language
from .BaseClassFunction import RedFunction
import json
import re


available_functions = {
    "turn_music": TurnMusic,
    "tell_current_datetime": TellCurrentDatetime,
    "open_app": OpenApp,
    "compose_email": ComposeEmail,
    "tell_number_unread_messages": TellNumberUnreadMessages,
    "search_google": SearchGoogle,
    "make_note": MakeNote,

    "call_by_phone_number": CallByPhoneNumber,
    "call_by_name": CallByName,
    "schedule_command": ScheduleCommand,
    "remove_scheduled_command": RemoveScheduledCommand,
    "message_by_phone_number": MessageByPhoneNumber,
    "message_by_contact_name": MessageByContactName,

    "execute_script": ScriptExecution,
}


def pipeline_responses_processing(llm_response):
    results = []
    if hasattr(llm_response, 'tool_calls'):
        tool_calls = llm_response.tool_calls
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_argument = tool_call.function.arguments

            if should_confirm_function_execution(function_name):
                if not confirm_tool_function_execution(function_name, function_argument):
                    continue

            return_code, stdout, stderr = get_funcs_response(function_name, function_argument)
            results.append(tuple([stdout, stderr]))
    else:

        code_blocks = parse_markdown_code_blocks(llm_response.content)

        if code_blocks and check_language(code_blocks[0][0]):
            function_argument = {"language": code_blocks[0][0],
                                 "code": code_blocks[0][1]}

            if confirm_tool_function_execution("execute_script", function_argument):
                return_code, stdout, stderr = get_funcs_response("execute_script", function_argument)
                results.append(tuple([stdout, stderr]))
                return results

        results.append(tuple([llm_response.content, None]))
    return results


def should_confirm_function_execution(function_name):
    return issubclass(available_functions[function_name], RedFunction)


def confirm_tool_function_execution(function_name, function_argument):
    if isinstance(function_argument, str):
        function_argument = json.loads(function_argument)
    confirmation_message = available_functions[function_name].get_confirmation_message(**function_argument)
    return confirm_tool_call(confirmation_message)


def confirm_tool_call(string):
    print(string)
    print("---Please type 'Y' or 'y' if you agree, or anything else if you disagree.---")
    line = input("> ").strip()
    if line == 'Y' or line == 'y':
        return True
    return False


def get_funcs_response(function_name, function_argument):
    if isinstance(function_argument, str):
        function_argument = json.loads(function_argument)
    function_to_call = available_functions[function_name]
    function_response = function_to_call.run(**function_argument)
    return function_response


def parse_markdown_code_blocks(markdown_text):
    code_block_regex = re.compile(r'```(python|bash|shell|applescript)\s*([\s\S]+?)```', re.MULTILINE)
    code_blocks = []
    matches = code_block_regex.finditer(markdown_text)
    for match in matches:
        language_name = match.group(1).strip().lower()  # Convert to lowercase
        code_block_content = match.group(2)

        # Replace triple backticks within a string inside the code
        code_block_with_triple_backticks_fixed = code_block_content.replace('```', '``\`')

        # Append the processed code block
        if language_name:
            code_blocks.append(tuple([language_name, code_block_with_triple_backticks_fixed]))

    return code_blocks
